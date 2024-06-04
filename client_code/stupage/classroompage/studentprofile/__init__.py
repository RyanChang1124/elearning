from ._anvil_designer import studentprofileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
classnow = None

class studentprofile(studentprofileTemplate):
  def __init__(self,classid, **properties):
    global classnow
    classnow = classid
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.student = app_tables.studentsclasses.get(student=(anvil.users.get_user()['username']))
    self.namebar.text = anvil.users.get_user()['username']
    self.userbar = self.student['student']
    self.quizcompletebar = self.student['completedquiz']
    self.totalpointbar = self.student['exp']
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classnow
    open_form('stupage.classroompage',classid = classnow)
