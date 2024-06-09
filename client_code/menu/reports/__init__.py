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
    # Set Form properties and Data Bindings.
    reports = app_tables.quizzes.search(reports=anvil.tables.number_greater_than(0))
    
    # Set the items of the RepeatingPanel
    self.repeating_panel_1.items = reports
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
