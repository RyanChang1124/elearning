from ._anvil_designer import quizeditTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class quizedit(quizeditTemplate):
  def __init__(self,classid,quizid, **properties):
    # Initialize components first
    self.init_components(**properties)
    self.quizcode = None

    self.classidnow = classid
    self.quizidnow = quizid
    self.quiz = None
    quiz_code = self.quizidnow
    if quiz_code == 0:  # New quiz
      self.quiz = app_tables.quizzes.add_row(
          quizcode=self.generate_quiz_code(),
          classcode=self.classidnow,
          quizname="",
          lecturer=anvil.users.get_user()['username'],
          endtime=None,
          available=False,
          reports=0,
      )
      self.quizidnow = self.quiz['quizcode']
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
    if self.quizname.text is not None and self.date_picker_1.date is not None:
      uprow = app_tables.quizzes.get(classcode=self.classidnow,quizcode=self.quizidnow)
      uprow.update(available=self.check_box_1.checked,
                  endtime=self.date_picker_1.date,
                  quizname=self.quizname.text,
                  lecturer=anvil.users.get_user()['username'])
      open_form('lecpage.lecclasspage',self.classidnow)
    else:
      alert("There are missing fields!")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage.lecclasspage',self.quiz['classcode'])

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm("Are you sure?")
    if c:
      rows = app_tables.quizcontent.search(quizcode=self.quizidnow)
      for row in rows:
          row.delete()
      rows = app_tables.quizzes.search(quizcode=self.quizidnow)
      for row in rows:
          row.delete()
      rows = app_tables.quizresult.search(quizcode=self.quizidnow)
      for row in rows:
          row.delete()
      open_form('lecpage.lecclasspage',self.classidnow)
