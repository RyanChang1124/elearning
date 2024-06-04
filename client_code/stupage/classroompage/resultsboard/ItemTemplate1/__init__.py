from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    self.init_components(**properties)
    # Set Form properties and Data Bindings.
    if self.item['perk'] == 'time':
      self.image_1.source=anvil.URLMedia("_/theme/icons8-time-100.png")
    elif self.item['perk'] == 'conf':
      self.image_1.source=anvil.URLMedia("_/theme/icons8-fast-forward-100.png")
    elif self.item['perk'] == 'chance':
      self.image_1.source=anvil.URLMedia("_/theme/icons8-retry-100.png")

    # Any code you write here will run before the form opens.
