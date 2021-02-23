# online-grocery-store-restaurant

# SETUP VIRTUAL ENVIRONMENT
navigate to root folder, i.e "online-grocery-store-restaurant"
run the following command in terminal: "python3 -m venv venv" or "python -m venv venv"

# ACTIVATE VIRTUAL ENVIRONMENT
the virtual environment has to be activated for the application to work
while in root folder run the following command in the terminal: 
"source venv/bin/activate"
       or
.\venv\Scripts\activate (if using Windows)

# INSTALL requirements
once virtual environment is activated
run "pip install -r requirements.txt"


# RUN appplication
enter in terminal "python3 run.py" or "python run.py"

# Create Database Tables
navigate to database folder and run "python3 schemas.py' in the terminal
ensure virtual environment is activated before you do so

# If using mysql-server
The connection to the database would not be established because of the new security features
One of two options:
1. Create a new mysql user and ensure password type is set to 'mysql_native_password'
    Run commands below to achieve this:
    1. CREATE USER '<newuser>'@'localhost' IDENTIFIED with mysql_native_password BY '<password>';
    2. GRANT ALL PRIVILEGES ON *.* TO '<newuser>'@'localhost';
                              or
       GRANT ALL PRIVILEGES ON <database_name>.* TO '<newuser>'@'localhost';
    3. Flush Privileges;
2. Change the password type of 'root' to 'mysql_native_password'
   Run commands below:
   1. ALTER USER 'root'@'localhost' IDENTIFIED with mysql_native_password BY '<MyNewPass>';
   2. Flush Privileges;

## note venv would need to be activated each time terminal is started