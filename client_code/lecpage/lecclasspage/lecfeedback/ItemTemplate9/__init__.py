from ._anvil_designer import ItemTemplate9Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate9(ItemTemplate9Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    try:
      self.item['response'] = self.response.text
      alert("Response Saved!")
    except:
      alert("There are invalid or missing fields!")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    pass
