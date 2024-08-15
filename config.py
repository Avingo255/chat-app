import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #DATABASE_CONNECTION_STRING = os.environ.get('CONNECTION_STRING') or "mysql+pymysql://avinash:M%40cr03c0n0m1c5@chatapp-database-mysql-server.mysql.database.azure.com:3306/database1"