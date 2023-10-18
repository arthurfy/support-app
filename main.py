import logging
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from pandasql import sqldf
from datetime import datetime, timedelta
from components.import_csv import import_csv
from components.common import common
from components.gui import gui
from components.login import login
from components.prep_data import prep_data
from components.visualise_data import visualise_data
from pandasql import sqldf

logger = common.logger


def section_collapse(layout, key, visible: bool = False):
  """
        Helper function that creates a column that can be later made hidden or visable
        """
  return sg.pin(sg.Column(layout, key=key, visible=visible))


def setup_database():
  '''
  setup the database
  '''
  # check if login.db exists
  if not os.path.exists("login.db"):
    # create the database
    login.create_database()
    login.add_user("admin", "admin")


setup_database()

menu_right_click = ['&Right', ['&Copy', '&Paste', '&Properties']]

main_menu = [['&File', ['&Exit']], ['&View', ['&Dashboard']],
             ['&Help', ['&About']]]

main_layout = [
    [sg.Menu(main_menu, key='-MENU-')],
    [section_collapse(gui.login_layout, '-LAYOUT-LOGIN-', True)],
    [section_collapse(gui.home_layout, '-LAYOUT-HOME-', False)],
    [sg.Canvas(key='-CANVAS-')],
    [sg.Exit()],
]

# Create the Window
window = sg.Window(
    'Data Application',
    main_layout,
    right_click_menu=menu_right_click,
    use_default_focus=False,
    finalize=True,
    element_justification='c',
)

customer_order_data = None
# Event Loop to process "events" and get the "values" of the inputs
while True:
  event, values = window.read()

  if event == "-LOGIN-BUTTON-":
    username = values["-LOGIN-USERNAME-"]
    password = values["-LOGIN-PASSWORD-"]

    if username != "" and password != "":
      if login(username, password):

        window['-LAYOUT-HOME-'].update(visible=True)
        window['-LAYOUT-LOGIN-'].update(visible=False)

        login.logged_in = True
        '''
        ON LOGIN, LOAD FIRST GRAPH
        '''

        # load customer order data
        customer_orders = prep_data.customer_orders()

        # limit records
        customer_orders = customer_orders.head(100)
        '''
        FILTE BY CUSTOMER ORDERS (DEV)
        '''

        # # filter customer orders by the last 12 months
        # today = datetime.date(datetime.now())
        # last_12_months = today - timedelta(days=365)
        # filter_query = f"""
        # SELECT * FROM customer_orders
        # where OrderDate >= {last_12_months}
        # """
        # customers_orders = sqldf(filter_query)

        customer_ids = customer_orders["CustomerID"].tolist()
        product_ids = customer_orders["ProductID"].tolist()

        visualise_data.draw_figure(
            window['-CANVAS-'].TKCanvas,
            visualise_data.create_scatter_graph(customer_ids, product_ids,
                                                "Customers VS Products"))

      else:
        sg.popup_ok("The username or password is incorrect")
    else:
      sg.popup_ok("The username or password cannot be blank")

    if event == "About":
      sg.popup("This is awesome!")

  if event == "API":

    if login.logged_in == True:

      try:

        gui.open_api_to_window("https://jsonplaceholder.typicode.com/todos")

      except Exception as e:
        logger.error(f"API: {e}")
    else:
      sg.popup_ok("You must login to import an api")

  if event == "About":
    sg.popup("This application is awesome!")

  if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Exit':  # if user closes window or clicks cancel
    break

window.close()
