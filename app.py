from flask import Flask, jsonify, request, render_template
# from dotenv import load_dotenv
import mysql.connector
import os
from swagger.swaggerui import setup_swagger
import random
import string


app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Set up Swagger
setup_swagger(app)

# Load environment variables from .env file
# load_dotenv()

# Check if the file "dev" exists
if not os.path.exists('dev'):
    # Retrieve MySQL connection details from environment variable
    mysql_details = os.getenv('MYSQL_DETAILS')

    if mysql_details:
        # Split the details by "@"
        details = mysql_details.split('@')

        # Extract the individual values
        host = details[0]
        user = details[1]
        password = details[2]
        database = details[3]
        port = int(details[4])

        # MySQL connection setup
        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            print("Connection successful")

        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL: {err}")
            db_connection = None
    else:
        print("MYSQL_DETAILS environment variable is not set.")
        db_connection = None
else:
    print("File 'dev' exists. Skipping MySQL connection setup.")



# Helper function to reconnect to MySQL
def reconnect_to_mysql():
    global db_connection

    mysql_details = os.getenv('MYSQL_DETAILS')

    if mysql_details:
        # Split the details by "@"
        details = mysql_details.split('@')

        # Extract the individual values
        host = details[0]
        user = details[1]
        password = details[2]
        database = details[3]
        port = int(details[4])

        # MySQL connection setup
        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            print("Reconnection successful")
            return True

        except mysql.connector.Error as err:
            print(f"Error reconnecting to MySQL: {err}")
            db_connection = None
            return False
    else:
        print("MYSQL_DETAILS environment variable is not set.")
        db_connection = None
        return False

