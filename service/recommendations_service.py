import logging
import os
import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from core import RecSysHandler, RecSysRequest, RecSysResponse


load_dotenv('.env_service')

# Настраиваем логгер
logger = logging.getLogger('recsys_service')
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter(
        '%(levelname)s:\t%(name)s:  %(asctime)s : %(message)s'
    )
)
logger.addHandler(log_handler)
logger.setLevel(os.getenv('LOG_LEVEL'))
logger.info('Recsys service module is being initialized.')


# Основной объект-хендлер для получения рекомендаций
recsys_handler = RecSysHandler(
    top_popular_recs_path=os.getenv('TOP_POPULAR_RECS_PATH'),
    personal_recs_path=os.getenv('PERSONAL_RECS_PATH'),
    similar_items_path=os.getenv('SIMILAR_ITEMS_PATH')
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    recsys_handler.load_data()
    logger.info('RecSysHandler data loaded, ready to serve requests.')
    yield
    logger.info('Recsys service is being shut down.')


# Основной объект приложения
app = FastAPI(title="Recommendation service", lifespan=lifespan)


# Healthcheck URI
@app.get('/')
def healthcheck():
    """Get service health status."""

    logger.debug('Healthchek handler called')
    return 'Service appears to be up and running.'


# Основной URI сервиса
@app.post('/recs', response_model=RecSysResponse)
def recommend(request: RecSysRequest):
    """Get recommendations."""

    logger.debug(f'Valid recs request received: {request}')

    #  Передаем паремтры в хендлер и получаем рекомендации
    response = RecSysResponse(recs=recsys_handler.get_recs(
        user_id=request.user_id,
        n_recs=request.n_recs,
        last_items=request.last_items
    ))
    logger.debug(f'Sending back response: {response}')

    return response


logger.info('Recsys service module initialization completed.')


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=os.getenv('HOST'),
        port=int(os.getenv('PORT')),
    )
