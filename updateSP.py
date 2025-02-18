import mysql.connector
import db_conn

if __name__ == '__main__':

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=db_conn.HOST,
        user=db_conn.FINAL_USER,
        password=db_conn.FINAL_PASSWORD,
        database=db_conn.DATABASE
    )

    cursor = conn.cursor()

    # Read the SQL script from a file
    with open(db_conn.DOWNLOAD_FILE_NAME, 'r') as file:
        sql_script = file.read()

    # Split the script by the custom delimiter `$$` used for defining functions/procedures
    # The delimiter should be $$, so split at that and replace it accordingly
    sql_commands = sql_script.split('$$')

    # First, execute commands before the functions, like `DROP FUNCTION`
    for command in sql_commands:
        command = command.strip()
        if command:  # Skip empty commands
            try:
                # For DROP FUNCTION statements, execute them normally with `;` delimiter
                if "DROP FUNCTION" in command:
                    cursor.execute(command)
                    print(f"Executed DROP: {command[:30]}...")  # Log the DROP command
                else:
                    print('DELIMITER $$ \n' + command + ' $$ \nDELIMITER ;')
                    # Execute CREATE FUNCTION statements with the custom delimiter handled
                    cursor.execute('DELIMITER $$ \n' + command + ' $$ \nDELIMITER ;')  # Add semicolon to properly terminate the command
                    print(f"Executed CREATE: {command[:30]}...")  # Log the CREATE command
            except mysql.connector.Error as err:
                print(f"Error executing command: {err}")
                break


    # Commit changes (if there are any modifications)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print("SQL script executed successfully!")