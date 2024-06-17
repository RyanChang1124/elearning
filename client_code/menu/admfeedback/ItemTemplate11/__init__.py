from ._anvil_designer import ItemTemplate11Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate11(ItemTemplate11Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def check_box_1_change(self, **event_args):
    """This method is called when this checkbox is checked or unchecked"""
    self.item['viewed'] = self.check_box_1.checked
