from ._anvil_designer import admfeedbackTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class admfeedback(admfeedbackTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.repeating_panel_1.items = app_tables.emails.search(tables.order_by('viewed', ascending=True))
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("menu.admindash")

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("menu.admfeedback")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("menu.reports")

  def buttonlog_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('menu')


