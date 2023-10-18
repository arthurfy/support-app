import os
import pandas as pd
from components.common import common

logger = common.logger

# CSV ENCODING: "windows-1252"
# CSV ENCODING: 'ISO-8859-1'


def import_csv_to_dataframe(file_path: str,
                            encoding: str = None,
                            dtype: dict = None) -> pd.DataFrame:
  '''
  import csv into a dataframe

  Parameters
  ----------
  file_path : str
  encoding : str
  dtype : dict, optional
  
  Returns
  -------
  pd.DataFrame

  Example dtype: 
  dtype = {'ID' : int, FirstName': str}
  '''
  # check if file path exists
  if not os.path.exists(file_path):
    raise FileNotFoundError(f'{file_path} does not exist')

  # check if the file is a csv
  if not file_path.endswith('.csv'):
    raise TypeError(f'{file_path} is not a csv file')

  # check if encoding is None and set default value
  if encoding is None:
    encoding = 'utf-8'

  # check if dtype is None and set default value, to handle low memory issues
  if dtype is None:
    dtype = object

  # try to import csv into a dataframe
  try:
    df = pd.read_csv(file_path, encoding=encoding, dtype=dtype)

    return None if df.empty else df

  except Exception as error:
    logger.error(f'import_csv_to_dataframe error: {error}')

    return None
