import mysql.connector
from mysql.connector import errorcode

def connect_to_server(config):
    try:
        conn = mysql.connector.connect(**config)
        print("Successfully Connected!")
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Username and password didn't match")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print("unexcepted error:")
            print(err)
        return False
    else:
        return conn
    
def helper(operation, input_value, col_names=None):
    if col_names is None:
        col_names = []
    table_name = input_value.get("table_name")
    if operation == "insert" or operation == "update":
        value_list = [input_value.get(col) for col in col_names]
        if operation == "insert":
            return table_name, value_list
        else:  # operation == "update"
            row_num = input_value.get("row")
            return table_name, row_num, value_list
    elif operation == "delete":
        row_num = input_value.get("row")
        return table_name, row_num
    else:
        raise ValueError("Invalid operation specified")

def print_table_info(config, print_type="", table_name="example_table"):
    conn=False
    conn=connect_to_server(config)
    if conn==False:
        return
    else:
        cursor = conn.cursor()
        if print_type == 'show_tables':
            cursor.execute("SHOW TABLES;")
            table_names = [i[0] for i in cursor.fetchall()]
            print(table_names)
            return table_names
        elif print_type == 'show_col':
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            col_names = [i[0] for i in cursor.description]
            print(col_names)
            return col_names
        else:
            query = f"SELECT * FROM {table_name};"
            cursor.execute(query)
            rows = cursor.fetchall()
            data = [[index + 1] + list(row) for index, row in enumerate(rows)]
            print(data)
            return data

def operating_mydatabase(config, col_names=[], input_value={}, data=[], operation="insert"):
    conn=False
    conn=connect_to_server(config)
    if conn==False:
        return
    else:
        cursor = conn.cursor()
        if operation == "insert":
            try:
                table_name, value_list = helper(operation, input_value, col_names)
                 # Construct column names part of the query
                col_names_str = ", ".join(col_names)
                # Construct placeholders for values
                placeholders = ", ".join(["%s"] * len(value_list))
                query = f"INSERT INTO {table_name} ({col_names_str}) VALUES ({placeholders});"
                # Execute the query with values
                cursor.execute(query, tuple(value_list))
                try:
                    conn.commit()
                    print(f"Inserted {cursor.rowcount} row(s) of data.")
                except Exception as commit_error:
                    print(f"Fail to insert. Error: {commit_error}")
            except Exception as err:
                print(f"Insert failed: {err}")
                conn.rollback()
            return query
        elif operation == "delete":
            try:
                table_name, row_num = helper(operation, input_value)
                delete_row = data[int(row_num) - 1][1:]
                conditions = " AND ".join([f"{col} = %s" for col in col_names])
                query = f"DELETE FROM {table_name} WHERE {conditions};"
                cursor.execute(query, delete_row)
                try:
                    conn.commit()
                    print("Deleted", cursor.rowcount, "row of data.")
                except Exception as commit_error:
                    print(f"Fail to delete. Error: {commit_error}")
                    conn.rollback()
            except Exception as err:
                print("Delete failed: ", err)
                conn.rollback()
            return query
        elif operation == "update":
            try:
                table_name, row_num, value_list = helper(operation, input_value, col_names)
                update_row = data[int(row_num) - 1][1:]
                set_clause = ", ".join([f"{col} = %s" for col in col_names])
                where_clause = " AND ".join([f"{col} = %s" for col in col_names])
                query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause};"
                # Combine value_list and update_row for the full set of parameters
                parameters = value_list + update_row
                cursor.execute(query, parameters)
                try:
                    conn.commit()
                    print("Updated", cursor.rowcount, "row of data.")
                except Exception as commit_error:
                    print(f"Fail to update. Error: {commit_error}")
                    conn.rollback()
            except Exception as err:
                print("Update failed: ", err)
                conn.rollback()
            return query
        # Cleanup
        cursor.close()
        conn.close()