def generate_random_string(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def get_cursor():
    if db_connection:
        return db_connection.cursor()
    else:
        return None

def is_mysql_available():
    return db_connection is not None

# Route to handle MySQL errors
def handle_mysql_error(e):
    print(f"MySQL Error: {e}")
    return jsonify({"error": "MySQL database operation failed. Please check the database connection."}), 500

# Initial list of fields
field_db = [
    ["app_status", "idle"],
    ["app_timestamp", "idle"],
]

##✅ ------ create table users_recharge ---------------- ##
@app.route('/create-table-users-recharge', methods=['GET'])
def create_users_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'users_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'users_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'users_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE users_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    userName TEXT NOT NULL,
                    passwordHash TEXT NOT NULL,
                    role TEXT,
                    groupId TEXT,
                    email TEXT,
                    status TEXT,
                    token TEXT,
                    resetCode TEXT,
                    timestamp TIMESTAMP  DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'users_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ create table profile_recharge ---------------- ##
@app.route('/create-table-profile-recharge', methods=['GET'])
def create_profile_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'profile_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'profile_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'profile_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE profile_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    firstName TEXT,
                    lastName TEXT,
                    suffix TEXT,
                    contactNumber TEXT,
                    email TEXT,
                    address TEXT,
                    birthday TEXT,
                    photoURL TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'profile_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


##✅ ------ create table store_recharge ---------------- ##
@app.route('/create-table-store-recharge', methods=['GET'])
def create_store_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'store_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'store_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'store_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE store_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    station1BottleCount TEXT,
                    station2BottleCount TEXT,
                    station3BottleCount TEXT,
                    station1Points TEXT,
                    station2Points TEXT,
                    station3Points TEXT,
                    station1TimeLeft TEXT,
                    station2TimeLeft TEXT,
                    station3TimeLeft TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'store_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


##✅ ------ create table station_recharge ---------------- ##
@app.route('/create-table-station-recharge', methods=['GET'])
def create_station_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'station_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'station_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'station_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE station_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    stationName TEXT,
                    stationStatus TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'station_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


##✅ ------ create table rewards_recharge ---------------- ##
@app.route('/create-table-rewards-recharge', methods=['GET'])
def create_rewards_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'rewards_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'rewards_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'rewards_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE rewards_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    rewardName TEXT,
                    rewardTime TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'rewards_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ create table bottle_history_recharge ---------------- ##
@app.route('/create-table-bottle-history-recharge', methods=['GET'])
def create_bottle_history_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'bottle_history_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'bottle_history_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'bottle_history_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE bottle_history_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    bottleCount TEXT,
                    bottleNotes TEXT,
                    fromStation TEXT,
                    bottleStatus TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'bottle_history_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


##✅ ------ create table notification_recharge ---------------- ##
@app.route('/create-table-notification-recharge', methods=['GET'])
def create_notification_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Check if table 'notification_recharge' exists
            cursor.execute("SHOW TABLES LIKE 'notification_recharge'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                cursor.close()
                return jsonify({"message": "Table 'notification_recharge' already exists"}), 200
            else:
                # Define SQL query to create table if it doesn't exist
                sql_create_table = """
                CREATE TABLE notification_recharge (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    uniqueId TEXT NOT NULL,
                    role TEXT,
                    status TEXT,
                    message TEXT,
                    priority TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
                cursor.execute(sql_create_table)
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Table 'notification_recharge' created successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table users_recharge ---------------- ##
@app.route('/delete-table-users-recharge', methods=['GET'])
def delete_users_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'users_recharge' table
            cursor.execute("DROP TABLE IF EXISTS users_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'users_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table profile_recharge ---------------- ##
@app.route('/delete-table-profile-recharge', methods=['GET'])
def delete_profile_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'profile_recharge' table
            cursor.execute("DROP TABLE IF EXISTS profile_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'profile_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table store_recharge ---------------- ##
@app.route('/delete-table-store-recharge', methods=['GET'])
def delete_store_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'store_recharge' table
            cursor.execute("DROP TABLE IF EXISTS store_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'store_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table station_recharge ---------------- ##
@app.route('/delete-table-station-recharge', methods=['GET'])
def delete_station_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'station_recharge' table
            cursor.execute("DROP TABLE IF EXISTS station_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'station_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table rewards_recharge ---------------- ##
@app.route('/delete-table-rewards-recharge', methods=['GET'])
def delete_rewards_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'rewards_recharge' table
            cursor.execute("DROP TABLE IF EXISTS rewards_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'rewards_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table bottle_history_recharge ---------------- ##
@app.route('/delete-table-bottle-history-recharge', methods=['GET'])
def delete_bottle_history_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'bottle_history_recharge' table
            cursor.execute("DROP TABLE IF EXISTS bottle_history_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'bottle_history_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

##✅ ------ delete table bottle_history_recharge ---------------- ##
@app.route('/delete-table-bottle-history-recharge', methods=['GET'])
def delete_bottle_history_recharge_table():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Drop the 'bottle_history_recharge' table
            cursor.execute("DROP TABLE IF EXISTS bottle_history_recharge")
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Table 'bottle_history_recharge' deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


## ------ insert table ---------------- ##

@app.route('/insert-mockup-users-recharge', methods=['GET'])
def insert_mockup_users_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'users_recharge' table without the 'timestamp' field
            sql_insert = """
            INSERT INTO users_recharge (uniqueId, userName, passwordHash, role, groupId, email, status, token, resetCode)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = ('mockUniqueId', 'testname', 'testpassword', 'admin', 'group1', 'mockEmail@example.com', 'active', 'mockToken', 'mockResetCode')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'users_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-profile-recharge', methods=['GET'])
def insert_mockup_profile_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'profile_recharge' table
            sql_insert = """
            INSERT INTO profile_recharge (uniqueId, firstName, lastName, suffix, contactNumber, email, address, birthday, photoURL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = ('mockUniqueId', 'John', 'Doe', 'Jr.', '1234567890', 'mockEmail@example.com', '123 Mock St.', '1990-01-01', 'http://example.com/photo.jpg')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'profile_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-station-recharge', methods=['GET'])
def insert_mockup_station_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert multiple mock data into 'station_recharge' table
            sql_insert = """
            INSERT INTO station_recharge (uniqueId, stationName, stationStatus)
            VALUES (%s, %s, %s)
            """
            data = [
                ('1234', 'Station1', 'active'),
                ('6578', 'Station2', 'active'),
                ('9102', 'Station3', 'active')
            ]
            cursor.executemany(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'station_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-rewards-recharge', methods=['GET'])
def insert_mockup_rewards_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'rewards_recharge' table
            sql_insert = """
            INSERT INTO rewards_recharge (uniqueId, rewardName, rewardTime)
            VALUES (%s, %s, %s)
            """
            data = ('1234', 'Add 15 minutes', '15')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'rewards_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-bottle-history-recharge', methods=['GET'])
def insert_mockup_bottle_history_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'bottle_history_recharge' table
            sql_insert = """
            INSERT INTO bottle_history_recharge (uniqueId, bottleCount, bottleNotes, fromStation, bottleStatus)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = ('1234', '1', 'Recycled bottles', 'Station1', 'completed')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'bottle_history_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


@app.route('/insert-mockup-notification-recharge', methods=['GET'])
def insert_mockup_notification_recharge():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'notification_recharge' table
            sql_insert = """
            INSERT INTO notification_recharge (uniqueId, role, status, message, priority)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = ('1234', 'admin', 'unread', 'Bottle count low at Station 2', 'high')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'notification_recharge' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)




@app.route('/insert-mockup-profile', methods=['GET'])
def insert_mockup_profile():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'profile' table
            sql_insert = """
            INSERT INTO profile (userId, firstName, lastName, suffix, contactNumber, email, address, birthday, photoURL, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = ('mockUserId', 'John', 'Doe', 'Jr', '1234567890', 'mockEmail@example.com', '123 Mock Street, City, Country', '1990-01-01', 'http://mockphoto.com/photo.jpg', '2025-03-08 00:00:00')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'profile' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-store', methods=['GET'])
def insert_mockup_store():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'store' table
            sql_insert = """
            INSERT INTO store (lockerId, locker1, locker2, locker3)
            VALUES (%s, %s, %s, %s)
            """
            data = ('Locker11234', 'locked', 'locked', 'locked')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'store' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-notifications', methods=['GET'])
def insert_mockup_notifications():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'notifications' table
            sql_insert = """
            INSERT INTO notifications (userId, role, status, message, timestamp)
            VALUES (%s, %s, %s, %s, %s)
            """
            data = ('mockUserId', 'admin', 'unread', 'This is a mock notification', '2025-03-08 00:00:00')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'notifications' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-activity', methods=['GET'])
def insert_mockup_activity():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'activity' table
            sql_insert = """
            INSERT INTO activity (userId, role, status, type, info, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            data = ('mockUserId', 'admin', 'active', 'login', 'User logged in from IP 192.168.1.1', '2025-03-08 00:00:00')
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'activity' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-watersense', methods=['GET'])
def insert_mockup_watersense():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'watersense' table
            sql_insert = """
            INSERT INTO watersense (userid, indicator, phlevel, temperature, conductivity, turbidity, orp, tds)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                '1234', 'check', '7.5', '25.5', '0.8', '5.2', '300', '400'
            )
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'watersense' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/insert-mockup-watersense-history', methods=['GET'])
def insert_mockup_watersense_history():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Insert mock data into 'watersense_history' table
            sql_insert = """
            INSERT INTO watersense_history (userid, indicator, phlevel, temperature, conductivity, turbidity, orp, tds)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                '1234', '1', '5.7', '29', '3000', '4000', '5000', '6000'
            )
            cursor.execute(sql_insert, data)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Mock data inserted into 'watersense_history' table"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

## ------ watersense routes ---------------- ##
@app.route('/watersense', methods=['GET'])
def show_watersense():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Fetch all records from the 'watersense' table
            cursor.execute("SELECT * FROM watersense")
            records = cursor.fetchall()

            # Check if there are records
            if records:
                watersense_list = []
                for record in records:
                    watersense_data = {
                        "id": record[0],
                        "userid": record[1],
                        "indicator": record[2],
                        "phlevel": record[3],
                        "temperature": record[4],
                        "conductivity": record[5],
                        "turbidity": record[6],
                        "orp": record[7],
                        "tds": record[8],
                        "timestamp": record[9]
                    }
                    watersense_list.append(watersense_data)

                cursor.close()
                return jsonify({"watersense": watersense_list}), 200
            else:
                cursor.close()
                return jsonify({"message": "No records found in 'watersense' table"}), 404
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/get-watersense-by-userid/<string:userid>', methods=['GET'])
def get_watersense_by_userid(userid):
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Retrieve all records from 'watersense' by 'userid'
            sql_select = """
            SELECT * FROM watersense WHERE userid = %s
            """
            cursor.execute(sql_select, (userid,))
            records = cursor.fetchall()
            
            # Check if any records are found
            if records:
                # Return records as JSON
                return jsonify({"message": "Records fetched successfully", "data": records}), 200
            else:
                return jsonify({"message": f"No records found for userid: {userid}"}), 404
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/update-watersense-by-userid', methods=['POST'])
def update_watersense_by_userid():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get data from request body (JSON)
        request_data = request.get_json()
        
        # Extract fields from the request body
        userid = request_data.get('userid')
        indicator = request_data.get('indicator')
        phlevel = request_data.get('phlevel')
        temperature = request_data.get('temperature')
        conductivity = request_data.get('conductivity')
        turbidity = request_data.get('turbidity')
        orp = request_data.get('orp')
        tds = request_data.get('tds')

        # Ensure all necessary fields are provided
        if not userid:
            return jsonify({"error": "userid is required"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Update all records for the specified 'userid'
            sql_update = """
            UPDATE watersense
            SET indicator = %s,
                phlevel = %s,
                temperature = %s,
                conductivity = %s,
                turbidity = %s,
                orp = %s,
                tds = %s
            WHERE userid = %s
            """
            data = (indicator, phlevel, temperature, conductivity, turbidity, orp, tds, userid)
            cursor.execute(sql_update, data)
            db_connection.commit()
            cursor.close()
            
            return jsonify({"message": f"Records for userid '{userid}' updated successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/update-watersense-fixed', methods=['POST'])
def update_watersense_fixed():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get data from request body (JSON)
        request_data = request.get_json()
        
        # Fixed userid = 1234
        userid = "1234"
        indicator = request_data.get('indicator')
        phlevel = request_data.get('phlevel')
        temperature = request_data.get('temperature')
        conductivity = request_data.get('conductivity')
        turbidity = request_data.get('turbidity')
        orp = request_data.get('orp')
        tds = request_data.get('tds')

        # Ensure necessary fields are provided
        if not indicator or not phlevel or not temperature or not conductivity or not turbidity or not orp or not tds:
            return jsonify({"error": "All fields are required"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Update records for userid '1234'
            sql_update = """
            UPDATE watersense
            SET indicator = %s,
                phlevel = %s,
                temperature = %s,
                conductivity = %s,
                turbidity = %s,
                orp = %s,
                tds = %s
            WHERE userid = %s
            """
            data = (indicator, phlevel, temperature, conductivity, turbidity, orp, tds, userid)
            cursor.execute(sql_update, data)
            db_connection.commit()
            cursor.close()
            
            return jsonify({"message": f"Records for userid '1234' updated successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/update-column-by-userid', methods=['POST'])
def update_column_by_userid():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get data from request body (JSON)
        request_data = request.get_json()
        
        # Extract fields from the request body
        userid = request_data.get('userid')
        column_name = request_data.get('column_name')
        new_value = request_data.get('new_value')

        # Ensure required fields are provided
        if not userid or not column_name or new_value is None:
            return jsonify({"error": "userid, column_name, and new_value are required"}), 400
        
        # Validate if the column exists in the 'watersense' table
        valid_columns = ['indicator', 'phlevel', 'temperature', 'conductivity', 'turbidity', 'orp', 'tds']
        if column_name not in valid_columns:
            return jsonify({"error": f"Invalid column name: {column_name}. Valid columns are {valid_columns}"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Prepare SQL query to update the specified column for the given 'userid'
            sql_update = f"""
            UPDATE watersense
            SET {column_name} = %s
            WHERE userid = %s
            """
            data = (new_value, userid)
            cursor.execute(sql_update, data)
            db_connection.commit()
            cursor.close()

            return jsonify({"message": f"Column '{column_name}' for userid '{userid}' updated successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


@app.route('/update-watersense-and-history', methods=['POST'])
def update_watersense_and_history():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get data from request body (JSON)
        request_data = request.get_json()
        
        # Fixed userid = 1234
        userid = "1234"
        indicator = request_data.get('indicator')
        phlevel = request_data.get('phlevel')
        temperature = request_data.get('temperature')
        conductivity = request_data.get('conductivity')
        turbidity = request_data.get('turbidity')
        orp = request_data.get('orp')
        tds = request_data.get('tds')

        # Ensure necessary fields are provided
        if not indicator or not phlevel or not temperature or not conductivity or not turbidity or not orp or not tds:
            return jsonify({"error": "All fields are required"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Update records for userid '1234' in 'watersense' table
            sql_update = """
            UPDATE watersense
            SET indicator = %s,
                phlevel = %s,
                temperature = %s,
                conductivity = %s,
                turbidity = %s,
                orp = %s,
                tds = %s
            WHERE userid = %s
            """
            data = (indicator, phlevel, temperature, conductivity, turbidity, orp, tds, userid)
            cursor.execute(sql_update, data)
            db_connection.commit()

            # Insert the updated data into 'watersense_history' table
            sql_insert = """
            INSERT INTO watersense_history (userid, indicator, phlevel, temperature, conductivity, turbidity, orp, tds)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert, (userid, indicator, phlevel, temperature, conductivity, turbidity, orp, tds))
            db_connection.commit()

            cursor.close()

            return jsonify({"message": "Data sent successfully"}), 200
            # return jsonify({"message": "Records updated in 'watersense' and new record inserted into 'watersense_history'"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


