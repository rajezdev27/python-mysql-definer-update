# python-mysql-definer-update
To get the list of existing mysql Database's stored procedures and functions and update the new definer

Prerequisites: Python 3.13

Problem: 
  We cannot able to simply update the name or attributes of Stored Procedures & Functions in a MySQL database. We should DROP & CREATE them.

Steps to execute:
1. Update your database credentials in db_conn.py
2. Run the getSP.py file - To get the list of all available Stored Procedures & Functions in a Database
3. You will see a new sql file contains the list of Stored Procedures & Functions, after the Step#2 completed
4. Run the updateSP.py to update the new definer in a fast as well as effective manner
