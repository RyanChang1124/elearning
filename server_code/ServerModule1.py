import anvil.email
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.server
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pytz
import io
import anvil.media
import psycopg2
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
@anvil.server.callable
def getawaredt():
    now = pd.Timestamp.now()
  
    # Make it timezone-aware
    aware_datetime = now.tz_localize('Asia/Kuala_Lumpur')  # Use your desired timezone
    
    return aware_datetime
  
@anvil.server.callable
def get_current_time():
    return datetime.datetime.now().timestamp()

@anvil.server.callable
def getmetrics():
  total = len(app_tables.users.search())
  students = len(app_tables.users.search(role='Student'))
  lecturers = len(app_tables.users.search(role='Lecturer'))
  return total, students, lecturers
'''
@anvil.server.callable
def getmetricsusers():
  conn = psycopg2.connect(anvil.tables.get_connection_string())
  with conn.cursor() as cur:
      cur.execute("SELECT * FROM users")
      total = len(cur)
  with conn.cursor() as cur:
      cur.execute("SELECT * FROM users WHERE role = 'Lecturer';")
      lecturers = len(cur)
  with conn.cursor() as cur:
      cur.execute("SELECT * FROM users WHERE role = 'student';")
      students = len(cur)
  return total, students, lecturers
'''
@anvil.server.callable
def plotactive():
    # get datetime
    now = datetime.now(pytz.utc)
    
    # get date from a month agao
    one_month_ago = now - timedelta(days=30)
    
    # Query for active users
    recent_users = app_tables.users.search(tables.order_by("last_login", ascending=False))
    recent_users = [user for user in recent_users if user['last_login'] > one_month_ago]
    
    # Query for all users
    all_users = app_tables.users.search()
    all_users = [user for user in all_users]
    
    # Calculate the number of users who have and haven't logged in within the last month
    logged_in = len(recent_users)
    not_logged_in = len(all_users) - logged_in
    
    # Plot
    fig, ax = plt.subplots()

    def value_and_percentage(val):
        total = sum([logged_in, not_logged_in])
        absolute = int(round(val*total/100.0))
        percentage = val
        return "{:.1f}%\n({:d})".format(percentage, absolute)
    ax.pie([logged_in, not_logged_in], labels=['Active', 'Inactive'], autopct=value_and_percentage)
    
    # Save to bytes.io
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    buf_bytes = buf.getvalue()
    
    # convert to an image
    return anvil.BlobMedia("image/png", buf_bytes, name="pie_chart.png")

@anvil.server.callable
def plot_login_chart():
    # Query the Logins table for all records
    logins = app_tables.metrics.search(tables.order_by("date"))
    
    # Extract the dates and number of logins
    dates = [record['date'] for record in logins]
    num_logins = [record['NumberOfLogins'] for record in logins]
    # Limit to the last 7 dates
    dates = dates[7:]
    num_logins = num_logins[7:]
    # Create a line plot
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(dates, num_logins)
    
    # Set the title and labels
    ax.set_title('Number of Logins this week')
    ax.set_xlabel('Date')
    ax.set_ylabel('Number of Logins')
    
    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert the BytesIO object to bytes
    buf_bytes = buf.getvalue()
    
    # Convert the bytes to an Anvil Media object and return it
    return anvil.BlobMedia("image/png", buf_bytes, name="login_chart.png")

@anvil.server.callable
def plot_quizcomplete_chart():
    # Query the Logins table for all records
    logins = app_tables.metrics.search(tables.order_by("date"))
    
    # Extract the dates and number of logins
    dates = [record['date'] for record in logins]
    num_quiz = [record['quizzescomplete'] for record in logins]
    # Limit to the last 7 dates
    dates = dates[7:]
    num_quiz = num_quiz[7:]
    # Create a line plot
    fig, ax = plt.subplots(figsize = (10,5))
    ax.plot(dates, num_quiz)
    
    # Set the title and labels
    ax.set_title('Number of Completed Quizzes this week')
    ax.set_xlabel('Date')
    ax.set_ylabel('COmpleted Quizzes')
    
    # Save the figure to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Convert the BytesIO object to bytes
    buf_bytes = buf.getvalue()
    
    # Convert the bytes to an Anvil Media object and return it
    return anvil.BlobMedia("image/png", buf_bytes, name="quiz_chart.png")

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
def sendlectemail(email,sub,body):
  anvil.email.send(from_name = anvil.users.get_user()['name'], 
                    to = email,
                    subject = sub,
                    text = body)

@anvil.server.callable
def sendadminemail(sub,body):
  anvil.email.send(from_name = anvil.users.get_user()['name'], 
                    to = 'qlearnadmin@gmail.com',
                    subject = sub,
                    text = body)

@anvil.server.callable
def quizzesincrement():
  dates = [r['date'] for r in app_tables.metrics.search()]
  today = pd.to_datetime('today')
  today = today.date()
  print(today)
  metric = app_tables.metrics.get(date=today)
  if today in dates:
    if metric['quizzescomplete'] is not None:    
      metric['quizzescomplete'] += 1
    else:
      metric['quizzescomplete'] = 1



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
    name = anvil.users.get_user()['username']
    
    # Get the enrollments for the student
    # enrollments = app_tables.classrooms.search(username=user_row)
    
    classes = []
    
    # Get the corresponding classroom
    classroom_row = app_tables.classrooms.search(username=name)
    for i in classroom_row:
      if i is not None:
          # Get the classroom name and classroomocode
          classroom_name = i['classroom']
          class_code = i['classcode']
          
          # Add the classroom information to the list
          classes.append({'classroom': classroom_name, 'classcode': class_code})
    
    return classes

@anvil.server.http_endpoint('/receive_email')
def receive_email(**params):
    # Assuming 'params' contains the email data
    sender = params.get('from')
    subject = params.get('subject')
    body = params.get('body')
    app_tables.emails.add_row(body=body,sender=sender,viewed=False,subject=subject)