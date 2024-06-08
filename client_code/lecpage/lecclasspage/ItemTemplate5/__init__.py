from ._anvil_designer import ItemTemplate5Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate5(ItemTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage.quizedit',self.item['classcode'],self.item['quizcode'])

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage.lecmaterial.resultsboard_copy',self.item['quizcode'],self.item['classcode'])
    
