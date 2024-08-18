import logging
from itertools import zip_longest

import pandas as pd
from pydantic import BaseModel, Field, NonNegativeInt, PositiveInt


class RecSysRequest(BaseModel):
    """Pydantic model of incoming recommendations request."""

    user_id: NonNegativeInt = Field(..., description='User ID')
    n_recs: PositiveInt = Field(10, description='Number of recommendations')
    last_items: list[NonNegativeInt] = Field(
        [], description='Ids of last items user interacted with'
    )


class RecSysResponse(BaseModel):
    """Pydantic model of outgoing recsys response."""

    recs: list[NonNegativeInt] = Field(
        ..., description='Ids of recommended items'
    )


class RecSysHandler:
    """
    Main handler class for recommendations retreival.

    Attributes:
        - **top_popular_recs_path** - path to a file with pre-saved
        non-personalised recommendations, a table with columns (item_id, score)

        - **personal_recs_path** -  path to a file with pre-saved personalised
        recommendations: a table with columns (user_id, item_id, score)

        - **similar_items_path** - path to a file with pre-saved table with
        similar items (item_id, sim_item_id, score).
    """

    def __init__(self, top_popular_recs_path: str, personal_recs_path: str,
                 similar_items_path: str):
        self.top_popular_recs_path = top_popular_recs_path
        self.personal_recs_path = personal_recs_path
        self.similar_items_path = similar_items_path
        self.logger = logging.getLogger('recsys_service')

    def load_data(self):
        """Load pre-saved offline recommendations to memory."""

        # Загружаем топ-популярные рекомендации в формате
        # (item_id, score)
        self.logger.debug('Loading top-popular recs from:  '
                          f'{self.top_popular_recs_path}')
        self.top_popular_recs = (
            pd.read_parquet(self.top_popular_recs_path,
                            columns=['item_id', 'score'])
            .sort_values(by='score', ascending=False)
        )

        # Загружаем персональные рекомендации в формате
        # (user_id, item_id, score),
        # NB: устанавливаем user_id как индекс
        self.logger.debug('Loading personal recs from:  '
                          f'{self.personal_recs_path}')
        self.personal_recs = (
            pd.read_parquet(self.personal_recs_path,
                            columns=['user_id', 'item_id', 'score'])
            .sort_values(by=['user_id', 'score'], ascending=[True, False])
            .set_index('user_id')
        )

        # Загружаем похожие объекты в формате
        # (item_id, sim_item_id, score)
        # NB: устанавливаем item_id как индекс
        self.logger.debug('Loading similar items from:  '
                          f'{self.similar_items_path}')
        self.similar_items = (
            pd.read_parquet(self.similar_items_path,
                            columns=['item_id', 'sim_item_id', 'score'])
            .sort_values(by=['item_id', 'score'], ascending=[True, False])
            .set_index('item_id')
        )

    def get_recs(self, user_id: NonNegativeInt, n_recs: PositiveInt,
                 last_items: list[NonNegativeInt]) -> list[NonNegativeInt]:
        """Get list of recommendations."""

        # Если пользователь холодный, в качестве оффлайн рекомендаций
        # для него используем топ-популярные
        if user_id not in self.personal_recs.index:
            offline_recs = (self.top_popular_recs['item_id']
                            .head(n_recs).to_list())
        else:
            offline_recs = (self.personal_recs.loc[user_id]['item_id']
                            .head(n_recs).to_list())

        # Очищаем список последних просмотренных объектов от идентификаторов,
        # для которых у нас, возможно, нет похожих объектов
        last_items = [x for x in last_items if x in self.similar_items.index]

        # В качестве онлайн рекомендации для каждого из последных просмотренных
        # пользователем объектов берем по одному наиболее похожему
        online_recs = (self.similar_items.loc[last_items].groupby('item_id')
                       .head(1)['sim_item_id'].tolist())

        # Объединяем списки путем чередования онлайн/офлайн рекомендаций
        final_recs = [x for pair in zip_longest(online_recs, offline_recs)
                      for x in pair if x is not None]

        # Удаляем из финального списка возможные дубликаты,
        # оставляем не более n_recs рекомендаций
        return pd.Series(final_recs).drop_duplicates().head(n_recs).tolist()
