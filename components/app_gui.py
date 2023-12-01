import sys
import os
import pandas as pd
import PySimpleGUI as sg

try:
  from components import common
except ModuleNotFoundError as error:
  print(f"{error} from app_gui.py")
  sys.path.append(os.getcwd())
  from components import common

'''
the application gui components
'''

sg.theme("GrayGrayGray")

def open_window():
  '''
  open an additional window
  '''  
  window_layout = []

  # create expandable window
  window = sg.Window('new window',
                     window_layout,
                     resizable=True,
                     finalize=True,
                     element_justification='c')

  while True:
    event, values = window.read()

    if event == '-NEW-WINDOW-EVENT-':
      pass

    if event == "Exit" or event == sg.WIN_CLOSED:
      break

  window.close()

def open_target_with_dataframe(target_dataframe: pd.DataFrame):
  '''
  load the dataframe into a viewer
  '''

  headings = list(target_dataframe.columns)
  values = target_dataframe.values.tolist()

  sg.theme("DarkBlue3")
  sg.set_options(font=("Courier New", 16))

  layout = [[
      sg.Table(values=values,
               headings=headings,
               max_col_width=25,
               background_color='light blue',
               auto_size_columns=True,
               display_row_numbers=True,
               justification='right',
               num_rows=min(len(values), 20))
  ]]
  # create expandable window
  window = sg.Window('Viewer',
                     layout,
                     resizable=True,
                     finalize=True,
                     element_justification='c')

  while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
      break

  window.close()

'''
LOGIN LAYOUT
'''

login_text = sg.Text("Login", size=(20, 1))
login_username_input = sg.InputText("admin",
                                    key='-LOGIN-USERNAME-',
                                    size=(50, 1))
login_password_input = sg.InputText("admin",
                                    key='-LOGIN-PASSWORD-',
                                    size=(50, 1))
login_button = sg.Button('Login', key='-LOGIN-BUTTON-', size=(10, 1))

login_layout = [
    [login_text],
    [login_username_input],
    [login_password_input],
    [login_button],
]

'''
HOME LAYOUT
'''

home_button = sg.Button("Home", key="-HOME-BUTTON-",size=(10, 1))
home_guide_text = sg.Multiline(common.home_guide_message, key='-HOME-GUIDE-TEXT', size=(100, 20))

home_layout = [
  [home_guide_text],
]

'''
CUSTOMER LAYOUT
'''

customer_listbox = sg.Listbox(values=[], key="-CUSTOMERS-LIST-", size=(40, 10))
customer_search = sg.InputText('search customers',font=('Arial Bold', 12),  expand_x=True, enable_events=True,  readonly=False, size=(32,1), key='-CUSTOMER-SEARCH-')

customer_layout = [
  # [customer_search],
  # [customer_listbox],
  [sg.Canvas(key='-CUSTOMERS-CANVAS-')],
]

'''
API LAYOUT
'''

function_api_label = sg.Text('API URL', size=(10, 1))
function_api_url = sg.InputText("https://jsonplaceholder.typicode.com/posts", key='-FUNCTION-API-REQUEST-URL-', size=(50, 1))
function_api_request = sg.Button('Request',
                            key='-FUNCTION-API-REQUEST-BUTTON-',
                            size=(10, 1))
function_api_response_data = sg.Multiline(key='api_url_response_large_text',
                                      size=(100, 20))

# create layout for api
api_layout = [[function_api_label, function_api_url, function_api_request],
              [function_api_response_data]]








