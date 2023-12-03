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

def open_window_with_dataframe(dataframe: pd.DataFrame):
  '''
  load the dataframe into a viewer
  '''

  table_headings = list(dataframe.columns)
  table_values = dataframe.values.tolist()

  table_element = sg.Table(values=table_values, headings=table_headings, max_col_width=25,
                    auto_size_columns=True,
                    # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                    display_row_numbers=True,
                    justification='center',
                    # num_rows=20,
                    alternating_row_color='lightblue',
                    key='-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only=False,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')

  layout = [
    [table_element],
  ]
  # create expandable window
  window = sg.Window('Datafrme Table',
                     layout,
                     resizable=True,
                     finalize=True,
                     element_justification='c')

  while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
      break

  window.close()

def open_window_with_table_from_dataframe(dataframe: pd.DataFrame):
  '''
  get pysimple gui table values from a dataframe

  PARAMETERS
  ----------
  dataframe : 

  RETURN
  ------
  gui_table_headings : 
  gui_table_values :

  '''

  if dataframe.empty:
    error_message = "dataframe is empty"
    raise ValueError(error_message)

  gui_table_headings = list(dataframe.columns)
  gui_table_values = dataframe.values.tolist()

  return None if len(gui_table_headings) == 0 else gui_table_headings, None if len(gui_table_values) == 0 else gui_table_values

def open_window_with_api_response(dataframe: pd.DataFrame):
  '''
  load the dataframe into a viewer
  '''

  api_response_headings = list(dataframe.columns)
  api_response_values = dataframe.values.tolist()

  api_response_table = sg.Table(values=api_response_values, headings=api_response_headings, max_col_width=25,
                    auto_size_columns=True,
                    # cols_justification=('left','center','right','c', 'l', 'bad'),       # Added on GitHub only as of June 2022
                    display_row_numbers=True,
                    justification='center',
                    # num_rows=20,
                    alternating_row_color='lightblue',
                    key='-FUNCTION-API-RESPONSE-TABLE-',
                    selected_row_colors='red on yellow',
                    enable_events=True,
                    expand_x=True,
                    expand_y=True,
                    vertical_scroll_only=False,
                    enable_click_events=True,           # Comment out to not enable header and other clicks
                    tooltip='This is a table')
  
  api_response_export = sg.Button('Export',key='-FUNCTION-API-RESPONSE-EXPORT-',size=(10, 1))

  layout = [
    [api_response_table],
    [api_response_export],

  ]

  # Create expandable window
  window = sg.Window('API Response',
                     layout,
                     resizable=True,
                     finalize=True,
                     element_justification='c')

  while True:
    event, values = window.read()

    if event == '-FUNCTION-API-RESPONSE-EXPORT-':
      '''
      export api response
      '''
      try:

        export_location = sg.popup_get_folder("Please select export location")
        if not os.path.exists(export_location):
          raise ValueError("Export location doesn't exist")

        export_file_name = sg.popup_get_text("Please enter a file name?")
        if export_file_name == None or export_file_name == "":
          raise ValueError("Export file name is empty")

        if not str(export_file_name).endswith(".xlsx"):
          export_file_name = export_file_name + ".xlsx"

        export_path = export_location + "/" + export_file_name

        if os.path.isfile(export_path):
          raise ValueError("File with that name already exists")
        
        dataframe.to_excel(f"{export_path}")

        sg.popup(f"File has been exported to:\n\n{export_location}")

      except Exception as error:
        sg.popup(f"Unable to export api response data due to error.\n\n{error}")

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

function_api_url_label = sg.Text('API URL', size=(10, 1))
function_api_url = sg.InputText("https://jsonplaceholder.typicode.com/posts", key='-FUNCTION-API-REQUEST-URL-', size=(50, 1))

function_api_key_label = sg.Text('API KEY', size=(10, 1))
function_api_key = sg.InputText("api_key", key='-FUNCTION-API-REQUEST-API-KEY-', size=(50, 1), disabled=True)

function_api_key_label = sg.Text('API KEY', size=(10, 1))
function_api_tls_on = sg.Radio("TLS", "api_options", key='tls_on', enable_events=False,default=False, disabled=True)
function_api_tls_off = sg.Radio("OFF", "api_options", key='tls_off', enable_events=False,default=True, disabled=True)


function_api_request = sg.Button('Request',key='-FUNCTION-API-REQUEST-BUTTON-',size=(10, 1))

api_layout = [
  [function_api_url_label, function_api_url],
  # [function_api_key_label, function_api_key],
  # [function_api_tls_off, function_api_tls_on],
  [function_api_request],
  ]








