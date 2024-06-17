from ._anvil_designer import newpageTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import time
newusername = None
newrole = None
newname = None



  

class newpage(newpageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    global newusername
    checkusername = self.outlined_1.text
    usernames = anvil.server.call('checkvalueusers','username')
    if checkusername in usernames:
      alert("This username is already in use!")
    else:
      try:
        self.outlined_card_1.visible = False
        self.outlined_card_2.visible = True
        newusername = checkusername
      except ValueError:
        alert("Something went wrong, try again?")

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    global newname
    checkname = self.outlined_2.text
    try:
      newname = checkname
      self.outlined_card_2.visible = False
      self.outlined_card_3.visible = True
    except ValueError:
      alert("Something went wrong, try again?")

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    global newrole
    global newname
    global newusername
    newrole = 'Student'
    anvil.server.call('newuservalue','role','Student')
    anvil.server.call('newuservalue','username',newusername)
    anvil.server.call('newuservalue','name',newname)
    anvil.server.call('newuservalue','setup_complete',True)
    newrole = 'Student'
    self.outlined_card_3.visible = False
    self.outlined_card_4.visible = True
    time.sleep(2)
    open_form('stupage')
    
  def outlined_button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    global newrole
    global newname
    global newusername
    newrole = 'Student'
    anvil.server.call('newuservalue','role','Lecturer')
    anvil.server.call('newuservalue','username',newusername)
    anvil.server.call('newuservalue','name',newname)
    anvil.server.call('newuservalue','setup_complete',True)
    newrole = 'Lecturer'
    self.outlined_card_3.visible = False
    self.outlined_card_4.visible = True
    time.sleep(2)
    open_form('lecpage')
