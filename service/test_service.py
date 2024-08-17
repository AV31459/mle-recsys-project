import logging
import sys
import os
from dotenv import load_dotenv
import json
import requests

load_dotenv('.env_service')

logger = logging.getLogger('recsys_test')
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(
    logging.Formatter(
        '%(name)s: %(levelname)s: %(message)s'
    )
)
logger.addHandler(log_handler)
logger.setLevel('INFO')

logger.info('Starting the tests for RecSys service...')
service_uri = 'http://' + os.getenv('HOST') + ':' + os.getenv('PORT')

logger.info(f'Target service uri: {service_uri}')

# Загружаем данные тестов из test_data.json
with open('service/test_data.json', 'r') as f:
    test_data = json.load(f)

logger.info('Test data loaded')
logger.info('Starting tests...')
logger.info('-' * 40)

errors = False

for num, test in enumerate(test_data, 1):
    logger.info(f'Test {num}: {test["test_name"]}')
    logger.info(f'>>> Request: uri="{test["uri"]}", method="{test["method"]}", '
                f'data={test["data"]}, ')
    logger.info(f'<!> Expected: code={test["response_code"]}, '
                f'data={test.get("response_data", "<any>")}')

    test_uri = service_uri + test["uri"]

    response = getattr(requests, test['method'])(
        url=(service_uri + test["uri"]),
        headers={'Content-type': 'application/json',
                 'Accept': 'application/json'},
        data=json.dumps(test['data'])
    )

    logger.info(f'<<< Response: code={response.status_code}, '
                f'data={response.json()}')

    if (
        response.status_code != test['response_code']
        or (
                test.get('response_data')
                and response.json() != test['response_data']
            )
    ):
        errors = True
        logger.error(f'TEST {num} FAILED!')
        continue
    logger.info('PASSED!')
    logger.info('-' * 40)

if errors:
    logger.error('TESTS FAILED!!!')
logger.info('OK! ALL TESTS PASSED.')
