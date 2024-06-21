from ._anvil_designer import checkTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class check(checkTemplate):
  def __init__(self,quizid, **properties):
    self.quizcode = quizid
    self.label_1.text = app_tables.quizzes.get(quizcode=quizid)['quizname']
    # Set Form properties and Data Bindings.
    self.repeating_panel_1.items = app_tables.quizcontent.search(quizcode=quizid)
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    rows = app_tables.quizcontent.search(quizcode=self.quizcode)
    for row in rows:
        row.delete()
    rows = app_tables.quizzes.search(quizcode=self.quizcode)
    for row in rows:
        row.delete()
    rows = app_tables.quizresult.search(quizcode=self.quizcode)
    for row in rows:
        row.delete()
    open_form('menu.reports')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    target = app_tables.quizzes.get(quizcode=self.quizcode)
    target.update(reports=0)
    open_form('menu.reports')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.reports')
