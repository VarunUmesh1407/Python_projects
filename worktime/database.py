import mysql.connector

class Worktimedb:
    host = "localhost"
    username = "root"
    password = "password"
    database = "worktime_database"

    def __init__(self):
        self.connection = None

    def connect(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.username,
            password=self.password,
            database=self.database
        )
        return self.connection

    def close(self):
        if self.connection:
            self.connection.close()

    def execute_query(self, query, parameters=None):
        cursor = self.connection.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchone()
        cursor.close()
        return result

    def commit(self):
        self.connection.commit()

