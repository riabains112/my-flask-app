## Help Desk ticketing system 

## What is it?
It is a web application i have built using Flask. It allows Admins to create, delete , view and manage tickets. There are features that are tailored bot for adminstrators and regular users.

## Login Details 
Admin Deatils 
username -  admin@example.com
password -  adminpassword

User (Software Developer)
username -  ria.bains@icloud.com
password -   RiaBains123

User (Tester)
username -  mischajessop@icloud.com
password -  MischaJessop123

User (Developer)
username -  sianjones@icloud.com
password -  SianJones123

## Structure 
main.py: Entry point to start the application.
website/: Contains application code
-__init__.py: Initializes the app, database, and admin user.
-views.py: Handles user-facing routes.
-auth.py: Manages authentication and user registration.
-admin.py: Routes and functionality for admin users.
-models.py: Defines database models for Users and Tickets.
-static/: Contains static files (CSS, JavaScript, etc.).
-templates/: HTML templates for the app.

## Features 
admin features: include being able to view and create all tickets and be able to assign them to users.

Regular user features: create, view and update the progess off their own ticket. 

## Run application 
python main.py
The app will be available at http://127.0.0.1:5000


## Screenshots 
### 1. Login Page
![Login Page](screenshots/login.png)

### 2. Admin Dashboard
![Admin Dashboard](screenshots/home_admin.png)

### 3. Create Ticket
![Create Ticket](screenshots/create_ticket.png)

### 4. Validation Error
![Validation Error](screenshots/validation_error.png)