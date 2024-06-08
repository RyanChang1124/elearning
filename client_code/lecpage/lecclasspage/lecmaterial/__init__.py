from ._anvil_designer import lecmaterialTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
classnow = None

class lecmaterial(lecmaterialTemplate):
  def __init__(self,classid, **properties):
    global classnow
    classnow = classid
    material = app_tables.materials.search(tables.order_by("postdate",ascending=False),classcode=classnow)
    self.repeating_panel_1.items = material
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    global classnow
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage.lecmaterial.editmaterial',classnow,0)

  def outlined_button_1_click(self, **event_args):
    global classnow
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage.lecmaterial.resultsboard_copy',classnow)


