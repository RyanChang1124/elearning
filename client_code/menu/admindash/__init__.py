from ._anvil_designer import admindashTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class admindash(admindashTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    total, students, lecturers = anvil.server.call('getmetrics')
    self.usercount.text = total
    self.stucount.text = students
    self.leccount.text = lecturers
    self.image_1.source = anvil.server.call('plotactive')
    # Any code you write here will run before the form opens.

  def button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('menu.activitydash')
