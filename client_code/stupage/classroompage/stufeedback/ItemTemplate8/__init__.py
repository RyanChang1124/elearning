from ._anvil_designer import ItemTemplate8Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate8(ItemTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if self.response.text is None:
      self.response.text = "No Response Yet"
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.item['content'] = self.Subject.text
    alert("Feedback Saved!")

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    choice = confirm("Are you sure you want to delete this feedback form?",buttons=[("Yes","YES"),("No","NO")])
    if choice == "YES":
      self.item.delete()
      self.remove_from_parent()
