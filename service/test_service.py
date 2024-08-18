import logging
import sys
import os
from dotenv import load_dotenv
import json
import requests
import argparse

load_dotenv('.env_service')

# Парсим аргументы командной строки
cli_parser = argparse.ArgumentParser()
cli_parser.add_argument('--strict', action='store_true',
                        help='Strict response check mode')
strict_mode = cli_parser.parse_args().strict

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
logger.info(f'Strict response check mode: {strict_mode}')

# Загружаем данные тестов из test_data.json
with open('service/test_data.json', 'r') as f:
    test_data = json.load(f)

logger.info('Test data loaded')
logger.info('Starting tests...')
logger.info('-' * 40)

errors = False

# Прогоняем загруженные тесты
for num, test in enumerate(test_data, 1):
    logger.info(f'Test {num}: "{test["test_name"]}"')
    logger.info(f'>>> Request: uri="{test["uri"]}", '
                f'method="{test["method"]}", '
                f'data={test.get("data", "<empty>")}')
    logger.info(f'<!> Expected: code={test["response_code"]}, '
                f'data={test.get("response_data", "<any>")}')

    response = getattr(requests, test['method'])(
        url=(service_uri + test["uri"]),
        headers={'Content-type': 'application/json',
                 'Accept': 'application/json'},
        data=json.dumps(test['data'])
    )

    logger.info(f'<<< Response: code={response.status_code}, '
                f'data={response.json()}')

    if (
        # Не совпадает response code
        response.status_code != test['response_code']
        # или не соответствует response data
        or (
            test.get('response_data')
            and (
                (strict_mode and response.json() != test['response_data'])
                or (len(response.json()['recs']) != len(test['response_data']
                                                        ['recs']))
            )
        )
    ):
        errors = True
        logger.error(f'TEST {num} FAILED!')
        continue
    logger.info(f'Test {num} PASSED!')
    logger.info('-' * 40)

if errors:
    logger.error('TESTS FAILED!!!')
else:
    logger.info('OK! ALL TESTS PASSED.')
