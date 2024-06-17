from ._anvil_designer import stufeedbackTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class stufeedback(stufeedbackTemplate):
  def __init__(self,classid, **properties):
    self.classid=classid
    # Set Form properties and Data Bindings.
    self.user = anvil.users.get_user()["username"]
    userfeedback = app_tables.feedback.search(classcode=self.classid,student=self.user)
    self.repeating_panel_1.items = userfeedback
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    app_tables.feedback.add_row(classcode=self.classid,
                               content=None,
                               student=self.user,
                               response=None)
    self.repeating_panel_1.items = app_tables.feedback.search(classcode=self.classid,student=self.user)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage',self.classid)
