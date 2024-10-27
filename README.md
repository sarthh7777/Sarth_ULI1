# Sarth_ULI1
a to-do list application in Django where users can sign up, log in, and manage their own to-do lists.

Features
Project Structure

Django project named ToDoProject.
App named tasks.
User Authentication

User registration with username and password.
User login and logout functionality.
Task Management

Task Model:
Title (CharField, max length 200).
Description (TextField, optional).
Created at (DateTimeField, auto_now_add=True).
Completed status (BooleanField, default: False).
Association with user (ForeignKey to Django’s User model).
Views:
Task List: Displays tasks for logged-in users.
Task Creation: Functionality to add new tasks.
Task Update: Option to mark tasks as completed or edit details.
Task Deletion: Functionality to remove tasks.

User Interface:
Homepage showcasing the user's tasks.
Forms for task addition and editing.
Links for login, logout, and user registration.
Task visibility restricted to the logged-in user.
Routing

URL definitions for all features.
Admin Interface

Task model registered in Django admin for management.
Bonus Features
tick box for completed tasks 
Basic CSS for improved layout and form styling.
Expected Outcome
Users manage their personal to-do lists with restricted access to their tasks.
