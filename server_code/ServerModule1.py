import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import pandas as pd
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def metricdateincrement():
  dates = [r['date'] for r in app_tables.metrics.search()]
  today = pd.to_datetime('today').normalize
  if today in dates:
    metric = app_tables.metrics.get(date=today)
    metric['NumberOfLogins'] += 1
  else:
    app_tables.metrics.add_row(
    date=today,
    NumberOfLogins= 1)

@anvil.server.callable
def checkvalueusers(value):
  return [r[value] for r in app_tables.users.search()]
@anvil.server.callable
def newuservalue(column,value):
  anvil.users.get_user()[column] = value