import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import pandas as pd
# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
import datetime

@anvil.server.callable
def get_current_time():
    return datetime.datetime.now().timestamp()
  
@anvil.server.callable
def metricdateincrement():
  dates = [r['date'] for r in app_tables.metrics.search()]
  today = pd.to_datetime('today')
  today = today.date()
  print(today)
  if today in dates:
    metric = app_tables.metrics.get(date=today)
    metric['NumberOfLogins'] += 1
  else:
    app_tables.metrics.add_row(
    date=today,
    NumberOfLogins= 1)

@anvil.server.callable
def checkvalueusers(value):
  return [r[value] for r in app_tables.users.search()]
@anvil.server.callable

def newuservalue(column,value):
  anvil.users.get_user()[column] = value

@anvil.server.callable
def returnclassname(classcode):
  class_row = app_tables.classrooms.get(classcode=classcode)
  if class_row is not None:
      # Get the class name
      class_name = class_row['classroom']
      return class_name

@anvil.server.callable
def getclasses(student_username):
    # Get the username for the student
    user_row = anvil.users.get_user()['username']
    
    # Get the enrollments for the student
    enrollments = app_tables.studentsclasses.search(student=user_row)
    
    classes = []
    for enrollment in enrollments:
        # Get the classcode from the enrollment
        classcode = enrollment['classcode']
        
        # Get the corresponding classroom
        classroom_row = app_tables.classrooms.get(classcode=classcode)
        
        if classroom_row is not None:
            # Get the classroom name and lecturer username
            classroom_name = classroom_row['classroom']
            lecturer_username = classroom_row['username']
            class_code = classroom_row['classcode']
            
            # Add the classroom information to the list
            classes.append({'classroom': classroom_name, 'lecturer': lecturer_username, 'classcode': class_code})
    
    return classes

@anvil.server.callable
def getlectclasses(lecturer_username):
    # Get the username for the lecturer
    user_row = anvil.users.get_user()['username']
    
    # Get the enrollments for the student
    enrollments = app_tables.classrooms.search(username=user_row)
    
    classes = []
    for enrollment in enrollments:
        # Get the classcode from the enrollment
        classcode = enrollment['classcode']
        
        # Get the corresponding classroom
        classroom_row = app_tables.classrooms.get(classcode=classcode)
        
        if classroom_row is not None:
            # Get the classroom name and classroomocode
            classroom_name = classroom_row['classroom']
            class_code = classroom_row['classcode']
            
            # Add the classroom information to the list
            classes.append({'classroom': classroom_name, 'classcode': class_code})
    
    return classes
    