from ._anvil_designer import QuizFormTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

import math
import random
import time

class QuizForm(QuizFormTemplate):
    def __init__(self, quizcode, studentid, **properties):
        self.numofq = None
        self.correctq = 0
        self.quizcoderem = None
        self.quizcoderem = quizcode
        # Set Form properties and Data Bindings.
        self.init_components(**properties)
        self.metadata = app_tables.quizzes.get(quizcode=quizcode)
        # Retrieve the quiz data
        self.questions = app_tables.quizcontent.search(quizcode=quizcode)
        self.numofq = len(self.questions)
        # Initialize the score and the streak of correct answers
        self.score = 0
        self.correct_streak = 0

        # Retrieve the student's perk
        self.student = app_tables.studentsclasses.get(student=studentid,classcode=self.metadata['classcode'])
        self.user.text = self.student['student']
        self.perk = self.student['perk']
        self.level = self.student['level']
        if self.student['perk'] == "time":
          self.image_4.source = "_/theme/icons8-time-100.png"
          self.label_1.text = "Extra Time"
        elif self.student['perk'] == "conf":
          self.image_4.source = "_/theme/icons8-fast-forward-100.png"
          self.label_1.text = "Point Streak"
        elif self.student["perk"] == "chance":
          self.image_4.source = "_/theme/icons8-retry-100.png"
          self.label_1.text = "Second Chance"

        # Start the quiz
        self.current_question_index = 0
        self.display_question()

    def display_question(self):
        # Display the current question
        question = self.questions[self.current_question_index]
        self.question_label.text = question['question']
        self.option_a.text = question['optiona']
        self.option_b.text = question['optionb']
        self.option_c.text = question['optionc']
        self.option_d.text = question['optiond']
        if question['image'] is not None:
          self.outlined_card_3.visible = True
          self.image_1.source = question['image']
        else:
          self.outlined_card_3.visible = False 

        # Start the timer
        time = question['time']
        if self.perk == 'time':
            # The student has the 'time' perk, so increase the time by a certain amount
            time = time * (1+(0.1 * self.level)) 
            time = round(time)
        self.time_remaining = time
        self.timeleft.text = str(self.time_remaining)
        self.start_time = self.time_remaining
        self.timer_1.interval = 1
        self.timer_1.enabled = True

    def timer_1_tick(self, **event_args):
        """This method is called every [interval] seconds. Does not trigger if [interval] is 0."""
        # The timer ran out before the user answered the question
        self.time_remaining -= 1
        print(self.time_remaining)
        self.timeleft.text = str(self.time_remaining)  # Update the time label
        if self.time_remaining <= 0:
          self.record_answer(None)
          # Move on to the next question
          self.current_question_index += 1
          if self.current_question_index < len(self.questions):
              self.display_question()
          else:
              self.end_quiz()

    def option_button_click(self, button, **event_args):
        """This method is called when the button is clicked"""
        self.timer_1.interval = 0
        self.record_answer(button)

        # Stop the timer
        self.timer_1.enabled = False

        # Move on to the next question
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.display_question()
        else:
            self.end_quiz()

    def record_answer(self, answer):
        # Record the user's answer
        question = self.questions[self.current_question_index]
        correct_answer = question['answer']
        question_weight = question['questionweight']
        elapsed_time = self.start_time - self.time_remaining
        total_time = question['time']

        if answer == correct_answer:
            # The answer is correct
            # Calculate the score based on the time elapsed
            score = question_weight * (1 - elapsed_time / total_time)
            # If the student has the 'conf' perk, increase their score by a bonus amount
            if self.perk == 'conf' and self.correct_streak > 0:
                score += 0.1 * self.level
            self.correctq += 1
            score = round(score)
            self.outlined_card_1.visible = False
            self.outlined_card_2.visible = False
            self.outlined_card_3.visible = False
            self.outlined_card_6.visible = True
            self.message_label.text = f"Correct! You gained {score} points!"
            time.sleep(2)
            self.outlined_card_1.visible = True
            self.outlined_card_2.visible = True
            self.outlined_card_3.visible = True
            self.outlined_card_6.visible = False
            self.message_label.text = " "
            # Add the score to the total score
            self.score += score
            # Increase the streak of correct answers
            self.correct_streak += 1
        else:
            # The answer is incorrect
            if self.perk == 'chance' and random.random() < 0.1 * self.level:
                # The student has the 'chance' perk, and they're lucky
                # Give them a chance to retry the question
                self.current_question_index -= 1
                # Reset the streak of correct answers
                self.outlined_card_1.visible = False
                self.outlined_card_2.visible = False
                self.outlined_card_3.visible = False
                self.outlined_card_6.visible = True
                self.message_label.text = "Wrong answer, but heres your lucky second chance :) "
                time.sleep(2)
                self.outlined_card_1.visible = True
                self.outlined_card_2.visible = True
                self.outlined_card_3.visible = True
                self.outlined_card_6.visible = False
                self.message_label.text = " "
                self.correct_streak = 0
            else:
                # Reset the streak of correct answers
                self.outlined_card_1.visible = False
                self.outlined_card_2.visible = False
                self.outlined_card_3.visible = False
                self.outlined_card_6.visible = True
                self.message_label.text = "Incorrect Answer! "
                time.sleep(2)
                self.outlined_card_1.visible = True
                self.outlined_card_2.visible = True
                self.outlined_card_3.visible = True
                self.outlined_card_6.visible = False
                self.message_label.text = " "
                self.correct_streak = 0

        # Update the score label
        self.score_label.text = "Score: " + str(self.score)

    def end_quiz(self):
      # End the quiz and display the user's score
      self.label_score.text = "Final score: " + str(self.score)
      self.canswers.text = f"{self.correctq}/{self.numofq}"
      self.accuracy.text = f"{(self.correctq/self.numofq)*100}%"
      app_tables.quizresult.add_row(student=self.student['student'],
                          result=self.correctq,
                          correctpercentage= (self.correctq/self.numofq),
                          quizcode=self.quizcoderem,
                          points = self.score,
                          perk=self.perk)
      self.student['exp']+=self.score
      self.student['totalpoints']+=self.score
      self.student['completedquiz']+=1
      self.studentpoints.text = self.student['exp']
      anvil.server.call('quizzesincrement')
      self.outlined_card_1.visible = False
      self.outlined_card_2.visible = False
      self.outlined_card_3.visible = False      
      self.ending.visible = True
    def option_a_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.option_button_click('a')

    def option_b_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.option_button_click('b')

    def option_c_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.option_button_click('c')

    def option_d_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.option_button_click('d')

    def exit_click(self, **event_args):
      """This method is called when the button is clicked"""
      classtoreturn = app_tables.quizzes.get(quizcode=self.quizcoderem)['classcode']
      open_form('stupage.classroompage',classtoreturn)

    def outlined_button_1_click(self, **event_args):
      """This method is called when the button is clicked"""
      classtoreturn = app_tables.quizzes.get(quizcode=self.quizcoderem)['classcode']
      targetquiz = app_tables.quizzes.get(quizcode=self.quizcoderem)
      if targetquiz['reports'] is None:
        targetquiz['reports'] = 1
      else:
        targetquiz['reports'] += 1
      open_form('stupage.classroompage',classtoreturn)
      
