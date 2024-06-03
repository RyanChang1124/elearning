from ._anvil_designer import classroompageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
classnow = None

class classroompage(classroompageTemplate):
  def __init__(self, classid, **properties):
      # Set Form properties and Data Bindings.
      global classnow
      classnow = classid
      quizzes = app_tables.quizzes.search(classcode=classnow)
      self.repeating_panel_1.items = quizzes
      self.init_components(**properties)
  
      # Any code you write here will run before the form opens.
      
  
      classroomname = anvil.server.call('returnclassname', classid)
      print(classroomname)
      self.classname.text = classroomname

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classnow
    open_form('stupage.classroompage.studentprofile',classid = classnow)
