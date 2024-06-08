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

class quizedit(quizeditTemplate):
  def __init__(self,quizid,classid, **properties):
    global quizcode
    self.uploaded_file = None
    if quizid == 0:
      quizcode = self.get_next_quizcode()
      app_tables.quizzes.add_row(quizcode=quizcode,
                                classcode=classid,
                                available=False,
                                lecturer=anvil.users.get_user()['username'],
                                quizname= "NewQuiz")
      self.qnum.text = 1
      quizcon = None
      self.repeating_panel_1.items = quizcon
    else:
      quizmeta = app_tables.quizzes.get(quizcode=quizid)
      self.quizname.text = quizmeta['quizname']
      self.date_picker_1.date = quizmeta['endtime']
      quizcon = app_tables.quizcontent.search(quizcode = quizid)
      self.repeating_panel_1.items = quizcon
    self.repeating_panel_1.add_event_handler('x-newqedit', self.newq)
    self.repeating_panel_1.add_event_handler('x-delnum', self.delnum)
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.drop_down_1.items = ['a', 'b', 'c', 'd']
    dropdown = [(str(row['questionnum']), row['questionnum']) for row in app_tables.quizcontent.search(quizcode=quizcode)]
    dropdown.append(("New", "New"))
    self.qnum.items = dropdown
    # Any code you write here will run before the form opens.

  def get_next_quizcode(self):
      # Get all rows from the 'quizzes' table
    quizzes = app_tables.quizzes.search()
    
    # Get the highest current quizcode
    max_quizcode = max([quiz['quizcode'] for quiz in quizzes], default=0)
    
    # Return one more than the highest current quizcode to avoid duplication
    return max_quizcode + 1

  def get_next_num(self):
      # Get all rows from the 'classrooms' table
      quizzes = app_tables.quizcontent.search()

      # Get the highest current questionnum
      max_quizcode = max([quiz['questionnum'] for quiz in quizzes], default=0)
  
      # Return one more than the highest current classcode to avoid duplication
      return max_quizcode + 1

  def newq(self, **event_args):
    global quizcode
    quesnum = event_args['qnum']
    self.qnum.selected_value = event_args['qnum']
    quescontent = app_tables.quizcontent.get(questionnum=quesnum,quizcode=quizcode)
    self.drop_down_1.selected_value = quescontent['answer']
    self.Questionprompt.text = quescontent['question']
    self.image_1.source = quescontent['image']
    self.a.text = quescontent['optiona']
    self.b.text = quescontent['optionb']
    self.c.text = quescontent['optionc']
    self.d.text = quescontent['optiond']
    self.score.text = quescontent['questionweight']
    self.time.text = quescontent['time']

  def submit_click(self, **event_args):
    global quizcode
    quesnum = self.qnum.selected_value
    """This method is called when the button is clicked"""
    
    if quesnum != "New":
      uprow =app_tables.quizcontent.get(quizcode=quizcode,questionnum=quesnum)
      uprow.update(answer=self.drop_down_1.selected_value,
                  question=self.Questionprompt,
                  image=self.image_1.source,
                  optiona=self.a.text,
                  optionb=self.b.text,
                  optionc=self.c.text,
                  optiond=self.d.text,
                  questionweight=self.score.text,
                  time=self.time.text)
      if self.uploaded_file is not None:
        uprow.update(image=self.uploaded_file)
      quizcon = app_tables.quizcontent.search(quizcode = quizcode)
      self.repeating_panel_1.items = quizcon
      dropdown = [(str(row['questionnum']), row['questionnum']) for row in app_tables.quizcontent.search(quizcode=quizcode)]
      dropdown.append(("New", "New"))
      self.qnum.items = dropdown
    else:
      newnum = self.get_next_num()
      app_tables.quizcontent.add_row(quizcode=quizcode,questionnum=newnum
                  ,answer=self.drop_down_1.selected_value,
                  question=self.Questionprompt.text,
                  optiona=self.a.text,
                  optionb=self.b.text,
                  optionc=self.c.text,
                  optiond=self.d.text,
                  questionweight=self.score.text,
                  time=self.time.text)
      if self.uploaded_file is not None:
        uprow.update(image=self.uploaded_file)
      quizcon = app_tables.quizcontent.search(quizcode = quizcode)
      self.repeating_panel_1.items = quizcon
      dropdown = [(str(row['questionnum']), row['questionnum']) for row in app_tables.quizcontent.search(quizcode=quizcode)]
      dropdown.append(("New", "New"))
      self.qnum.items = dropdown

  def delnum(self, **event_args):
    quesnum = event_args['qnum']
    self.delete_and_reorder(quesnum)
    
  def delete_and_reorder(self,targetnum):
      # Get the row to delete
      global quizcode
      row_to_delete = app_tables.quizcontent.get(questionnum=targetnum,quizcode=quizcode)
  
      # Delete the row
      app_tables.quizcontent.delete(row_to_delete)
  
      # Get all remaining questions
      remaining_questions = app_tables.quizcontent.search(quizcode=quizcode)
  
      # Iterate over the remaining questions
      for question in remaining_questions:
          # If the question order is greater than the deleted order, decrement it
          if question['questionnum'] > targetnum:
              question['questionnum'] -= 1
              app_tables.quizcontent.update(question, questionnum=question['questionnum'])
      quizcon = app.tables.quizcontent.search(quizcode = quizcode)   
      self.repeating_panel_1.items = quizcon       

  def file_loader_1_change(self, file, **event_args):
        # This method is called when a file has been loaded into the FileLoader
        # Store the uploaded file in the variable
        self.uploaded_file = file
        self.image_1.source = file