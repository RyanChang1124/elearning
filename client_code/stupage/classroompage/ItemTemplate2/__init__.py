from ._anvil_designer import ItemTemplate2Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.tz

now = datetime.now(anvil.tz.tzlocal())


class ItemTemplate2(ItemTemplate2Template):
  def __init__(self, **properties):
    global now
    global avail
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    codenow = int(self.item['quizcode'])
    if app_tables.quizresult.get(quizcode=codenow,student=anvil.users.get_user()['username']):     
      avail = "Complete"
      self.enterquiz.text = "Results"
    elif self.item['endtime'] <= now:
      self.enterquiz.text = "Overdue"
    else:
      avail="Yes"

    # Any code you write here will run before the form opens.

  def enterquiz_click(self, **event_args):
    global avail
    """This method is called when the button is clicked"""
    if self.enterquiz.text == "Begin Attempt":
      open_form('stupage.classroompage.quizprep',self.item['quizcode'],anvil.users.get_user()['username'])
    elif self.enterquiz.text == "Overdue":
      alert("Quiz is overdue!")
    elif self.enterquiz.text == "Results":
      pass
      