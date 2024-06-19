from ._anvil_designer import activitydashTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class activitydash(activitydashTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.image_1.source = anvil.server.call('plot_login_chart')
    self.image_2.source = anvil.server.call('plot_quizcomplete_chart')
    # Any code you write here will run before the form opens.

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.reports')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.admindash')

  def button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("menu.admfeedback")


  def buttonlog_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('menu')

