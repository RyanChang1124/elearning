from ._anvil_designer import lectemailTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class lectemail(lectemailTemplate):
  def __init__(self, classid, **properties):
    # Set Form properties and Data Bindings.
    self.classid = classid
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.subject.text is not None and self.body.text is not None:
      c = confirm("Is this email complete?")
      if c is False:
        exit()
      if c is True:
        app_tables.emails.add_row(body=self.body.text,subject=self.subject.text,sender=(anvil.users.get_user()["username"]),viewed=False)
        alert("Feedback Sent!")
    else:
      alert("One or more fields are empty!")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("lecpage.lecclasspage", self.classid)
