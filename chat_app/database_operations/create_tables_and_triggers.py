from cloud_database import query_db       

def create_user_table():
    query = """
    CREATE TABLE IF NOT EXISTS database1.user (
        username VARCHAR(50) NOT NULL PRIMARY KEY,
        display_name VARCHAR(50) NOT NULL,
        email_address VARCHAR(60),
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
    # group is a reserved keyword in sqlite, 
    # so 'group_table' is used instead as table name
    # however, all class definitions, function names, etc...
    # will use 'group' for simplicity
    return query_db(query, no_return=True)

def create_user_group_table():
    # user_group_table is a link table for the many_to_many
    # relationship between user and group
    # so its table name is user_group_table for clarity
    # even though user_group is not a reserved keyword
    
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
        CONSTRAINT invite_request_receiver_username_fk FOREIGN KEY (receiver_username) REFERENCES database1.user(username) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT invite_request_sender_username_fk FOREIGN KEY (sender_username) REFERENCES database1.user(username) ON UPDATE CASCADE ON DELETE CASCADE,
        CONSTRAINT invite_request_group_id_fk FOREIGN KEY (group_id) REFERENCES database1.group(group_id) ON UPDATE CASCADE ON DELETE CASCADE
    ) ENGINE=InnoDB;
    """
    # status can be 'pending', 'accepted', or 'rejected'
    return query_db(query, no_return=True)

def create_delete_group_with_no_users_trigger():
    query = """
    CREATE TRIGGER IF NOT EXISTS database1.delete_group_with_no_users
    AFTER DELETE ON database1.user_group
    FOR EACH ROW
    BEGIN
        DECLARE user_count INT;

        -- Count the number of users in the group
        SELECT COUNT(*) INTO user_count
        FROM database1.user_group
        WHERE group_id = OLD.group_id;

        -- If no users are in the group, delete the group
        IF user_count = 0 THEN
            DELETE FROM database1.group
            WHERE group_id = OLD.group_id;
        END IF;
    END;
    """
    return query_db(query, no_return=True)

def setup_database():
    query_db("SET FOREIGN_KEY_CHECKS = 1;", no_return=True)
    create_user_table()
    create_group_table()
    create_user_group_table()
    create_message_table()
    create_invite_request_table()
    create_delete_group_with_no_users_trigger()

setup_database()