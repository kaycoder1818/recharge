from flask import Flask, jsonify, request, render_template
import mysql.connector
import os
from swagger.swaggerui import setup_swagger
import random
import string
from datetime import datetime, timedelta

app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/static')

# Set up Swagger
setup_swagger(app)

# Global database connection
db_connection = None

def get_connection():
    global db_connection
    try:
        if db_connection is None or not db_connection.is_connected():
            mysql_details = os.getenv('MYSQL_DETAILS')
            if not mysql_details:
                print("MYSQL_DETAILS environment variable is not set.")
                return None

            # Split the details by "@"
            details = mysql_details.split('@')
            if len(details) != 5:
                print("Invalid MYSQL_DETAILS format")
                return None

            # Extract the individual values
            host = details[0]
            user = details[1]
            password = details[2]
            database = details[3]
            port = int(details[4])

            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
        return db_connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

def get_cursor():
    connection = get_connection()
    if connection:
        return connection.cursor()
    return None

def cleanup_connection(connection):
    try:
        if connection and connection.is_connected():
            connection.close()
    except:
        pass

# Initialize database connection
if not os.path.exists('dev'):
    get_connection()

def generate_random_string(length=32):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# ... existing code ...
