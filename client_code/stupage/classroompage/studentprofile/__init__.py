from ._anvil_designer import studentprofileTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import math 
classnow = None

class studentprofile(studentprofileTemplate):
  def __init__(self,classid, **properties):
    global classnow
    classnow = classid
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.student = app_tables.studentsclasses.get(student=(anvil.users.get_user()['username']),classcode=classid)
    self.classinfo = app_tables.classrooms.get(classcode=classid)
    self.namebar.text = anvil.users.get_user()['name']
    self.userbar.text = self.student['student']
    self.quizcompletebar.text = self.student['completedquiz']
    self.totalpointbar.text = self.student['totalpoints']
    self.label_7.text = self.student['exp']
    self.label_8.text = self.student['level']
    self.label_9.text = round(self.classinfo['baselevel']+(self.student['level']*self.classinfo['levelincrement']))
    if self.student['perk'] == 'time':
      self.image_2.source = "_/theme/icons8-time-100.png"
      self.label_3.text = "Extra Time"
      self.label_10.text = "You gain extra time for each question."
    if self.student['perk'] == 'conf':
      self.image_2.source = "_/theme/icons8-fast-forward-100.png"
      self.label_3.text = "Points Streak"
      self.label_10.text = "If you answer questions correctly \n back to back, you gain extra score."
    if self.student['perk'] == 'chance':
      self.image_2.source = "_/theme/icons8-retry-100.png"
      self.label_3.text = "Second Chance"
      self.label_10.text = "There is a slight chance to retry\n a question you answered wrongly."
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classnow
    open_form('stupage.classroompage',classid = classnow)

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.student['exp'] >= round(self.classinfo['baselevel']*self.student['level']*self.classinfo['levelincrement']) and self.student['level'] < 10:
      self.student['level'] += 1
      self.student['exp'] -= round(self.student['level']*self.classinfo['baselevel']*self.classinfo['levelincrement'])
      self.label_7.text = self.student['exp']
      self.label_8.text = self.student['level']
      self.label_9.text = round(self.classinfo['baselevel']*self.classinfo['baselevel']+(self.student['level']*self.classinfo['levelincrement']))
    elif self.student['exp'] < round(self.student['level']*self.classinfo['levelincrement']):
      alert("You do not have enough points!")
    elif self.student['level'] >= 10:
      alert("You are at the maximum level!")

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('menu')
      
