import sqlalchemy as sa

# AZURE DATABASE
#connection_string = "mysql+pymysql://avinash:M%40cr03c0n0m1c5@chat-app-database-mysql-server.mysql.database.azure.com:3306/database1"


# LOCAL DATABASE
connection_string = "mysql+pymysql://root:c%40tFISH0@localhost:3306/database1"


engine = sa.create_engine(connection_string, echo=True, isolation_level="SERIALIZABLE")

def query_db(query_string: str, parameter_dictionary: dict = None, no_return: bool = False):
    """_summary_
    This function is used to execute SQL queries on the database
    
    no_return argument exists as query engine's .fetchall() is needed for some queries
    but not for others, and .fetchall will throw an error if no rows are returned
    this argument is used to handle that case

    parameter_dictionary is used with sqlalchemy text function's parameter binding
    to protect against SQL injection
    
    Args:
        query_string (str): the SQL query to be executed
        parameter_dictionary (dict, optional): the dictionary of parameters for the sql query to be executed. Defaults to None.
        no_return (bool, optional): if the sql query is written to return rows, specify True. Defaults to False.
    
    Returns:
        list: if no_return is set to True, the function will return None
        None: if no_return is set to False, the function will return a list of rows (as tuples) returned by the query
    """
    
    if parameter_dictionary == None:
        if no_return:
            with engine.connect() as connection:
                connection.execute(sa.text(query_string))
                connection.commit()
                return None
        else:
            with engine.connect() as connection:
                result = connection.execute(sa.text(query_string))
                connection.commit()  
                
            return result.fetchall()
    else:
        if no_return:
            with engine.connect() as connection:
                connection.execute(sa.text(query_string), parameter_dictionary)
                connection.commit()
                return None
        else:
            with engine.connect() as connection:
                result = connection.execute(sa.text(query_string), parameter_dictionary)
                connection.commit()  
                
            return result.fetchall()
        
if __name__ == "__main__":
    
    #print(query_db("SHOW databases;"))
    pass
