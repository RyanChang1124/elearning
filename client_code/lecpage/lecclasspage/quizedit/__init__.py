from ._anvil_designer import quizeditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
quizcode = None
classidnow = None
quizidnow = None
class quizedit(quizeditTemplate):
  def __init__(self,classid,quizid, **properties):
    global classidnow
    global quizidnow
    # Initialize components first
    self.init_components(**properties)

    classidnow = classid
    quizidnow = quizid
    self.quiz = None
    quiz_code = quizidnow
    if quiz_code == 0:  # New quiz
      self.quiz = app_tables.quizzes.add_row(
          quizcode=self.generate_quiz_code(),
          classcode=classidnow,
          quizname="",
          lecturer="",
          endtime=None,
          available=False
      )
    else:  # Existing quiz
        self.quiz = app_tables.quizzes.get(quizcode=quiz_code)
        if self.quiz is not None:
            self.quizname.text = self.quiz['quizname']
            self.date_picker_1.date = self.quiz['endtime']
            self.load_questions()
        else:
            alert("No quiz found with the given code.")
    
    
     

  def generate_quiz_code(self):
    max_quiz_code = max((qu['quizcode'] for qu in app_tables.quizzes.search()), default=0)
    return max_quiz_code + 1

  def load_questions(self):
    questions = app_tables.quizcontent.search(quizcode=self.quiz['quizcode'])
    self.repeating_panel_1.items = questions
    
  def button_add_question_click(self, **event_args):
    """This method is called when the button is clicked"""
    app_tables.quizcontent.add_row(
        quizcode=self.quiz['quizcode'],
        questionnum=self.generate_question_num(),
        question="",
        optiona="",
        optionb="",
        optionc="",
        optiond="",
        image=None,
        answer="",
        time=30,
        questionweight=30
    )
    self.load_questions()

  def generate_question_num(self):
    max_question_num = max((qu['questionnum'] for qu in app_tables.quizcontent.search(quizcode=self.quiz['quizcode'])), default=0)
    return max_question_num + 1

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classidnow
    global quizidnow
    uprow = app_tables.quizzes.get(classcode=classidnow,quizcode=quizidnow)
    uprow.update(available=self.check_box_1.checked,
                endtime=self.date_picker_1.date,
                quizname=self.quizname.text,
                lecturer=anvil.users.get_user()['username'])
    open_form('lecpage.lecclasspage',classidnow)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage',self.quiz['classcode'])
