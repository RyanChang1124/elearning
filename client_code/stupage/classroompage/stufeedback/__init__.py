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
    # Set Form properties and Data Bindings.
    user = anvil.users.get_user()["username"]
    userfeedback = app_tables.ge
    self.repeating_panel_1.items = userfeedback
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
