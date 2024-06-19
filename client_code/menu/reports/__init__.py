from ._anvil_designer import reportsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class reports(reportsTemplate):
  def __init__(self, **properties):
    all_rows = app_tables.quizzes.search()
    
    # Filter the rows where "reports" is more than 0
    reports = [row for row in all_rows if row['reports'] > 0]
    self.repeating_panel_1.items = reports
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.admindash')

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.activitydash')

  def button_2_copy_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("menu.admfeedback")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass

  def buttonlog_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('menu')
