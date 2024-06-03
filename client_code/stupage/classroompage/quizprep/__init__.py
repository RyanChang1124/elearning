from ._anvil_designer import quizprepTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
quizcodenum = None
user = None

class quizprep(quizprepTemplate):
  def __init__(self,quizcode,username, **properties):
    global quizcodenum 
    global user
    user = username
    quizcodenum = quizcode
    
    
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.
    quiznaming = app_tables.quizzes.get(quizcode=quizcodenum)['quizname']
    self.quizname.text = quiznaming
    self.questions = app_tables.quizcontent.search(quizcode=quizcode)
    numofq = len(self.questions)
    self.quiznum.text = numofq
  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.open_form('stupage.classroompage.QuizForm',quizcodenum,user)

  def outlined_button_1_click(self, **event_args):
    global quizcodenum
    """This method is called when the button is clicked"""
    classtoreturn = app_tables.quizzes.get(quizcode=quizcodenum)['classcode']
    open_form('stupage.classroompage',classtoreturn)
