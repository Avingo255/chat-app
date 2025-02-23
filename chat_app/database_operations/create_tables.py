from chat_app.database_operations.database_connection import query_db       

def create_user_table():
    query = """
    CREATE TABLE IF NOT EXISTS database1.user (
        username VARCHAR(50) NOT NULL PRIMARY KEY,
        display_name VARCHAR(50) NOT NULL,
        form_group VARCHAR(10) NOT NULL,
        datetime_joined DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        password_hash VARCHAR(500) NOT NULL,
        is_authenticated BOOLEAN NOT NULL DEFAULT FALSE,
        is_active BOOLEAN NOT NULL DEFAULT TRUE,
        is_anonymous BOOLEAN NOT NULL DEFAULT FALSE
    ) ENGINE=InnoDB;
    """
    return query_db(query, no_return=True)

def create_group_table():
    query = """
    CREATE TABLE IF NOT EXISTS database1.group (
        group_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        group_name VARCHAR(50) NOT NULL,
        datetime_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB;
    """
    return query_db(query, no_return=True)

def create_user_group_table():
    
    query = """
    CREATE TABLE IF NOT EXISTS database1.user_group (
        username VARCHAR(50) NOT NULL,
        group_id INT NOT NULL,
        PRIMARY KEY (username, group_id),
        CONSTRAINT user_group_username_fk FOREIGN KEY (username) REFERENCES database1.user(username) ON DELETE CASCADE ON UPDATE CASCADE,
        CONSTRAINT user_group_group_id_fk FOREIGN KEY (group_id) REFERENCES database1.group(group_id) ON DELETE CASCADE ON UPDATE CASCADE
    ) ENGINE=InnoDB;
    """
    return query_db(query, no_return=True) 

def create_message_table():
    query = """
    CREATE TABLE IF NOT EXISTS database1.message (
        message_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        message_content VARCHAR(2000) NOT NULL,
        message_date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        sender_username VARCHAR(50) NOT NULL,
        group_id INT NOT NULL,
        CONSTRAINT message_sender_username_fk FOREIGN KEY (sender_username) REFERENCES database1.user(username) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT message_group_id_fk FOREIGN KEY (group_id) REFERENCES database1.group(group_id) ON UPDATE CASCADE ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
    return query_db(query, no_return=True)

def create_invite_request_table():
    query = """
    CREATE TABLE IF NOT EXISTS database1.invite_request (
        request_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        receiver_username VARCHAR(50) NOT NULL,
        sender_username VARCHAR(50) NOT NULL,
        group_id INT NOT NULL,
        status VARCHAR(50) NOT NULL,
        request_date_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT invite_request_receiver_username_fk FOREIGN KEY (receiver_username) REFERENCES database1.user(username) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT invite_request_sender_username_fk FOREIGN KEY (sender_username) REFERENCES database1.user(username) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT invite_request_group_id_fk FOREIGN KEY (group_id) REFERENCES database1.group(group_id) ON UPDATE CASCADE ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
    # status can be 'pending', 'accepted', or 'rejected'
    return query_db(query, no_return=True)


def setup_database():
    query_db("SET FOREIGN_KEY_CHECKS = 1;", no_return=True)
    create_user_table()
    create_group_table()
    create_user_group_table()
    create_message_table()
    create_invite_request_table()

if __name__ == '__main__':
    setup_database()