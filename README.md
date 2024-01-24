# NIKKO ticket managment software
#### Video Demo:  <https://youtu.be/6Ea12THBGms>
#### Description:
my fina project is a ticket management application. Technologies used:
- flask
- sqlite
- ajax
- jinja2

it relies on python libraries:
- Werkzeug
- cs50 libaraies
 Ticket managment platform has 3 statuses to do, in progress and done, users can add, delete and change ticket status as they like. In ticket there are to do items witch user can add mark them as done.


# Interface


#### Register page

The "Register" page allows new users to create an account and gain access to the features and functionalities of this platform. To register, users need to provide essential information, including a unique username, a secure password, their first name, and last name. for password I used werkzeug.security library.

#### Log In page

The "Login" page is where registered users can access their accounts by providing their unique username and password. Logging in allows users to access their personalized dashboard, manage their tickets, and interact with tasks associated with those tickets.


#### Home page

The home page is main hub where user can add tickets they can also change its status, rename or delete them.


#### platform page

The platform page users are able to add to do items in their tickets they can also edit or dlete them.



#### Managing Tickets
Home Page: View a list of your active tickets.
Add Ticket: Create a new ticket with a title.
Edit Ticket: Modify the title of an existing ticket.
Delete Ticket: Delete a ticket and its associated tasks.
Change Ticket Status: Change the status of a ticket.



#### Managing Tasks
View and manage tasks associated with a ticket on the platform page.
Add, edit, and delete tasks as needed.



## Features
User authentication and authorization.
Create, edit, and delete tickets.
Manage tasks associated with tickets.
Real-time updates using AJAX (example: changing task status).


# Files


#### app.py:
I decided to develope my final project in ppython as I felt more comfortable using it. I used cs50 libaraies and took great inspiration from finance problem set in week 9. I worte all the functions seperatly like: log in, register, add ticket, remane ticket and etc.



#### help.py
I copyed this file from finance problem it has login reqierd and error functions.


#### templates:
templates are separated for each page to keep the code simple and readable. in index.html I used ajax to update data asynchronously to database.


# Database

#### database.db:
For me this was the most interesting part of the project. SQLite is used for back-end storage for simplicity but any SQL implementation can be integrated with the code. I use only one database with tables:
- Users
- Tickets
- To-do Items

all are in one to many relationship between each other, all identified with self incrementing unique IDs. Users own tickets and tickets have to-do items. I used SQLdbm.com to design relational schema and imported it manually in SQLite via CLI.

User passwords are not stored on back-end, they are hashed and salted.