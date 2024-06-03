from ._anvil_designer import lecpageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class lecpage(lecpageTemplate):
  def __init__(self, **properties):
    lecturer_username = anvil.users.get_user('username')
    classes = anvil.server.call('getlectclasses', lecturer_username )
    self.repeating_panel_1.items = classes
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
