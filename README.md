# online-grocery-store-restaurant

Getting started:

1) start xampp apache and mysql server
2) in your browser, type www.localhost/phpmyadmin.com
3) create a database named food_delivery
4) pull the code from the repo
5) navigate to root folder in command prompt
6) install flask using pip or otherwise
7) install flask_sqlalchemy using pip or otherwise
8) open another command prompt and navigate to the database folder
9) type "python" and press enter
10) this should launch the python interpreter
11) run "from Models import db"
12) then run "db.create_all()". This should create all the tables
13) to exist, type exit()
14) in your terminal and the root folder of the project, run "python app.py". This should start the server on port 5000
15) in your browser, type localhost:5000 to access customer home page OR
16) in your browser, type localhost:5000/manage_employee_account to access employee home page