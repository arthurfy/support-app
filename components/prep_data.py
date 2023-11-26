import os
import sys
import pandas as pd
from pandasql import sqldf

try:
  from components import import_csv_to_dataframe
  from components import logger, CUSTOMERS, ORDERS, ORDER_DETAILS, PRODUCTS
except ModuleNotFoundError:
  sys.path.append(os.getcwd())
  from components import import_csv_to_dataframe
  from components import logger, CUSTOMERS, ORDERS, ORDER_DETAILS, PRODUCTS


def customer_orders() -> pd.DataFrame:
  '''
  join customer and order data

  RETURN
  ------
  customer_orders : pd.DataFrame
  '''

  customers = import_csv_to_dataframe(CUSTOMERS)
  logger.info(f"loading customer data")
  logger.info(f"customer data shape: {customers.shape}")
  logger.info(f"customer data columns: {customers.columns}")

  orders = import_csv_to_dataframe(ORDERS)
  logger.info(f"loading order data")
  logger.info(f"order data shape: {orders.shape}")
  logger.info(f"order data columns: {orders.columns}")

  order_details = import_csv_to_dataframe(ORDER_DETAILS)
  logger.info(f"loading order details")
  logger.info(f"order details shape: {order_details.shape}")
  logger.info(f"order details columns: {order_details.columns}")

  products = import_csv_to_dataframe(PRODUCTS)
  logger.info(f"loading product data")
  logger.info(f"product data shape: {products.shape}")
  logger.info(f"product data columns: {products.columns}")

  customers_to_orders_query = """
  SELECT 
  customers.CustomerID, 
  customers.FirstName, 
  customers.LastName,
  customers.LoyaltyClubMember,
  customers.StateID, 
  orders.SalesOrderID,
  orders.OrderDate,
  orders.ShipDate,
  order_details.ProductID,
  order_details.UnitPrice,
  order_details.OrderQty, 
  products.Name,
  products.ListPrice,
  products.Cost
  FROM customers
  INNER JOIN orders
  ON customers.CustomerID = orders.CustomerID
  INNER JOIN order_details
  ON orders.SalesOrderID = order_details.SalesOrderID
  INNER JOIN products
  ON order_details.ProductID = products.ProductID;
  """

  customers_orders = sqldf(customers_to_orders_query)
  logger.info(f"customers_orders shape: {customers_orders.shape}")
  logger.info(f"customers_orders columns: {customers_orders.columns}")

  return customers_orders


def dash_products(customer_orders: pd.DataFrame) -> pd.DataFrame:
  '''
  filter top products from customer orders
  '''

  products_query = '''
  SELECT ProductID, COUNT(*) AS Orders
  FROM customer_orders
  GROUP BY ProductID
  ORDER BY Orders DESC
  LIMIT 10
  '''

  products = sqldf(products_query)

  return products


def dash_orders():
  '''
  filter order details from customer orders
  '''
  pass


def dash_customers():
  '''
  filter top customers from customer orders
  '''
  pass


if __name__ == "__main__":
  pass

  customer_orders = customer_orders()

  dash_products(customer_orders)
