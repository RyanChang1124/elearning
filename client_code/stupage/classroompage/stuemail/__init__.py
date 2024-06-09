from ._anvil_designer import stuemailTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class stuemail(stuemailTemplate):
  def __init__(self,classid, **properties):
    # Set Form properties and Data Bindings.
    self.classid = classid
    self.init_components(**properties)
    self.lectdata = app_tables.classrooms.get(classcode=classid)
    self.label_4.text = self.lectdata['lectname']
    # Any code you write here will run before the form opens.

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.subject.text is not None and self.body.text is not None:
      c = confirm("Is this email complete?")
      if c is False:
        exit()
      if c is True:
        anvil.server.call('sendlectemail',self.lectdata['email'],self.subject.text,self.body.text)
        alert("Email Sent!")
        open_form('stupage.classroompage',self.classid)
    else:
      alert("One or more fields are empty!")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage.classroompage',self.classid)

  