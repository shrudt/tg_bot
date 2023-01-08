import requests
import logging

stat_logger = logging.getLogger('stat')


def send_statistic(name, user_id, url='http://nginx:80'):
    try:
        requests.post(f'{url}/{name}', timeout=0.1, json={'user_id': str(user_id)})
    except requests.ConnectionError as er:
        stat_logger.info(er)


