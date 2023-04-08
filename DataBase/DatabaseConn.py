import psycopg2 
import configparser


class PostgreSQL():
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.db_name  = self.config['postgresql']['DB_NAME']
        self.user     = self.config['postgresql']['USER']
        self.password = self.config['postgresql']['PASSWORD']
        self.conn = None
        self.cursor = None
        self.id = 0
    
    def connect(self):
        try:
            self.conn  = psycopg2.connect(
                dbname=self.db_name,
                user = self.user,
                password = self.password,
                # host = self.host,
                # port = self.port
            )
            self.cursor = self.conn.cursor()
            print("Connected to PostgreSQL database!")
            
        except psycopg2.Error as e:
            print("Unable to connect to database")
            print(e)

    def execute_connector(self, query):
        try: 
            self.cursor.execute(query)
            self.conn.commit()
            
            rows = self.cursor.fetchall()
            return rows      
                             
        except psycopg2.Error as e:
            print("Erorr execute ")
            print (e)
            return []
            
    def add_user(self, username):
       self.id = self.queryToDatabase("users", "nick_name", username)
       return self.id
       

    def add_coin(self, coin):
        self.id = self.queryToDatabase("coins", "name_coin", coin)
        return self.id
    
        
    def add_to_portfolio(self, user_id, coin_id, quantity):
        insert_query = f"INSERT INTO user_coins (user_id, coin_id, quantity) VALUES ({user_id}, {coin_id}, {quantity})"
        self.cursor.execute(insert_query)
        self.conn.commit()
       
    
    def close_connection(self):
        self.sort()        
        if self.cursor:
            self.cursor.close()            
        if self.conn:
            self.conn.close()
        print("connection close")
        
    def sort(self):
        sort = "SELECT * FROM user_coins ORDER BY user_id ASC"
        self.execute_connector(sort)
   
    def queryToDatabase(self, tableName, nameofRow, data):
        query = f"SELECT * FROM {tableName} WHERE {nameofRow} = '{data}'"
        existing_users = self.execute_connector(query)
        
        if not existing_users:
            query = f"INSERT INTO {tableName} ({nameofRow}) VALUES ('{data}') RETURNING id "
            res = self.execute_connector(query)
            return res[0][0] if res else None

        return existing_users[0][0] if existing_users else None

            

        
        
        