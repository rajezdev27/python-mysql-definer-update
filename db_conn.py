# Database connection details
HOST = 'www'  # e.g., 'mydbinstance.xyz123.us-west-2.rds.amazonaws.com'
USER = 'xxx'  # e.g., 'manager'
PASSWORD = 'yyy'  # e.g., 'manager_password'
DATABASE = 'zzz'  # e.g., 'mydatabase'

FINAL_USER = 'new_definer'  # e.g., 'manager'
FINAL_PASSWORD = 'bbb'  # e.g., 'manager_password'

# Definer & logged in(FINAL_USER) user must be same and the user must have permissions to DROP, ALTER, CREATE - Stored Procedures & Function
DEFINER_NAME = 'new_definer'
DOWNLOAD_FILE_NAME = 'fff.sql'
