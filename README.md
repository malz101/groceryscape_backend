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
navigate to root directory<br>
run command 'python3 manage.py init' to initialize the migrations if not already created<br>
run 'python manage.py migrate' to add changes to schema<br>
run 'python manage.py upgrade' to commit changes to schema

