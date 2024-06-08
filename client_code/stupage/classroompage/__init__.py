from ._anvil_designer import classroompageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
now = datetime.now()
classnow = None


class classroompage(classroompageTemplate):
  def __init__(self, classid, **properties):
      # Set Form properties and Data Bindings.
      global classnow
      classnow = classid
      quizzes = app_tables.quizzes.search(tables.order_by("endtime",ascending=False),classcode=classnow,available=True)
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

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('stupage')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classnow
    open_form('stupage.classroompage.materials',classid = classnow)
