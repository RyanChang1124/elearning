from ._anvil_designer import classcreationTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class classcreation(classcreationTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.drop_down_1.items = [(str(row['lvlfactor']), row) for row in app_tables.levelfactor.search()]
    self.init_components(**properties)
    
    
    # Any code you write here will run before the form opens.

  def get_next_classcode(self):
      # Get all rows from the 'classrooms' table
      classrooms = app_tables.classrooms.search()
  
      # Get the highest current classcode
      max_classcode = max([classroom['classcode'] for classroom in classrooms], default=0)
  
      # Return one more than the highest current classcode to avoid duplication
      return max_classcode + 1

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('lecpage')

  def createclass_click(self, **event_args):
    self.createclass.visible = False
    """This method is called when the button is clicked"""
    value = self.drop_down_1.selected_value['lvlfactor']
    basevalue = self.basevalue.text
    app_tables.classrooms.add_row(classroom=self.classname.text,
                                 classcode=self.get_next_classcode(),
                                 baselevel=basevalue,
                                 levelincrement=value,
                                 username=anvil.users.get_user()['username'],
                                 lectname=anvil.users.get_user()['name'],
                                 email=anvil.users.get_user()['email'])
    open_form('lecpage')
