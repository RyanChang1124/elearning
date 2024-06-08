from ._anvil_designer import resultsboard_copyTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

classnow = None


class resultsboard_copy(resultsboard_copyTemplate):
  def __init__(self, quizid, classid, **properties):
    global classnow
    classnow = classid
    # Set Form properties and Data Bindings.
    rows = app_tables.quizresult.search(
      tables.order_by("points", ascending=False), quizcode=quizid
    )

    # Convert rows to a list so we can index it
    rows = list(rows)

    # Now 'rows' contains the leaderboard sorted by points in descending order
    self.repeating_panel_1.items = [
      {
        "rank": i + 1,
        "student": row["student"],
        "points": row["points"],
        "perk": row["perk"],
      }
      for i, row in enumerate(rows)
    ]
    self.init_components(**properties)
    self.label_7.text = app_tables.quizzes.get(quizcode=quizid)["quizname"]
    numofstudent = app_tables.studentsclasses.search(classcode=classnow)
    self.label_9.text = len(numofstudent)
    numofcompletions = app_tables.quizresult.search(quizcode=quizid)
    self.label_11.text = len(numofcompletions)
    aveaccu = sum([i['correctpercentage'] for i in numofcompletions])/len(numofcompletions)
    self.label_13.text = aveaccu
    # average_classcode = sum([material['classcode'] for material in materials]) / len(materials)
    # Any code you write here will run before the form opens.

  def outlined_button_1_click(self, **event_args):
    global classnow
    open_form('lecpage.lecclasspage', classid=classnow)
    """This method is called when the button is clicked"""
