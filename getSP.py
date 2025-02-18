import mysql.connector
import db_conn
import re

# Define the output CSV file name
new_definer = db_conn.DEFINER_NAME          # new definer
f_new = open(db_conn.DOWNLOAD_FILE_NAME, 'w')     # open a file to write the updated definer stored procedures

if __name__ == '__main__':

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host=db_conn.HOST,
        user=db_conn.USER,
        password=db_conn.PASSWORD,
        database=db_conn.DATABASE
    )

    cursor = conn.cursor()

    # Query to get all stored procedures from the information schema
    cursor.execute("""
        SELECT * FROM information_schema.ROUTINES
        WHERE ROUTINE_SCHEMA = %s AND ROUTINE_TYPE IN ('PROCEDURE', 'FUNCTION') ORDER BY ROUTINE_TYPE
    """, (db_conn.DATABASE,))

    # Fetch all stored procedure & function names
    routines = cursor.fetchall()
    pattern = r"CREATE DEFINER=`(.*?)`@`%`"     # to get the definer pattern
    i = 0

    # Iterate over the procedures and execute SHOW CREATE PROCEDURE
    for routine in routines:
        routine_name = routine[3]  # ROUTINE_NAME is in the 3rd column (index 2)
        routine_type = routine[4]  # ROUTINE_TYPE is in the 6th column (index 5)
        i += 1

        if routine_type == 'PROCEDURE':
            cursor.execute(f"SHOW CREATE PROCEDURE `{db_conn.DATABASE}`.`{routine_name}`;")
            result = cursor.fetchone()
            create_statement = result[2]  # The third column contains the CREATE PROCEDURE statement
            altered_create_statement = re.sub(pattern, f"CREATE DEFINER=`{new_definer}`@`%`", create_statement)

            print(f"# Stored Procedure {i}: {routine_name}\n{create_statement}\n")
            f_new.write(f"-- Stored Procedure {i}: {routine_name} \n")
            f_new.write(f"DROP PROCEDURE IF EXISTS {routine_name}; $$ \n")
            f_new.write(f"{altered_create_statement}$$\n\n")
        elif routine_type == 'FUNCTION':
            cursor.execute(f"SHOW CREATE FUNCTION `{db_conn.DATABASE}`.`{routine_name}`;")
            result = cursor.fetchone()
            create_statement = result[2]  # The third column contains the CREATE PROCEDURE statement
            altered_create_statement = re.sub(pattern, f"CREATE DEFINER=`{new_definer}`@`%`", create_statement)

            print(f"# Function {i}: {routine_name}\n{create_statement}\n")
            f_new.write(f"-- Function {i}: {routine_name} \n")
            f_new.write(f"DROP FUNCTION IF EXISTS {routine_name}; $$ \n")
            f_new.write(f"{altered_create_statement}$$\n\n")

    # Close the cursor and connection
    cursor.close()
    conn.close()

    f_new.close()
