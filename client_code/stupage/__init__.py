from ._anvil_designer import stupageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

 
class stupage(stupageTemplate):
  def __init__(self, **properties):
    # Any code you write here will run before the form opens.
    student_username = anvil.users.get_user()['username']
    classes = anvil.server.call('getclasses', student_username )
    print(classes)
    self.repeating_panel_1.items = classes
    print(student_username)
    self.student.text = (f'Welcome back, {student_username}.')
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage.joinclass')
    

    