from ._anvil_designer import menuTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server

def loginadd():
  anvil.server.call('metricdateincrement')
class menu(menuTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.login_with_form()
    if anvil.users.get_user('email') is not None:
      loginadd()
    if anvil.users.get_user()['setup_complete'] is None:
      open_form('newpage')
    elif anvil.users.get_user()['setup_complete'] is True:
      if anvil.users.get_user()['role'] == 'Student':
        open_form('stupage')
      elif anvil.users.get_user()['role'] == 'Lecturer':
        open_form('lecpage')
      elif anvil.users.get_user()['role'] == 'Admin':
        open_form('menu.admindash')

  def button_5_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
