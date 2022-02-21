import requests

import logging
from time import time
from functools import partial

from concurrent.futures import ProcessPoolExecutor


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

URL = 'http://localhost:8000/view/menus/'
USER = 'admin'
PASS = '123123'



def access_rest_api(path, arg):
    r = requests.get(URL,auth=(USER,PASS))
    print(r.status_code, r.text[0:30])


def main():
    ts = time()
    access_api = partial(access_rest_api, URL)

    with ProcessPoolExecutor() as executor:
        executor.map(access_api, range(20))
    logging.info('Took %s', time() - ts)


if __name__ == '__main__':
    main()


