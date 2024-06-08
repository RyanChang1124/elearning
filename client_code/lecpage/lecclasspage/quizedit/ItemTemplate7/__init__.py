from ._anvil_designer import ItemTemplate7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class ItemTemplate7(ItemTemplate7Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings
    self.init_components(**properties)

  def button_save_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.item['question'] = self.text_box_question.text
      self.item['optiona'] = self.text_box_optiona.text
      self.item['optionb'] = self.text_box_optionb.text
      self.item['optionc'] = self.text_box_optionc.text
      self.item['optiond'] = self.text_box_optiond.text
      self.item['answer'] = self.drop_down_answer.selected_value
      self.item['time'] = int(self.numeric_box_time.text)
      self.item['questionweight'] = int(self.numeric_box_questionweight.text)
      if self.file_loader_1.file:
          self.item['image'] = self.file_loader_1.file
      self.item.update()
    
  # Any code you write here will run before the form opens.

  def text_box_question_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass


