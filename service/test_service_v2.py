# import logging
# import sys
# import os
from dotenv import load_dotenv
# import json
# import requests
# import argparse
import pytest

load_dotenv('.env_service')


@pytest.fixture(scope='session')
def params():
    return [1, 2, 3]


@pytest.mark.parametrize('number', params)
def test_test(number):
    assert number
