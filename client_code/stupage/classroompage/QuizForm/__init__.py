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

class QuizForm(QuizFormTemplate):
    def __init__(self, quizcode, studentid, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Retrieve the quiz data
        self.questions = app_tables.quizcontent.search(quizcode=quizcode)

        # Initialize the score and the streak of correct answers
        self.score = 0
        self.correct_streak = 0

        # Retrieve the student's perk
        self.student = app_tables.studentsclasses.get(student=studentid)
        self.perk = self.student['perk']
        self.level = self.student['level']


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
        if question['image']:
            self.image.source = question['image']

        # Start the timer for this question
        time = question['time']
        if self.perk == 'time':
            # The student has the 'time' perk, so increase the time by a certain amount
            time += self.level  # Modify this to suit your needs
        self.start_time = anvil.server.call('get_current_time')
        self.time_remaining = question['time']
        self.timeleft.text = str(self.time_remaining)
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
        # Handle the user's answer
        # 'button' is the button that was clicked
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
        elapsed_time = anvil.server.call('get_current_time') - self.start_time
        total_time = question['time']

        if answer == correct_answer:
            # The answer is correct
            # Calculate the score based on the time elapsed
            score = question_weight * (1 - elapsed_time / total_time)
            # If the student has the 'conf' perk, increase their score by a bonus amount
            if self.perk == 'conf' and self.correct_streak > 0:
                score += self.level  # Modify this to suit your needs
            # Round the score to the nearest integer
            score = round(score)
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
            else:
                # Reset the streak of correct answers
                self.correct_streak = 0

        # Update the score label
        self.score_label.text = "Score: " + str(self.score)

    def end_quiz(self):
      # End the quiz and display the user's score
      self.label_score.text = "Final score: " + str(self.score)
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
