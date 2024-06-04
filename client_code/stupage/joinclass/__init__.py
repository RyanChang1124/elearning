from ._anvil_designer import joinclassTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
code = None

class joinclass(joinclassTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage')

  def confirmation_click(self, **event_args):
    global code
    code = int(self.codehere.text)
    studentrows = app_tables.studentsclasses.search(student=anvil.users.get_user()['username'], classcode=code)
    classrows = app_tables.classrooms.search(classcode=code)
    # Check if any rows were returned
    if len(list(studentrows)) > 0:
      alert("You are already in this classroom!")     
    elif len(list(classrows)) > 0:
      self.outlined_card_2.visible = False
      self.perk.visible = True
    elif len(list(classrows)) == 0:
      alert("There is no such classroom")

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.initnewstudent("time")

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.initnewstudent("conf")

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    self.initnewstudent("Chance")
    
    
  def initnewstudent(self, newperk):
    studentuser = anvil.users.get_user()['username']
    app_tables.studentsclasses.add_row(student=studentuser,
                                          level=1,
                                          classcode=code,
                                          totalpoints=0,
                                          exp=0,
                                          completedquiz=0,
                                          studentsetup=True,
                                          perk=newperk)
    open_form('stupage')