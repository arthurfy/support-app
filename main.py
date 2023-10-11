import logging, os, sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import PySimpleGUI as sg

sys.path.append(os.getcwd())
from components import import_csv, common, gui, login, prep_data

logger = common.logger

logger.info("The application is running")


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

# sg.theme('DarkAmber')  # Add a touch of color

menu_right_click = ['&Right', ['&Copy', '&Paste', '&Properties']]

main_menu = [['&File', ['&Exit']], ['&Import', ['&API']],
             ['&View', ['&Customers', '&Orders', '&Products']],
             ['&Help', ['&About']]]

main_layout = [
    [sg.Menu(main_menu, key='-MENU-')],
    [section_collapse(gui.login_layout, '-LAYOUT-LOGIN-', False)],
    [section_collapse(gui.home_layout, '-LAYOUT-HOME-', True)],
]

# Create the Window
window = sg.Window('Data Application',
                   main_layout,
                   right_click_menu=menu_right_click,
                   use_default_focus=False,
                   element_justification='c')

customer_order_data = None
# Event Loop to process "events" and get the "values" of the inputs
while True:
  event, values = window.read()

  if event == "-LOGIN-BUTTON-":
    username = values["-LOGIN-USERNAME-"]
    password = values["-LOGIN-PASSWORD-"]

    if username != "" and password != "":
      if login.login(username, password):

        window['-LAYOUT-HOME-'].update(visible=True)
        window['-LAYOUT-LOGIN-'].update(visible=False)
        login.logged_in = True
        customer_order_data = prep_data.customer_orders()
        logger.info(f"customer_order_data: {customer_order_data})")

        dataSize = 1000

        # Make synthetic data:
        xData = np.random.randint(100, size=dataSize)
        yData = np.linspace(0, dataSize, num=dataSize, dtype=int)

        # Make and show plot
        plt.plot(xData, yData, '.k')
        plt.show()

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
