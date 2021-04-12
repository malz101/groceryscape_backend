# online-grocery-store-restaurant

## HEROKU APP URL
https://infinite-beach-27814.herokuapp.com/

## SETUP VIRTUAL ENVIRONMENT
Navigate to root folder, i.e "online-grocery-store-restaurant"<br/>
Run the following command in terminal:<br/>
"python3 -m venv venv"<br/> 
or <br/>
"python -m venv venv"

## ACTIVATE VIRTUAL ENVIRONMENT
The virtual environment has to be activated for the application to work.<br/>
While in root folder run the following command in the terminal:<br/> 
"source venv/bin/activate"<br/>
       or<br/>
.\venv\Scripts\activate (if using Windows)

## INSTALL requirements
Once virtual environment is activated run:<br/>
"pip install -r requirements.txt"


## RUN appplication
Ensure you are in root folder<br/>
Enter in terminal<br/>
"python3 run.py"<br/>
or<br/> 
"python run.py"

## Create Database Tables
Navigate to the 'database' folder<br/>
Run "python3 schemas.py' in the terminal.<br/>
Ensure virtual environment is activated before you do so

## If using mysql-server
The connection to the database would not be established because of the new security features<br/>
One of two options:
1. Create a new mysql user and ensure password type is set to 'mysql_native_password'
    Run commands below to achieve this:<br/>
    1. CREATE USER '<newuser>'@'localhost' IDENTIFIED with mysql_native_password BY '<password>';
    2. GRANT ALL PRIVILEGES ON \*.\* TO '<newuser>'@'localhost';<br/>
                              or<br/>
       GRANT ALL PRIVILEGES ON <database_name>.* TO '<newuser>'@'localhost';
    3. Flush Privileges;
2. Change the password type of 'root' to 'mysql_native_password'
   Run commands below:<br/>
   1. ALTER USER 'root'@'localhost' IDENTIFIED with mysql_native_password BY '<MyNewPass>';
   2. Flush Privileges;

## note venv would need to be activated each time terminal is started


## Manage Database Schema from using Python environment (with version control)
navigate to root directory__
run command 'python3 manage.py init' to initialize the migrations if not already created__
run 'python manage.py migrate' to add changes to schema__
run 'python manage.py upgrade' to commit changes to schema


# online-grocery-store-restaurant

Getting started:

1) start xampp apache and mysql server
2) in your browser, type www.localhost/phpmyadmin.com
3) create a database named food_delivery
4) pull the code from the repo
5) navigate to root folder in command prompt
6) install flask using pip or otherwise
7) install flask_sqlalchemy using pip or otherwise
8) open another command prompt and navigate to the root folder
9) type "python" and press enter
10) this should launch the python interpreter
11) run "from app.database.Models import db"
12) then run "db.create_all()". This should create all the tables
13) to exist, type exit()
14) in your terminal and the root folder of the project, run "python run.py". This should start the server on port 5000
15) in your browser, type localhost:5000 to access customer home page OR
16) in your browser, type localhost:5000/manage_employee_account to access employee home page
