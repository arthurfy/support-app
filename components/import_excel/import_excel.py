import os
import pandas as pd
from components.common import common

logger = common.logger


def import_excel_to_dataframe(file_path: str,
                              target_sheet: str = None) -> pd.DataFrame:
  '''
  import excel into a dataframe

  Parameters
  ----------
  file_path : str
  target_sheet : str
  
  Returns
  -------
  pd.DataFrame
  '''

  # check if file path exists
  if not os.path.exists(file_path):
    raise FileNotFoundError(f'{file_path} does not exist')

  # check if the file is a csv
  if not file_path.endswith('.xlsx') or not file_path.endswith('.xlsm'):
    raise TypeError(f'{file_path} is not an excel file')

  # try to read the excel file
  try:
    excel_file = pd.ExcelFile(file_path)

    # collect the excel sheetnames
    sheet_names = excel_file.sheet_names

    # try to find sheet name and if not default to the first sheet
    if target_sheet in sheet_names:
      df = pd.read_excel(file_path, sheet_name=target_sheet)
    else:
      df = pd.read_excel(file_path, sheet_name=sheet_names[0])

    return None if df.empty else df

  except Exception as error:
    logger.error(f'import_excel_to_dataframe error: {error}')

    return None
