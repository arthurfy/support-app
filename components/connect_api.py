import sys
import os
import logging
import shutil
import datetime
import json
import requests
import ssl
import hashlib
import pandas as pd
from urllib3 import poolmanager

from components import common

logger = common.logger
'''
import API module
'''


class TLSAdapter(requests.adapters.HTTPAdapter):

  def init_poolmanager(self, connections, maxsize, block=False):
    """Create and initialize the urllib3 PoolManager."""
    ctx = ssl.create_default_context()
    ctx.set_ciphers('DEFAULT@SECLEVEL=1')
    self.poolmanager = poolmanager.PoolManager(num_pools=connections,
                                               maxsize=maxsize,
                                               block=block,
                                               ssl_version=ssl.PROTOCOL_TLS,
                                               ssl_context=ctx)


def api_request(url: str,
                headers: dict,
                method: str = None,
                tls: bool = False,
                request_body=None,
                params: dict = None) -> pd.DataFrame:
  '''
    create an api request and return a repsonse\n\n

    params =  form the query string in the URL\n
    request_body = is used to fill the body of a request (together with files 
    '''
  # check if url is none
  if url is None:
    logger.error("The url is None")
    raise Exception("The url is None")

  logger.info(f"API REQUEST URL: {url}")

  # check if headers is none:
  if headers is None:
    logger.error("The headers is None")
    raise Exception("The headers is None")

  logger.info(f"API REQUEST HEADERS: {headers}")

  if method is None:
    method = "GET"

  # Create session
  session = requests.session()

  # check tls
  if tls:
    session.mount('https://', TLSAdapter())

  if method == "GET":
    # GET request
    response = session.get(url,
                           headers=headers,
                           data=request_body,
                           params=params)
  elif method == "POST":
    # POST request
    response = session.post(url,
                            headers=headers,
                            data=request_body,
                            params=params)
  else:
    # Default to GET request
    response = session.get(url,
                           headers=headers,
                           data=request_body,
                           params=params)

  # if status code is not 200 raise an error
  if response.status_code != 200:
    raise Exception("API request failed: {}".format(response.status_code))

  logger.info("The response is 200 okay")

  # log the repsonse
  pretty_response = json.dumps(response.json(), indent=4, sort_keys=True)
  logger.info("The response is: {}".format(pretty_response))

  return response


def api_response_to_dataframe(
    response: requests.models.Response) -> pd.DataFrame:
  '''
  convert a api repsonse to a dataframe
  '''

  # check if response is none
  if response is None:
    logger.error("The response is None")
    raise Exception("The response is None")

  # convert reponse to dataframe
  df = pd.DataFrame(response.json())

  return None if df.empty else df


def api_standard(api_key: str = None) -> dict:
  '''
    create parameters for a standard api request
    '''

  headers = {
      "Content-Type": "application/json",
  }

  # add api key to headers
  if api_key is not None:
    headers.update({"Authorization": f"Bearer {api_key}"})

  return headers


def api_request(url: str,
                headers: dict,
                method: str = None,
                tls: bool = False,
                request_body=None,
                params: dict = None) -> pd.DataFrame:
  '''
    create an api request and return a repsonse\n\n

    params =  form the query string in the URL\n
    request_body = is used to fill the body of a request (together with files 
    '''
  # check if url is none
  if url is None:
    logger.error("The url is None")
    raise Exception("The url is None")

  logger.info(f"API REQUEST URL: {url}")

  # check if headers is none:
  if headers is None:
    logger.error("The headers is None")
    raise Exception("The headers is None")

  logger.info(f"API REQUEST HEADERS: {headers}")

  if method is None:
    method = "GET"

  # Create session
  session = requests.session()

  # check tls
  if tls:
    session.mount('https://', TLSAdapter())

  if method == "GET":
    # GET request
    response = session.get(url,
                           headers=headers,
                           data=request_body,
                           params=params)
  elif method == "POST":
    # POST request
    response = session.post(url,
                            headers=headers,
                            data=request_body,
                            params=params)
  else:
    # Default to GET request
    response = session.get(url,
                           headers=headers,
                           data=request_body,
                           params=params)

  # if status code is not 200 raise an error
  if response.status_code != 200:
    raise Exception("API request failed: {}".format(response.status_code))

  logger.info("The response is 200 okay")

  # log the repsonse
  pretty_response = json.dumps(response.json(), indent=4, sort_keys=True)
  logger.info("The response is: {}".format(pretty_response))

  return response


def api_response_to_dataframe(
    response: requests.models.Response) -> pd.DataFrame:
  '''
    convert a api repsonse to a dataframe
    '''

  # check if response is none
  if response is None:
    logger.error("The response is None")
    raise Exception("The response is None")

  # convert reponse to dataframe
  df = pd.DataFrame(response.json())

  return None if df.empty else df


def api_standard(api_key: str = None) -> dict:
  '''
    create parameters for a standard api request
    '''

  headers = {
      "Content-Type": "application/json",
  }

  # add api key to headers
  if api_key is not None:
    headers.update({"Authorization": f"Bearer {api_key}"})

  return headers


def api_marvel(marvel_public_api_key: str,
               marvel_private_api_key: str) -> dict:
  '''
    create parameters for a marvel api request\n\n

    request example:\n\n

    marvel_api_url = "https://gateway.marvel.com/v1/public/characters"#\n
    marvel_headers, marvel_params = api_marvel(api_key_public_marvel, api_key_private_marvel)\n
    marvel_response = api_request(marvel_api_url, marvel_headers,None, True, None, marvel_params)\n
    print(marvel_response.json())
    '''

  # create headers
  headers = {
      "Content-Type": "application/json",
  }

  # create marvel timestmap
  timestamp = datetime.datetime.now().strftime("%Y-%m-%d%H:%M:%S")
  logger.info(f"MARVEL API: Timestamp: {timestamp}")

  # create marvel has
  hash = hashlib.md5(
      f"{timestamp}{marvel_private_api_key}{marvel_public_api_key}".encode(
          'utf-8')).hexdigest()
  logger.info(f"MARVEL API: Hash: {hash}")

  params = {"ts": timestamp, "apikey": marvel_public_api_key, "hash": hash}

  return headers, params


if __name__ == "__main__":
  pass