@app.route('/fetch-watersense-history', methods=['GET'])
def fetch_watersense_history():
    try:
        # Get the period from the query parameters (if provided)
        period = request.args.get('period', None)

        # Calculate the date range based on the period
        if period:
            # Ensure the period is a valid integer (months)
            try:
                period = int(period)
            except ValueError:
                return jsonify({"error": "Invalid period value. It must be an integer."}), 400

            # Calculate the start date for the period (current date minus 'period' months)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period * 30)  # Approximate each month as 30 days
            date_filter = f"AND timestamp >= '{start_date.strftime('%Y-%m-%d %H:%M:%S')}'"
        else:
            date_filter = ""  # No filter, return all data

        # Query the 'watersense_history' table
        sql_query = f"""
        SELECT * FROM watersense_history
        WHERE 1 {date_filter}
        ORDER BY timestamp DESC
        """
        
        cursor = get_cursor()
        if cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Get column names from cursor description
            cursor.close()

            # Format the result to match the required output
            formatted_result = [
                dict(zip(columns, row))  # Map column names to the corresponding values in the row
                for row in result
            ]

            # Format the timestamp to the required format
            for entry in formatted_result:
                entry["timestamp"] = entry["timestamp"].strftime("%a, %d %b %Y %H:%M:%S GMT")
            
            return jsonify(formatted_result), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/delete-old-watersense-history', methods=['GET'])
