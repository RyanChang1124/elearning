from ._anvil_designer import lecclasspageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
classcode = None

class lecclasspage(lecclasspageTemplate):
  def __init__(self,classid, **properties):
    global classcode
    classcode = classid
    # Set Form properties and Data Bindings.
    self.label_3.text = app_tables.classrooms.get(classcode=classid)['classroom']
    global classnow
    classnow = classid
    quizzes = app_tables.quizzes.search(tables.order_by("endtime",ascending=False),classcode=classnow)
    self.repeating_panel_1.items = quizzes
    self.init_components(**properties)
    

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    global classcode
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage.quizedit', classcode,0 )

  def log_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('menu')
      
