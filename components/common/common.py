import os
import sys
import logging
import datetime

# setup application logging
logging.basicConfig(filemode='app.log',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def application_path():
  '''
  calculated the application path from switch it is running.
  required when running from an executable
  '''
  if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    return bundle_dir
  else:
    bundle_dir = os.getcwd()
    return bundle_dir


# Setup file paths
APP_PATH = application_path()
DATA_FOLDER = os.path.join(APP_PATH, "data")
WORKSPACE_FOLDER = os.path.join(APP_PATH, "workspace")
CUSTOMERS = os.path.join(DATA_FOLDER, 'customers.csv')
ORDER_DETAILS = os.path.join(DATA_FOLDER, 'order_details.csv')
ORDERS = os.path.join(DATA_FOLDER, 'orders.csv')
PRODUCTS = os.path.join(DATA_FOLDER, 'products.csv')


def copy_list_of_files_from_source_to_destination(source_path: str,
                                                  destination_path: str,
                                                  file_list: list):
  '''
  copy a list of files from one location to another

  PARAMETERS
  ----------
  source_path : str
  destination_path : str
  file_list : list
  
  '''
  # check if the source path exists
  if not os.path.exists(source_path):
    logger.error("The source path does not exist")
    raise FileNotFoundError

  # check if the destination path exists
  if not os.path.exists(destination_path):
    logger.error("The destination path does not exist")
    raise FileNotFoundError

  # check if the file list is empty
  if len(file_list) == 0:
    logger.error("The file list is empty")
    raise ValueError

  # copy the files
  for file in file_list:
    shutil.copy2(os.path.join(source_path, file), destination_path)
    # check if the destination file exists after being copied
    if not os.path.exists(os.path.join(destination_path, file)):
      logger.error("The file was not copied to the destination path")
      raise FileNotFoundError


def get_list_of_files_in_directory(directory_path: str) -> list:
  '''
    get a list of files from a directory

    PARAMETERS
    ----------
    source_path : str

    RETURNS
    -------
    list of files
    '''
  # check if the directory path exists
  if not os.path.exists(directory_path):
    logger.error("The directory path does not exist")
    raise FileNotFoundError

  # get the list of files
  file_list = os.listdir(directory_path)

  return file_list


def open_directory_in_file_explorer(directory_path: str):
  '''
    open the application directory in file explorer

    PARAMETERS
    ----------
    directory_path : str
    
    ''' ''

  # check if the directory path exists
  if not os.path.exists(directory_path):
    logger.error("The directory path does not exist")
    raise FileNotFoundError

  # open the directory in file explorer
  # os.startfile(directory_path)
  # disabled for replit


def check_list_files_exist_in_directory(directory_path: str,
                                        file_list: list) -> list:
  '''
  check if a list of files exist in a directory

  PARAMETERS
  ----------
  directory_path : str
  file_list : list
  
  RETURNS
  -------
  list of files that exist in the directory
  
  '''
  # check if the directory path exists
  if not os.path.exists(directory_path):
    logger.error("The directory path does not exist")
    raise FileNotFoundError

  # check if the file list is empty
  if len(file_list) == 0:
    logger.error("The file list is empty")
    raise ValueError

  fetch_list = []

  # check if the files exist
  for file in file_list:
    if not os.path.exists(os.path.join(directory_path, file)):
      fetch_list.append(file)

  return None if len(fetch_list) == 0 else fetch_list


def check_list_files_last_modified_in_directory(directory_path: str,
                                                file_list: list,
                                                last_modified: str = None
                                                ) -> list:
  '''
  check if a list of files have been modified in a directory

  PARAMETERS
  ----------
  directory_path : str
  file_list : list
  last_modified : str
  
  RETURNS
  -------
  list of files that have been modified in the directory
  
  '''
  # check if the directory path exists
  if not os.path.exists(directory_path):
    logger.error("The directory path does not exist")
    raise FileNotFoundError

  # check if the file list is empty
  if len(file_list) == 0:
    logger.error("The file list is empty")
    raise ValueError

  # check if the last modified is empty
  if last_modified is None:
    # get today's date
    last_modified = datetime.datetime.now()

  fetch_list = []

  # check if the files have been modified
  for file in file_list:
    if os.path.getmtime(os.path.join(directory_path, file)) > last_modified:
      fetch_list.append(file)

  return None if len(fetch_list) == 0 else fetch_list