def delete_old_watersense_history():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Step 1: Get the IDs of the latest 20 records
            sql_latest_20 = """
            SELECT id FROM watersense_history
            ORDER BY timestamp DESC
            LIMIT 20
            """
            cursor.execute(sql_latest_20)
            latest_20_ids = [row["id"] for row in cursor.fetchall()]
            
            if not latest_20_ids:
                return jsonify({"message": "No records found in the watersense_history table"}), 200

            # Step 2: Delete all records except the latest 20
            # We'll delete records whose id is not in the list of latest 20 IDs
            ids_to_delete = tuple(latest_20_ids)
            sql_delete = f"""
            DELETE FROM watersense_history
            WHERE id NOT IN {ids_to_delete}
            """
            cursor.execute(sql_delete)
            db_connection.commit()
            cursor.close()
            
            return jsonify({"message": "Old records deleted, keeping the latest 20 records"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)



## ------ users routes ---------------- ##

## show the all the records of table 'users'
@app.route('/users', methods=['GET'])
def show_users():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Fetch all records from the 'users' table
            cursor.execute("SELECT * FROM users")
            records = cursor.fetchall()

            # Check if there are records
            if records:
                users_list = []
                for record in records:
                    user = {
                        "id": record[0],
                        "userId": record[1],
                        "passwordHash": record[2],
                        "fingerPrintId": record[3],
                        "role": record[4],
                        "groupId": record[5],
                        "email": record[6],
                        "lockerAssigned": record[7],
                        "status": record[8],
                        "token": record[9],
                        "resetCode": record[10],
                        "timestamp": record[11]
                    }
                    users_list.append(user)

                cursor.close()
                return jsonify({"users": users_list}), 200
            else:
                cursor.close()
                return jsonify({"message": "No records found in 'users' table"}), 404
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

## adding the new user
@app.route('/users/add', methods=['POST'])
def add_user():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if all required fields are provided
        required_fields = ['userId', 'passwordHash', 'fingerPrintId', 'role', 'groupId', 'email', 'lockerAssigned', 'status', 'token', 'resetCode']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = get_cursor()
        if cursor:
            # Check if the userId already exists in the 'users' table
            sql_check = "SELECT id FROM users WHERE userId = %s"
            cursor.execute(sql_check, (data['userId'],))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                return jsonify({"error": "User with this userId already exists"}), 400
            
            # Insert the new user into the 'users' table if userId does not exist
            sql_insert = """
            INSERT INTO users (userId, passwordHash, fingerPrintId, role, groupId, email, lockerAssigned, status, token, resetCode)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Prepare the data for insertion without the timestamp
            data_values = (
                data['userId'],
                data['passwordHash'],
                data['fingerPrintId'],
                data['role'],
                data['groupId'],
                data['email'],
                data['lockerAssigned'],
                data['status'],
                data['token'],
                data['resetCode']
            )

            cursor.execute(sql_insert, data_values)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "New user added successfully"}), 201

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

## adding the validate user
@app.route('/users/validate', methods=['POST'])
def validate_user():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'userId' and 'passwordHash' are provided in the request
        if 'userId' not in data or 'passwordHash' not in data:
            return jsonify({"error": "Missing 'userId' or 'passwordHash'"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Query to find the first match of 'userId' and 'passwordHash'
            sql_query = """
            SELECT role, fingerPrintId, groupId, status FROM users 
            WHERE userId = %s AND passwordHash = %s
            LIMIT 1
            """
            cursor.execute(sql_query, (data['userId'], data['passwordHash']))
            result = cursor.fetchone()

            if result:
                # If user is found, return relevant details
                user_info = {
                    "message": "User validated successfully",
                    "role": result[0],
                    "fingerPrintId": result[1],
                    "groupId": result[2],
                    "status": result[3]
                }
                cursor.close()
                return jsonify(user_info), 200
            else:
                cursor.close()
                return jsonify({"error": "Invalid 'userId' or 'passwordHash'"}), 401
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/validate-active', methods=['POST'])
def validate_user_active():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'userId' and 'passwordHash' are provided in the request
        if 'userId' not in data or 'passwordHash' not in data:
            return jsonify({"error": "Missing 'userId' or 'passwordHash'"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Query to find the first match of 'userId', 'passwordHash', and 'status' = 'active'
            sql_query = """
            SELECT role, fingerPrintId, groupId, status FROM users 
            WHERE userId = %s AND passwordHash = %s AND status = 'active'
            LIMIT 1
            """
            cursor.execute(sql_query, (data['userId'], data['passwordHash']))
            result = cursor.fetchone()

            if result:
                # If user is found and status is active, return relevant details
                user_info = {
                    "message": "User validated successfully",
                    "role": result[0],
                    "fingerPrintId": result[1],
                    "groupId": result[2],
                    "status": result[3]
                }
                cursor.close()
                return jsonify(user_info), 200
            else:
                cursor.close()
                return jsonify({"error": "Invalid 'userId' or 'passwordHash', or user is not active"}), 401
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

## update password by userId
@app.route('/users/update-password/', methods=['PUT'])
def update_password():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if all required fields are provided
        if 'userId' not in data or 'password_hash' not in data or 'new_password_hash' not in data:
            return jsonify({"error": "Missing required fields: 'userId', 'password_hash', or 'new_password_hash'"}), 400

        cursor = get_cursor()
        if cursor:
            # Query to check if the user exists with the provided userId and password_hash
            sql_check = "SELECT id FROM users WHERE userId = %s AND passwordHash = %s"
            cursor.execute(sql_check, (data['userId'], data['password_hash']))
            user = cursor.fetchone()

            if user:
                # If user is found, update the passwordHash
                sql_update = """
                UPDATE users 
                SET passwordHash = %s
                WHERE userId = %s
                """
                cursor.execute(sql_update, (data['new_password_hash'], data['userId']))
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "Password updated successfully"}), 200
            else:
                cursor.close()
                return jsonify({"error": "Invalid 'userId' or 'password_hash'"}), 401
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

## delete records by userId
@app.route('/users/delete/', methods=['DELETE'])
def delete_user():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'userId' is provided in the request
        if 'userId' not in data:
            return jsonify({"error": "Missing required field: 'userId'"}), 400

        cursor = get_cursor()
        if cursor:
            # Query to check if the user exists with the provided userId
            sql_check = "SELECT id FROM users WHERE userId = %s"
            cursor.execute(sql_check, (data['userId'],))
            user = cursor.fetchone()

            if user:
                # If user exists, delete the user by userId
                sql_delete = "DELETE FROM users WHERE userId = %s"
                cursor.execute(sql_delete, (data['userId'],))
                db_connection.commit()
                cursor.close()
                return jsonify({"message": "User deleted successfully"}), 200
            else:
                cursor.close()
                return jsonify({"error": "User with the provided 'userId' does not exist"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

## validate fingerPrintId
@app.route('/users/validate/fingerprint-id', methods=['POST'])
def validate_fingerprint():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'fingerPrintId' is provided in the request
        if 'fingerPrintId' not in data:
            return jsonify({"error": "Missing required field: 'fingerPrintId'"}), 400

        cursor = get_cursor()
        if cursor:
            # Query to find the first match of 'fingerPrintId'
            sql_query = """
            SELECT userId, lockerAssigned, role, groupId, status FROM users 
            WHERE fingerPrintId = %s
            LIMIT 1
            """
            cursor.execute(sql_query, (data['fingerPrintId'],))
            result = cursor.fetchone()

            if result:
                # If a match is found, return relevant details
                user_info = {
                    "message": "Fingerprint validated successfully",
                    "userId": result[0],
                    "lockerAssigned": result[1],
                    "role": result[2],
                    "groupId": result[3],
                    "status": result[4]
                }
                cursor.close()
                return jsonify(user_info), 200
            else:
                cursor.close()
                return jsonify({"error": "No matching fingerprint found"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

## unlock by fingerPrintId
@app.route('/users/unlock-by/fingerprint-id', methods=['POST'])
def unlock_locker():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'fingerPrintId' is provided in the request
        if 'fingerPrintId' not in data:
            return jsonify({"error": "Missing required field: 'fingerPrintId'"}), 400

        cursor = get_cursor()
        if cursor:
            # Query to check if 'fingerPrintId' exists and has 'active' status
            sql_query = """
            SELECT userId, lockerAssigned, status FROM users 
            WHERE fingerPrintId = %s AND status = 'active'
            LIMIT 1
            """
            cursor.execute(sql_query, (data['fingerPrintId'],))
            user = cursor.fetchone()

            if user:
                # If user found and status is 'active', proceed to unlock locker
                locker_assigned = user[1]

                # Check if the locker column exists in the 'store' table
                cursor.execute(f"SHOW COLUMNS FROM store LIKE %s", (locker_assigned,))
                column_exists = cursor.fetchone()

                if column_exists:
                    # Update the locker in the 'store' table to 'unlock'
                    sql_update = f"UPDATE store SET {locker_assigned} = 'unlock' WHERE id = 1"
                    cursor.execute(sql_update)
                    db_connection.commit()
                    cursor.close()
                    return jsonify({"message": f"Locker '{locker_assigned}' unlocked successfully"}), 200
                else:
                    cursor.close()
                    return jsonify({"error": f"Column '{locker_assigned}' does not exist in the 'store' table"}), 400
            else:
                cursor.close()
                return jsonify({"error": "No active user found with the provided fingerprint"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/group/locker-assign', methods=['POST'])
def locker_assign():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if groupId and lockerAssignedForAll are provided
        if 'groupId' not in data or 'lockerAssignedForAll' not in data:
            return jsonify({"error": "Missing required fields: groupId and lockerAssignedForAll"}), 400
        
        groupId = data['groupId']
        lockerAssignedForAll = data['lockerAssignedForAll']

        cursor = get_cursor()
        if cursor:
            # First, collect all records from the users table with the specified groupId and status "active"
            cursor.execute("SELECT * FROM users WHERE groupId = %s AND status = 'active'", (groupId,))
            active_records = cursor.fetchall()

            if not active_records:
                cursor.close()
                return jsonify({"error": "No active users found for the given groupId"}), 404
            
            # Update the lockerAssigned value for all matching records in the users table
            sql_update_locker = """
            UPDATE users
            SET lockerAssigned = %s
            WHERE groupId = %s AND status = 'active'
            """
            cursor.execute(sql_update_locker, (lockerAssignedForAll, groupId))
            db_connection.commit()
            cursor.close()

            # Return response with the message
            return jsonify({"message": f"Locker assigned successfully for all active users in group {groupId}"}), 200

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/users/group/by-userid', methods=['POST'])
def update_group_by_userid():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if userId and new_groupId are provided
        if 'userId' not in data or 'new_groupId' not in data:
            return jsonify({"error": "Missing required fields: userId and new_groupId"}), 400
        
        userId = data['userId']
        new_groupId = data['new_groupId']

        cursor = get_cursor()
        if cursor:
            # First, look for the record with the given userId in the users table
            cursor.execute("SELECT * FROM users WHERE userId = %s", (userId,))
            existing_user = cursor.fetchone()

            if not existing_user:
                cursor.close()
                return jsonify({"error": "User not found"}), 404

            # Update the groupId for the given userId in the users table
            sql_update_group = """
            UPDATE users
            SET groupId = %s
            WHERE userId = %s
            """
            cursor.execute(sql_update_group, (new_groupId, userId))
            db_connection.commit()
            cursor.close()

            # Return response with the message
            return jsonify({"message": f"Group ID updated successfully for userId {userId}"}), 200

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/status/by-userid', methods=['POST'])
def update_status_by_userid():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if userId and new_status are provided
        if 'userId' not in data or 'new_status' not in data:
            return jsonify({"error": "Missing required fields: userId and new_status"}), 400
        
        userId = data['userId']
        new_status = data['new_status']

        cursor = get_cursor()
        if cursor:
            # First, look for the record with the given userId in the users table
            cursor.execute("SELECT * FROM users WHERE userId = %s", (userId,))
            existing_user = cursor.fetchone()

            if not existing_user:
                cursor.close()
                return jsonify({"error": "User not found"}), 404

            # Update the status for the given userId in the users table
            sql_update_status = """
            UPDATE users
            SET status = %s
            WHERE userId = %s
            """
            cursor.execute(sql_update_status, (new_status, userId))
            db_connection.commit()
            cursor.close()

            # Return response with the message
            return jsonify({"message": f"Status updated successfully for userId {userId}"}), 200

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/verify', methods=['GET'])
def verify_user_token():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        # Get the query parameters (token and userId)
        token = request.args.get('token')
        userId = request.args.get('userId')

        if not token or not userId:
            return jsonify({"error": "Missing required query parameters: token and userId"}), 400
        
        cursor = get_cursor()
        if cursor:
            # Look for the record with the given userId and status "inactive"
            cursor.execute("SELECT * FROM users WHERE userId = %s AND status = 'inactive'", (userId,))
            user = cursor.fetchone()

            if not user:
                cursor.close()
                return jsonify({"error": "User not found or user is not inactive"}), 404

            # Compare the token from query parameter with the token stored in the database for that userId
            stored_token = user[9]  # Assuming 'token' is in the 10th column (index 9) of the 'users' table

            if token != stored_token:
                cursor.close()
                return jsonify({"error": "Invalid token"}), 401

            # Update the status to "active" if token matches
            sql_update_status = """
            UPDATE users
            SET status = 'active'
            WHERE userId = %s
            """
            cursor.execute(sql_update_status, (userId,))
            db_connection.commit()
            cursor.close()

            # Return a success message if the token matches and the status is updated
            return jsonify({"message": f"Token verified successfully and status updated to 'active' for userId {userId}"}), 200

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/users/resetcode', methods=['POST'])
def reset_password():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'userId', 'resetCode', and 'new_password' are provided in the request
        if 'userId' not in data or 'resetCode' not in data or 'new_password' not in data:
            return jsonify({"error": "Missing required fields: userId, resetCode, or new_password"}), 400
        
        userId = data['userId']
        resetCode = data['resetCode']
        new_password = data['new_password']

        cursor = get_cursor()
        if cursor:
            # Query to find the user with the given userId and resetCode
            sql_query = """
            SELECT resetCode FROM users 
            WHERE userId = %s
            LIMIT 1
            """
            cursor.execute(sql_query, (userId,))
            result = cursor.fetchone()

            if result:
                # Check if the resetCode matches
                if result[0] == resetCode:
                    # Update the password for the user
                    sql_update_password = """
                    UPDATE users
                    SET passwordHash = %s
                    WHERE userId = %s
                    """
                    cursor.execute(sql_update_password, (new_password, userId))
                    db_connection.commit()
                    cursor.close()

                    # Return response with the message
                    return jsonify({"message": "Password reset successfully"}), 200
                else:
                    cursor.close()
                    return jsonify({"error": "Invalid reset code"}), 400
            else:
                cursor.close()
                return jsonify({"error": "User not found"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/user/forgot-password', methods=['POST'])
def forgot_password():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'userId' and 'email' are provided in the request
        if 'userId' not in data or 'email' not in data:
            return jsonify({"error": "Missing required fields: userId or email"}), 400
        
        userId = data['userId']
        email = data['email']

        # Generate a random reset code (6 digits for simplicity)
        resetCode = ''.join(random.choices(string.digits, k=6))

        cursor = get_cursor()
        if cursor:
            # Query to find the user with the given userId and email
            sql_query = """
            SELECT email FROM users 
            WHERE userId = %s
            LIMIT 1
            """
            cursor.execute(sql_query, (userId,))
            result = cursor.fetchone()

            if result:
                # Check if the email matches
                if result[0] == email:
                    # Update the resetCode for the user
                    sql_update_reset_code = """
                    UPDATE users
                    SET resetCode = %s
                    WHERE userId = %s
                    """
                    cursor.execute(sql_update_reset_code, (resetCode, userId))
                    db_connection.commit()
                    cursor.close()

                    # Return response with the message and email
                    return jsonify({"message": "Reset code generated successfully", "email": email}), 200
                else:
                    cursor.close()
                    return jsonify({"error": "Email does not match the userId"}), 400
            else:
                cursor.close()
                return jsonify({"error": "User not found"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## ------- profile route ----------------##

@app.route('/profile', methods=['GET'])
def get_all_profiles():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Fetch all records from the 'profile' table
            cursor.execute("SELECT * FROM profile")
            profiles = cursor.fetchall()

            if not profiles:
                cursor.close()
                return jsonify({"message": "No profiles found"}), 404

            # Format the results into a list of dictionaries
            profile_list = []
            for profile in profiles:
                profile_dict = {
                    "id": profile[0],
                    "userId": profile[1],
                    "firstName": profile[2],
                    "lastName": profile[3],
                    "suffix": profile[4],
                    "contactNumber": profile[5],
                    "email": profile[6],
                    "address": profile[7],
                    "birthday": profile[8],
                    "photoURL": profile[9],
                    "timestamp": profile[10]
                }
                profile_list.append(profile_dict)

            cursor.close()

            return jsonify({"profiles": profile_list}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/profile/add', methods=['POST'])
def add_profile():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if all required fields are provided
        required_fields = ['userId', 'firstName', 'lastName', 'contactNumber', 'email', 'address', 'birthday', 'photoURL']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400

        cursor = get_cursor()
        if cursor:
            # Check if the userId already exists
            cursor.execute("SELECT * FROM profile WHERE userId = %s", (data['userId'],))
            existing_profile = cursor.fetchone()

            if existing_profile:
                cursor.close()
                return jsonify({"error": "userId already exists, cannot add a new profile with this userId"}), 400

            # Insert the new profile record into the 'profile' table
            sql_insert = """
            INSERT INTO profile (userId, firstName, lastName, suffix, contactNumber, email, address, birthday, photoURL)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            # Prepare the data for insertion
            data_values = (
                data['userId'],
                data['firstName'],
                data['lastName'],
                data.get('suffix', None),  # optional field
                data['contactNumber'],
                data['email'],
                data['address'],
                data['birthday'],
                data['photoURL']
            )

            cursor.execute(sql_insert, data_values)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Profile added successfully"}), 201

        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/profile/update', methods=['PUT'])
def update_profile():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Extract the data from the request body
            data = request.get_json()
            userId = data.get("userId")
            
            if not userId:
                return jsonify({"error": "userId is required"}), 400

            # Check if the userId exists in the table
            cursor.execute("SELECT * FROM profile WHERE userId = %s", (userId,))
            existing_profile = cursor.fetchone()

            if not existing_profile:
                cursor.close()
                return jsonify({"error": "User not found"}), 404

            # Get the fields from the request body or use existing values if not provided
            firstName = data.get("firstName", existing_profile[2])
            lastName = data.get("lastName", existing_profile[3])
            suffix = data.get("suffix", existing_profile[4])
            contactNumber = data.get("contactNumber", existing_profile[5])
            email = data.get("email", existing_profile[6])
            address = data.get("address", existing_profile[7])
            birthday = data.get("birthday", existing_profile[8])
            photoURL = data.get("photoURL", existing_profile[9])

            # Define SQL query to update the first matching record
            sql_update_profile = """
            UPDATE profile
            SET firstName = %s, lastName = %s, suffix = %s, contactNumber = %s, 
                email = %s, address = %s, birthday = %s, photoURL = %s
            WHERE userId = %s
            LIMIT 1
            """
            cursor.execute(sql_update_profile, (firstName, lastName, suffix, contactNumber, email, address, birthday, photoURL, userId))
            db_connection.commit()
            cursor.close()

            return jsonify({"message": "Profile updated successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/profile/delete', methods=['DELETE'])
def delete_profile():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Extract the userId from the request body
            data = request.get_json()
            userId = data.get("userId")
            
            if not userId:
                return jsonify({"error": "userId is required"}), 400

            # Check if the userId exists in the table
            cursor.execute("SELECT * FROM profile WHERE userId = %s", (userId,))
            existing_profile = cursor.fetchone()

            if not existing_profile:
                cursor.close()
                return jsonify({"error": "User not found"}), 404

            # Define SQL query to delete only the first matching record
            sql_delete_profile = "DELETE FROM profile WHERE userId = %s LIMIT 1"
            cursor.execute(sql_delete_profile, (userId,))
            db_connection.commit()
            cursor.close()

            return jsonify({"message": "Profile deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


## ------ stores routes ---------------- ##

@app.route('/stores', methods=['GET'])
def get_all_stores():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Query to fetch all records from the 'store' table
            sql_query = "SELECT * FROM store"
            cursor.execute(sql_query)
            stores = cursor.fetchall()

            # Prepare the response
            if stores:
                # If there are stores, return them
                stores_list = []
                for store in stores:
                    store_data = {
                        "id": store[0],
                        "lockerId": store[1],
                        "locker1": store[2],
                        "locker2": store[3],
                        "locker3": store[4]
                    }
                    stores_list.append(store_data)
                cursor.close()
                return jsonify(stores_list), 200
            else:
                cursor.close()
                return jsonify({"message": "No stores found"}), 404
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stores/update-locker', methods=['PUT'])
def update_locker():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        # Get the data from the request (expecting JSON)
        data = request.get_json()

        # Check if 'lockerName' and 'newValue' are provided in the request
        if 'lockerName' not in data or 'newValue' not in data:
            return jsonify({"error": "Missing required fields: 'lockerName' or 'newValue'"}), 400
        
        locker_name = data['lockerName']
        new_value = data['newValue']

        # Check if the lockerName is valid
        if locker_name not in ['locker1', 'locker2', 'locker3']:
            return jsonify({"error": "Invalid lockerName, must be 'locker1', 'locker2', or 'locker3'"}), 400

        cursor = get_cursor()
        if cursor:
            # Check if the column exists in the store table
            cursor.execute(f"SHOW COLUMNS FROM store LIKE %s", (locker_name,))
            column_exists = cursor.fetchone()

            if column_exists:
                # Update the specified locker column with the new value
                sql_update = f"UPDATE store SET {locker_name} = %s WHERE id = 1"
                cursor.execute(sql_update, (new_value,))
                db_connection.commit()
                cursor.close()
                return jsonify({"message": f"Locker '{locker_name}' updated successfully to '{new_value}'"}), 200
            else:
                cursor.close()
                return jsonify({"error": f"Column '{locker_name}' does not exist in the 'store' table"}), 400
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/stores/lock-all', methods=['GET'])
def lock_all_lockers():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # Update all lockers (locker1, locker2, locker3) to 'locked'
            sql_update = """
            UPDATE store 
            SET locker1 = 'locked', locker2 = 'locked', locker3 = 'locked'
            WHERE id = 1
            """
            cursor.execute(sql_update)
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "All lockers (locker1, locker2, locker3) are now locked"}), 200
        
        else:
            return jsonify({"error": "Database connection not available"}), 500

    except mysql.connector.Error as e:
        return handle_mysql_error(e)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


## ------ notifications routes ---------------- ##

@app.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # SQL query to select all notifications
            cursor.execute("SELECT * FROM notifications")
            notifications = cursor.fetchall()
            
            # If no notifications exist
            if not notifications:
                return jsonify({"message": "No notifications found"}), 200
            
            # Convert results into a list of dictionaries
            result = []
            for notification in notifications:
                result.append({
                    "id": notification[0],
                    "userId": notification[1],
                    "role": notification[2],
                    "status": notification[3],
                    "message": notification[4],
                    "timestamp": notification[5]
                })
            cursor.close()
            return jsonify(result), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/notifications/add', methods=['POST'])
def add_notification():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')
        role = data.get('role')
        status = data.get('status')
        message = data.get('message')

        # Validate the required fields
        if not user_id or not role or not status or not message:
            return jsonify({"error": "Missing required fields"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to insert the new notification
            sql_insert_notification = """
            INSERT INTO notifications (userId, role, status, message)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_insert_notification, (user_id, role, status, message))
            db_connection.commit()
            cursor.close()
            return jsonify({"message": "Notification added successfully"}), 201
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/notifications/by-user-id', methods=['POST'])
def get_notifications_by_user():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')
        role = data.get('role')
        status = data.get('status')

        # Validate the required fields
        if not user_id or not role or status != "new":
            return jsonify({"error": "Missing required fields or status is not 'new'"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to select notifications for the given user, role, and new status, ordered by timestamp
            sql_select_notifications = """
            SELECT message, timestamp 
            FROM notifications 
            WHERE userId = %s AND role = %s AND status = %s 
            ORDER BY timestamp DESC
            """
            cursor.execute(sql_select_notifications, (user_id, role, status))
            notifications = cursor.fetchall()

            # If no notifications are found
            if not notifications:
                return jsonify({"message": "No notifications found for the given user with status 'new'"}), 200
            
            # Format the response
            result = []
            for notification in notifications:
                result.append({
                    "msg": notification[0],  
                    "timestamp": notification[1]
                })
            cursor.close()
            return jsonify(result), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/notifications/update/by-user-id', methods=['POST'])
def update_notifications_status():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')
        status = data.get('status')

        # Validate the required fields
        if not user_id or not status:
            return jsonify({"error": "Missing required fields"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to update the status of all notifications for the given userId
            sql_update_status = """
            UPDATE notifications 
            SET status = %s 
            WHERE userId = %s
            """
            cursor.execute(sql_update_status, (status, user_id))
            db_connection.commit()
            cursor.close()
            
            return jsonify({"message": f"Status of all notifications for userId '{user_id}' updated successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


## ------ activity routes ---------------- ##

@app.route('/activity', methods=['GET'])
def get_all_activities():
    try:
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
        
        cursor = get_cursor()
        if cursor:
            # SQL query to select all activities
            cursor.execute("SELECT * FROM activity")
            activities = cursor.fetchall()

            # If no activities exist
            if not activities:
                return jsonify({"message": "No activities found"}), 200

            # Format the response
            result = []
            for activity in activities:
                result.append({
                    "id": activity[0],
                    "userId": activity[1],
                    "role": activity[2],
                    "status": activity[3],
                    "type": activity[4],
                    "info": activity[5],
                    "timestamp": activity[6]
                })
            cursor.close()
            return jsonify(result), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/activity/add', methods=['POST'])
def add_activity():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')
        role = data.get('role')
        status = data.get('status')
        activity_type = data.get('type')
        info = data.get('info')

        # Validate the required fields
        if not user_id or not role or not status or not activity_type or not info:
            return jsonify({"error": "Missing required fields"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to insert a new activity record
            sql_insert_activity = """
            INSERT INTO activity (userId, role, status, type, info)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql_insert_activity, (user_id, role, status, activity_type, info))
            db_connection.commit()
            cursor.close()
            
            return jsonify({
                "message": "Activity added successfully",
                "userId": user_id,
                "role": role,
                "status": status,
                "type": activity_type,
                "info": info
            }), 201
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/activity/by-user-id', methods=['POST'])
def get_activities_by_user_id():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')

        # Validate the required fields
        if not user_id:
            return jsonify({"error": "Missing 'userId' in request"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to select all activities for the given userId, ordered by timestamp (latest to oldest)
            sql_select_activities = """
            SELECT * FROM activity
            WHERE userId = %s
            ORDER BY timestamp DESC
            """
            cursor.execute(sql_select_activities, (user_id,))
            activities = cursor.fetchall()

            # If no activities exist for the given userId
            if not activities:
                return jsonify({"message": f"No activities found for userId '{user_id}'"}), 200

            # Format the response
            result = []
            for activity in activities:
                result.append({
                    "id": activity[0],
                    "userId": activity[1],
                    "role": activity[2],
                    "status": activity[3],
                    "type": activity[4],
                    "info": activity[5],
                    "timestamp": activity[6]
                })
            cursor.close()
            return jsonify(result), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)

@app.route('/activity/delete/by-user-id', methods=['DELETE'])
def delete_activities_by_user_id():
    try:
        # Get data from the request
        data = request.get_json()
        user_id = data.get('userId')

        # Validate the required fields
        if not user_id:
            return jsonify({"error": "Missing 'userId' in request"}), 400
        
        if not is_mysql_available():
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500

        cursor = get_cursor()
        if cursor:
            # SQL query to delete all activities for the given userId
            sql_delete_activities = """
            DELETE FROM activity
            WHERE userId = %s
            """
            cursor.execute(sql_delete_activities, (user_id,))
            db_connection.commit()
            cursor.close()
            
            return jsonify({"message": f"All activities for userId '{user_id}' have been deleted successfully"}), 200
        else:
            return jsonify({"error": "Database connection not available"}), 500
    except mysql.connector.Error as e:
        return handle_mysql_error(e)


# Route to reconnect to MySQL
@app.route('/reconnect-mysql', methods=['GET'])
def reconnect_mysql():
    if reconnect_to_mysql():
        return jsonify({"message": "Reconnected to MySQL successfully!"}), 200
    else:
        return jsonify({"error": "Failed to reconnect to MySQL."}), 500

# Check if the file "dev" exists
if not os.path.exists('dev'):
    # Execute this route if "dev" is not present and MySQL is available
    @app.route('/', methods=['GET'])
    def index():
        if is_mysql_available():
            return jsonify({
                "message": {
                    "status": "ok",
                    "developer": "kayven",
                    "email": "yvendee2020@gmail.com"
                }
            })
        else:
            return jsonify({"error": "MySQL database not responding, please check the database service"}), 500
else:
    # Execute this route if "dev" exists
    @app.route('/', methods=['GET'])
    def index():
        return jsonify({"message": "Welcome to the parcelpoint API"})

# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({"message": "Welcome to the appfinity API"})

@app.route("/ui")
def ui():
    # Render the HTML template for the /ui route
    return render_template("index.html")

@app.route("/history")
def history():
    # Render the HTML template for the /history route
    return render_template("history.html")

@app.route("/history-preview")
def history_preview():
    # Render the HTML template for the /history route
    return render_template("history-preview.html")

if __name__ == '__main__':
    app.run(debug=True)
