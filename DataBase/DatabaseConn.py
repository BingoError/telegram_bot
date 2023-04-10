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
            
            
    def checkPortfolio(self, username):
        self.cursor.execute(f"SELECT id FROM users WHERE nick_name = '{username}' ")
        res = self.cursor.fetchone()
        self.conn.commit()
       
       
        self.cursor.execute(f"SELECT * FROM user_coins WHERE user_id = {res[0]}")
        query = self.cursor.fetchone()
        self.conn.commit()
        
        if query == None:
            return False
        return True
        
    def add_user(self, username):
       self.id = self.queryToDatabase("users", "nick_name", username)
       return self.id
       

    def add_coin(self, coin):
        self.id = self.queryToDatabase("coins", "name_coin", coin)
        return self.id
    
    def get_coin_name(self ,coin_id):
        coin_name = self.execute_connector(f"SELECT name_coin FROM coins WHERE id={coin_id}")      
        return coin_name[0][0]

        
    def add_to_portfolio(self, user_id, coin_id, quantity):
        insert_query = f"INSERT INTO user_coins (user_id, coin_id, quantity) VALUES ({user_id}, {coin_id}, {quantity})"
        self.cursor.execute(insert_query)
        self.conn.commit()
    
    def getPortfolio(self, user_id):       
        
        insert_query = f"SELECT user_id , coin_id, quantity FROM user_coins WHERE user_id = {user_id};"
        res = self.execute_connector(insert_query)
               
        coin_list = []
        for r in res:
            coin_id = r[1]
            quantity = r[2]
            name = self.get_coin_name(coin_id)
            coin_list.append([name, quantity])

        self.conn.commit()
        return coin_list
       
    def update_portfolio(self, coin_id, user_id):
        insert_query = f"DELETE FROM user_coins WHERE coin_id = {coin_id} AND user_id = {user_id};"
        self.cursor.execute(insert_query)
        self.conn.commit()
    
    def delete_to_portfolio(self, user_id, coin_id, quantity):
        select_query = f"SELECT CAST(SUM(quantity) AS DECIMAL(16,5)) AS total_quantity FROM user_coins WHERE user_id = {user_id} AND coin_id = {coin_id};"
        res = self.execute_connector(select_query)
        total_quantity = float(res[0][0]) if res and res[0] and res[0][0] else 0.0
        new_quantity = total_quantity - float(quantity)
       
        insert_query = f"DELETE FROM user_coins WHERE coin_id = {coin_id} AND user_id = {user_id};"
        self.cursor.execute(insert_query)
        self.conn.commit()
       
        self.add_to_portfolio(user_id, coin_id, new_quantity)
        return new_quantity
        
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

            

        
        
        