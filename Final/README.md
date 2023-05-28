**About my Project**

My final project is a task application named Taskhub. It consists of a noticeboard where you can create and delete movable and resizable notes, a tasks page where you can create and delete tasks with subtasks and deadlines, and a calendar that you can view your tasks on.

The noticeboard page utilises a Javascript library called Interact.js for implementing the movable and resizable notes in the Noticeboard page. The notes are automatically saved and updated in the database when resized, moved or edited.

The tasks page uses formsets to allow the user to add subtasks to the tasks they create. They can also complete tasks, individual subtasks and delete tasks. Users can also choose to only view tasks they have completed or have not completed.

On the calendar page, the user can view all the tasks they have created on a calendar created using CSS Grids. The calendar will load the current date. The calendar will update when the user scrolls up or down to show the next or previous dates.

I believe the project satisfies the distinctiveness requirements as it is a different application from the previous projects, and it also utilises libraries that were not used in previous projects. This application also uses features of Django such as formsets that were not implemented in previous projects. I believe this application also fulfils the complexity requirements of the project as it utilises multiple models as well as javascript libraries, and implements features that were not done in previous projects.


**Application Directory**

taskhub - main application directory
- static - contains all static content namely the css and js files.
  - styles.css - stylesheet for the layout.html base template.
  - login.css - stylesheet for the login/register.html template.
  - noticeboard.css - stylesheet for the noticeboard.html template.
  - noticeboard.js - script for the noticeboard.html template.
  - tasks.css - stylesheet for the tasks.html template.
  - tasks.js - script for the tasks.html template.
  - calendar.css - stylesheet for the calendar.html template.
  - calendar.js - script for the calendar.html template.
- templates/taskhub - contains all application templates.
  - layout.html - base template. All other templates extend it.
  - noticeboard.html - templates for users lists.
  - tasks.html - template that shows user tasks and allows the user to create tasks.
  - register.html - template to show register form for new users.
  - login.html - template to show login form.
- admin.py - registered models used for the project.
- apps.py - for configuration of the app.
- models.py - contains the models used in the project. User model extends the standard User model, the Board and Note model are for the Noticeboard page, and the Task model is to represent a user task.
- urls.py - all application URLs.
- views.py - contains all application views.


**Running the application:**
1. This application does not require installation of any packages/modules.
2. Make and apply migrations by running "python manage.py makemigrations" and "python manage.py migrate".
3. Go to website address and register an account.
