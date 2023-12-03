import sys
import os
import datetime
import json
import requests
import ssl
import hashlib
import pandas as pd
import json
from urllib3 import poolmanager
try:
  from components import common
except ModuleNotFoundError as error:
  print(f"{error} from connect_api.py")
  sys.path.append(os.getcwd())
  from components import common

logger = common.logger
'''
Making requests against APIs
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
                headers: dict = None,
                method: str = None,
                request_body = None,
                parameters: dict = None,
                tls: bool = False,
                api_key : str = None,
                log_response : bool = False) -> pd.DataFrame:
  
  '''
  create an api request and return a repsonse

  PARAMETERS
  ----------
  url : str
  headers : dict
  method : str
  tls : bool
  request_body : API specific
  params : dict

  RETURN
  ------
  response : api response data
  '''
  # Check if url is none
  if url is None:
    logger.error("The url is None")
    raise Exception("The url is None")

  logger.info(f"api request - url - {url}")

  # Check if headers is none:
  if headers is None:
    headers = {
      "Content-Type": "application/json",
    }

  logger.info(f"api request - headers - {headers}")

  # Check api key
  if api_key is not None:
    headers.update({"Authorization": f"Bearer {api_key}"})
    logger.info(f"api request - api key - true")

  # Create session
  session = requests.session()

  # Check tls
  if tls:
    session.mount('https://', TLSAdapter())

  # Check method
  if method is None:
    method = "GET"

  logger.info(f"api request - method - {method}")

  if method == None:
    method = "GET"

  if method == "GET":
    # GET method: retrieves information or data from a specified resource.
    response = session.get(url,
                           headers=headers,
                           data=request_body,
                           params=parameters)

  elif method == "POST":
    # POST method: submits data to be processed to a specified resource.
    response = session.post(url,
                            headers=headers,
                            data=request_body,
                            params=parameters)
    
  elif method == "PUT": 
    # PUT method: updates a specified resource with new data.
    logger.info(f"api request - method - {method} - not configured")
    raise ValueError(f"api method {method} not configured")

  elif method == "DELETE":
    # DELETE method: deletes a specified resource.
    logger.info(f"api request - method - {method} - not configured")
    raise ValueError(f"api method {method} not configured")

  elif method == "PATCH":
    # PATCH method: partially updates a specified resource.
    logger.info(f"api request - method - {method} - not configured")
    raise ValueError(f"api method {method} not configured")

  else:
    logger.info(f"api request - method - {method} - not configured")
    raise ValueError(f"api method {method} not configured")


  # Check status code
  if response.status_code != 200:
    response_status_error = "API request failed: {}".format(response.status_code)
    logger.error(response_status_error)
    raise Exception(response_status_error)

  logger.info(f"api request - response - okay")

  # Check response
  if log_response == True:
    pretty_response = json.dumps(response.json(), indent=4, sort_keys=True)
    logger.info("The response is: {}".format(pretty_response))

  return None if response.status_code != 200 else response

def api_response_converter(
    response: requests.models.Response, format:str):
  '''
  convert api repsonse

  PARAMETERS
  ----------
  response : api response data

  RETURN
  ------
  dataframe
  json

  '''

  # check if response is none
  if response is None:
    error_message = "api converted - response is None"
    logger.error(error_message)
    raise Exception(error_message)
  
  # check response status
  if response.status_code != 200:
    error_message = f"api converted - response code - {response.status_code}"
    logger.error(error_message)
    raise Exception(error_message)
  
  format = format.lower()

  if format == "json":
    # convert reponse to json
    json_format = response.json()
    return None if len(json_format) == 0 else json_format

  if format == "df":
    # convert reponse to dataframe
    df = pd.DataFrame(response.json())
    return None if df.empty else df

  return None

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

  # API TESTING
  placeholder_api = "https://jsonplaceholder.typicode.com/posts"
  response = api_request(placeholder_api)
  response_converted = api_response_converter(response, "json")
  print("Response Type: ", type(response_converted))
  print(response_converted[0])
  print(type(response_converted[0]))
  pass

