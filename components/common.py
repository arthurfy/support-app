import os
import sys
import logging
import datetime

'''
Setup application logging
'''

logging.basicConfig(filemode='app.log',
                    format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

'''
Set application path
'''

def application_path():
  '''
  calculated the application path
  useful / required when running from an executable
  '''
  if getattr(sys, 'frozen', False):
    bundle_dir = sys._MEIPASS
    return bundle_dir
  else:
    bundle_dir = os.getcwd()
    return bundle_dir

'''
Setup common application paths
'''

APP_PATH = application_path()
DATA_FOLDER = os.path.join(APP_PATH, "data")
WORKSPACE_FOLDER = os.path.join(APP_PATH, "workspace")
CUSTOMERS = os.path.join(DATA_FOLDER, 'customers.csv')
ORDER_DETAILS = os.path.join(DATA_FOLDER, 'order_details.csv')
ORDERS = os.path.join(DATA_FOLDER, 'orders.csv')
PRODUCTS = os.path.join(DATA_FOLDER, 'products.csv')

'''
GUIDE MESSAGE
'''

application_version = "V0.1.0"
function_customers_message = "Customers:\nTop products"
function_api_message = "API:\nSimple api request"
home_guide_message = f"{application_version}\nPlease select a function from the menu\n\n{function_customers_message}\n\n{function_api_message}"
