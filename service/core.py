import logging
# import sys
from typing import Literal

import pandas as pd
from pydantic import BaseModel, Field, PositiveInt, NonNegativeInt


class RecSysRequest(BaseModel):
    """Pydantic model of incoming recommendations request."""

    type: Literal['top_popular', 'personal', 'mixed'] = Field(
        ..., description='Type of recommendations'
    )
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
        # (user_id, item_id, score)
        self.logger.debug('Loading personal recs from:  '
                          f'{self.personal_recs_path}')
        self.personal_recs = (
            pd.read_parquet(self.personal_recs_path,
                            columns=['user_id', 'item_id', 'score'])
            .sort_values(by=['user_id', 'score'], ascending=[True, False])
        )

        # Загружаем похожие объекты в формате
        # (item_id, sim_item_id, score)
        self.logger.debug('Loading similar items from:  '
                          f'{self.similar_items_path}')
        self.similar_items = (
            pd.read_parquet(self.similar_items_path,
                            columns=['item_id', 'sim_item_id', 'score'])
            .sort_values(by=['item_id', 'score'], ascending=[True, False])
        )

    def get_recs(self, type: str, user_id: NonNegativeInt, n_recs: PositiveInt,
                 last_items: list[NonNegativeInt]) -> list[NonNegativeInt]:
        """Get list of recommendations."""

        if type == 'top_popular':
            return self.top_popular_recs['item_id'].head(n_recs).to_list()

        return []
