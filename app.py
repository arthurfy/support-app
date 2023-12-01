import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from pandasql import sqldf
from datetime import datetime, timedelta
from components import common
from components import app_gui
from components import connect_login
from components import connect_api
from components import prep_data
from components import visualise_data

logger = common.logger


def setup_database():
  '''
  setup the authentication database
  '''
  # Check if login.db exists
  if not os.path.exists("login.db"):

    # Create the database
    connect_login.create_database()

    # Create the admin user
    connect_login.add_user("admin", "admin")

setup_database()

def app():
    '''
    main application function
    '''

    sg.theme("GrayGrayGray")

    def login_check():
      '''
      check if the user is logged in
      '''

      if connect_login.logged_in == True:
        return True
      else:
        sg.popup("Please login")
        return False

    def section_collapse(layout, key, visible: bool = False):
      """
      Creates a simple gui column that can be later made hidden or visable

      PARAMETERS
      ----------
      layout : 
      key : 
      visible : boolean - true or false

      RETURNS
      -------
      sg.pin

      """
      return sg.pin(sg.Column(layout, key=key, visible=visible))

    menu_right_click = ['&Right', ['&Copy', '&Paste', '&Properties']]

    main_menu = [['&File', ['&Exit']], ['&Function', ['&Customers','API']],
                ['&Help', ['&About']]]

    main_layout = [
        [sg.Menu(main_menu, key='-MENU-')],
        [section_collapse(app_gui.login_layout, '-LAYOUT-LOGIN-', True)],
        [section_collapse(app_gui.home_layout, '-LAYOUT-HOME-', False)],
        [section_collapse(app_gui.customer_layout, '-LAYOUT-CUSTOMER-', False)],
        [section_collapse(app_gui.api_layout, '-LAYOUT-API-', False)],
        [sg.Exit()],
    ]

    # Create the Window
    window = sg.Window(
        'Support Application',
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

      '''
      LOGIN SCREEN
      '''
      if event == "-LOGIN-BUTTON-":
        username = values["-LOGIN-USERNAME-"]
        password = values["-LOGIN-PASSWORD-"]

        if username != "" and password != "":
          if connect_login.login(username, password):

            window['-LAYOUT-HOME-'].update(visible=True)
            window['-LAYOUT-LOGIN-'].update(visible=False)

            # if successful set logged in to true
            connect_login.logged_in = True

          else:
            sg.popup_ok("The username or password is incorrect")
        else:
          sg.popup_ok("The username or password cannot be blank")

        if event == "About":
          sg.popup("This is awesome!")

      '''
      FUNCTION - CUSTOMERS
      '''
      if event == "Customers":
        logger.info(f"{event}")

        logged_in = login_check()

        if logged_in:

          # hide views
          window['-LAYOUT-HOME-'].update(visible=False)
          window['-LAYOUT-LOGIN-'].update(visible=False)
          window['-LAYOUT-API-'].update(visible=False)

          # show views
          window['-LAYOUT-CUSTOMER-'].update(visible=True)

          # load customer order data
          customer_orders = prep_data.customer_orders()

          # calculate top products
          products = prep_data.dash_products(customer_orders)

          product_ids = products["ProductID"].tolist()
          orders = products["Orders"].tolist()

          visualise_data.draw_figure(
              window['-CUSTOMERS-CANVAS-'].TKCanvas,
              visualise_data.create_plot_graph(product_ids, orders,
                                                  "Top Products", "Product ID", "Orders"))
          
      if event == "API":
        logger.info(f"{event}")
        '''
        FUNCTION - API
        '''

        logged_in = login_check()

        if logged_in:

          # hide views
          window['-LAYOUT-HOME-'].update(visible=False)
          window['-LAYOUT-LOGIN-'].update(visible=False)
          window['-LAYOUT-CUSTOMER-'].update(visible=False)

          # show views
          window['-LAYOUT-API-'].update(visible=True)

      if event == "-FUNCTION-API-REQUEST-BUTTON-": 
          logger.info(f"{event}")
          
          try:
            user_api_url = values['-FUNCTION-API-REQUEST-URL-']

            if user_api_url == None:
              continue

            if user_api_url == "":
              continue

            api_response = connect_api.api_request(user_api_url)
            api_response_formatted = connect_api.api_response_converter(api_response, "json")

            app_gui.function_api_response_data.update(str(api_response_formatted))

          except Exception as error:
            sg.popup_error(f"Unable to retrieve data from API\n\n{error}")

      if event == "About":
        sg.popup("GITHUB: https://github.com/arthurfy/support-app")

      if event == sg.WIN_CLOSED or event == 'Cancel' or event == 'Exit':  # if user closes window or clicks cancel
        break

    window.close()

app()
