from ._anvil_designer import editmaterialTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
classcodenow = None

class editmaterial(editmaterialTemplate):
  def __init__(self,classid,materialid, **properties):
    global classcodenow
    classcodenow = classid
    self.material = materialid
    self.init_components(**properties)
    self.load_material(materialid)

  def load_material(self, material_code):
      if material_code == 0:
          # This is a new material
          self.material = app_tables.materials.add_row(
              materialcode=self.generate_matcode(),
              classcode=classcodenow,
              postdate=anvil.server.call('getawaredt'),
              title="",
              desc="",
              attachment=None
          )
      else:
          # Fetch the existing material from the database
          self.material = app_tables.materials.get(materialcode=material_code)

      # Load the material data into the form fields
      self.creation.text = self.material['postdate']
      self.title_box.text = self.material['title']
      self.desc_box.text = self.material['desc']
      
      # Update the label with the name of the attachment
      if self.material['attachment'] is not None:
          self.attachmentname.text = self.material['attachment'].name
      else:
          self.attachmentname.text = "No attachment"
  def save_button_click(self, **event_args):
      # Save the form fields back into the material row
      self.material['title'] = self.title_box.text
      self.material['desc'] = self.desc_box.text
      self.material['attachment'] = self.file_loader_1.file

      # Commit the changes to the database
      self.material.update()

    # Any code you write here will run before the form opens.
  def generate_matcode(self):
    max_mat_code = max((qu['materialcode'] for qu in app_tables.materials.search()), default=0)
    return max_mat_code + 1

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    self.attachmentname.text = self.file_loader_1.file.name

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    global classcodenow
    open_form('lecpage.lecclasspage.lecmaterial',classcodenow)

  def outlined_button_2_click(self, **event_args):
    global classcodenow
    # Ask the user to confirm the deletion
    if alert("Are you sure you want to delete this material?", title="Confirm Deletion", buttons=[("Yes", True), ("No", False)]):
        # Delete the material
        target = app_tables.materials.get(materialcode = self.material['materialcode'])
        target.delete()

        # Navigate back to the other form
        open_form('lecpage.lecclasspage.lecmaterial',classcodenow)  # Replace 'OtherForm' with the name of your form
