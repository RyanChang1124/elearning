from ._anvil_designer import materialviewTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class materialview(materialviewTemplate):
  def __init__(self,materialid, **properties):
    # Set Form properties and Data Bindings.
    self.materiallist = app_tables.materials.get(materialcode=materialid)
    self.init_components(**properties)
    if self.materiallist['checkpoint'] is not None:
     self.outlined_card_3.visible = True
    if self.materiallist['attachment'] is not None:
      self.outlined_button_1.visible = True
      self.outlined_button_1.text = f"Download attachment: {self.materiallist['attachment'].name}"
    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    anvil.media.download(self.materiallist['attachment'])
    """This method is called when the button is clicked"""

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage.classroompage.materials',classid = self.materiallist['classcode'])

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage.classroompage.quizprep',self.materiallist['checkpoint'],anvil.users.get_user()['username'])
