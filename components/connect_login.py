import sqlite3
import logging
import hashlib
from components import common

logger = common.logger

# create login state
logged_in = False

# create a new sqlite database
def create_database():
  conn = sqlite3.connect('login.db')
  c = conn.cursor()

  # create a table
  c.execute("""CREATE TABLE IF NOT EXISTS user_credentials (
        username text,
        password text
    )""")

  conn.commit()
  conn.close()


# check if the user exists in the database
def check_user(username: str, password: str):
  conn = sqlite3.connect('login.db')
  c = conn.cursor()

  # create SHA256 hash of the password
  hashed_password = hashlib.sha256(password.encode()).hexdigest()

  # check if the user exists in the database
  c.execute(
      "SELECT * FROM user_credentials WHERE username = :username AND password = :password",
      {
          'username': username,
          'password': hashed_password
      })
  user = c.fetchone()

  conn.commit()
  conn.close()

  return user


# add a new user to the database
def add_user(username: str, password: str):
  conn = sqlite3.connect('login.db')
  c = conn.cursor()

  # create SHA256 hash of the password
  hashed_password = hashlib.sha256(password.encode()).hexdigest()

  # add a new user to the database
  c.execute("INSERT INTO user_credentials VALUES (:username, :password)", {
      'username': username,
      'password': hashed_password
  })

  conn.commit()
  conn.close()

  if check_user(username, password):
    logging.info(f"User {username} was added to the database")
    return True
  else:
    logging.info(f"User {username} was not added to the database")
    return False


# login to the application
def login(username: str, password: str):
  user = check_user(username, password)

  if user:
    logged_in = True
  else:
    logged_in = False

  return logged_in
