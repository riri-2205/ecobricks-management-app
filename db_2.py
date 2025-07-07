import mysql.connector

def crCon(db_name=None):
    conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password='R22ithika05@2005',
        database=db_name
    )
    cursor=conn.cursor()
    return conn,cursor

def crDb():
    conn,cursor=crCon()
    cursor.execute("create database if not exists Ecobricks")
    cursor.execute("use Ecobricks")
    cursor.close()
    conn.close()
    return crCon("Ecobricks")

def crTables(conn, cursor):
    cursor.execute("""CREATE TABLE if not exists Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_no VARCHAR(15),
    role ENUM('Donator', 'Builder', 'Admin') NOT NULL,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    verification_status ENUM('Verified', 'Unverified') DEFAULT 'Unverified'
    );""")

    cursor.execute("""CREATE TABLE if not exists Inventory (
    inventory_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    weight DECIMAL(10,2) CHECK (weight > 0),
    plastic_type ENUM('PET', 'HDPE', 'PVC', 'LDPE', 'PP', 'PS', 'Other') NOT NULL,
    collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
    );""")

    cursor.execute("""CREATE TABLE if not exists Projects(
    project_id INT PRIMARY KEY AUTO_INCREMENT,
    project_name VARCHAR(255),
    user_id INT,
    weight DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    project_status ENUM('In progress', 'Pending', 'Finished') DEFAULT 'Pending',
    category ENUM('Environmental', 'Medical','Social','Economic', 'Other'),
    urgency ENUM('Immediate', 'Medium-term','Short-term','Long-term','None'),
    priority_score INT
    )""")

    cursor.execute("""CREATE TABLE if not exists global_variables (
    name VARCHAR(255) PRIMARY KEY,
    value DECIMAL(10,2) NOT NULL
    );""")

    conn.commit()

def crTriggers(conn,cursor):
    cursor.execute("""
    Delimiter //

    create trigger if not exists update_total_ecobricks
    after insert on inventory
    for each row
    begin
        declare selected_project int default null;
        declare project_weight decimal(10,2);
        declare total_ecobricks decimal(10,2);

        UPDATE global_variables 
        SET value = value + NEW.weight
        WHERE name = 'total_ecobricks';

        select value into total_ecobricks from global_variables where name='total_ecobricks';
        select project_id,weight into selected_project, project_weight
        from projects where project_status='Pending' and weight<=total_ecobricks order by priority_score desc, project_id asc
        limit 1;

        if selected_project is not null then 
            UPDATE  projects
            set project_status='In progress'
            where project_id=selected_project;
            
            UPDATE global_variables SET value = value - project_weight WHERE name = 'total_ecobricks';
            
        end if;
    end;
    //
    delimiter ;
    """)

    cursor.execute("""
    DELIMITER //
    CREATE TRIGGER if not exists calculate_priority_score
    BEFORE INSERT ON Projects
    FOR EACH ROW
    BEGIN
        DECLARE category_weight INT DEFAULT 1;
        DECLARE urgency_score INT DEFAULT 1;

        -- Assign category weight
        SET category_weight = 
            CASE 
                WHEN NEW.category = 'Environmental' THEN 5
                WHEN NEW.category = 'Medical' THEN 4
                WHEN NEW.category = 'Social' THEN 3
                WHEN NEW.category = 'Economic' THEN 2
                ELSE 1
            END;

        -- Assign urgency score
        SET urgency_score = 
            CASE 
                WHEN NEW.urgency = 'Immediate' THEN 5
                WHEN NEW.urgency = 'Short-term' THEN 4
                WHEN NEW.urgency = 'Medium-term' THEN 3
                WHEN NEW.urgency = 'Long-term' THEN 2
                ELSE 1
            END;
        -- Calculate final priority score
        SET NEW.priority_score = (category_weight * 2) + urgency_score;
    END;
    //
    DELIMITER ;""")

    cursor.execute("""create procedure if not exists reward_points(IN id INT, OUT points DECIMAL(10,2))\
        begin
        select sum(weight) into points from inventory where user_id=id;
        end;""")
def closeCon(conn,cursor):
    cursor.close()
    conn.close()
    