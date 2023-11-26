import sys
import os
import re
import logging
import pandas as pd
import PySimpleGUI as sg
from datetime import datetime, timedelta
from components import connect_api
'''
the application gui components
'''
def open_target_dataframe_to_window(target_dataframe: pd.DataFrame):
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

def open_api_to_window(api_url: str = None):
  '''
        load api url into a viewer
        '''

  sg.theme("DarkBlue3")
  sg.set_options(font=("Courier New", 16))

  # create an input field for the api url
  api_url_label = sg.Text('API URL', size=(10, 1))
  api_url_text_box = sg.InputText(key='-API-REQUEST-URL-', size=(50, 1))
  api_url_button = sg.Button('Load API',
                             key='-API-REQUEST-BUTTON-',
                             size=(10, 1))
  api_url_response_data = sg.Multiline(key='api_url_response_large_text',
                                       size=(100, 20))

  # create layout for api
  api_layout = [[api_url_label, api_url_text_box, api_url_button],
                [api_url_response_data]]

  # create expandable window
  window = sg.Window('API Import',
                     api_layout,
                     resizable=True,
                     finalize=True,
                     element_justification='c')

  if api_url != None and api_url != "":
    api_url_text_box.update(api_url)

  while True:
    event, values = window.read()

    if event == '-API-REQUEST-BUTTON-':

      try:
        user_api_url = values['-API-REQUEST-URL-']
        if user_api_url != None and user_api_url != "":
          api_headers = connect_api.api_standard()
          api_request = connect_api.api_request(user_api_url,
                                               headers=api_headers)
          api_response = connect_api.api_response_to_dataframe(api_request)
          api_url_response_data.update(api_response.to_string())
      except Exception as e:
        sg.popup_error(f"Error: {e}\nUnable to retrieve data from API")

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

# GUI COMPONENTS
# notes_listbox = sg.Listbox(values=common.get_list_of_files_in_directory(
#     common.WORKSPACE_FOLDER),
#                            key="-WORKSPACE-FILES-",
#                            size=(20, 19))
# notes_large_text = sg.Multiline(key='notes_large_text', size=(100, 20))




'''
HOME LAYOUT
'''

customer_listbox = sg.Listbox(values=[], key="-CUSTOMERS-LIST-", size=(40, 10))
customer_search = sg.InputText('search customers',font=('Arial Bold', 12),  expand_x=True, enable_events=True,  readonly=False, size=(32,1), key='-CUSTOMER-SEARCH-')


customer_layout = [
  [customer_search],
  # [customer_listbox],
  [sg.Canvas(key='-CUSTOMERS-CANVAS-')],
]

'''
DASHBOARD LAYOUT
'''

dash_products = sg.Button('Products', key='-DASH-PRODUCTS-', size=(10, 1))
dash_orders = sg.Button('Orders', key='-DASH-ORDERS-', size=(10, 1))
dash_customers = sg.Button('Customers', key='-DASH-CUSTOMERS-', size=(10, 1))

dash_layout = [
    [dash_products, dash_orders, dash_customers],
]

'''
HOME LAYOUT
'''


home_button = sg.Button("Home", key="-HOME-BUTTON-",size=(10, 1))
home_guide_text = sg.Multiline("guide text here", key='-HOME-GUIDE-TEXT', size=(100, 20))

home_layout = [
  [home_guide_text],
]



