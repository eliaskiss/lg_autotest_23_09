import pymysql
from icecream import ic
import sys

ic.configureOutput(includeContext=True)

# SQL Tutorial
# https://www.w3schools.com/sql/sql_where.asp
# https://www.tutorialspoint.com/sql/sql-create-table.htm

class Database:
    def __init__(self, host, user, passwd, db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

        self.conn = None
        self.cursor = None

    ################################################
    # Connect DB
    ################################################
    def connect_db(self):
        try:
            if self.conn is None:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd, db=self.db, charset='utf8')

                # id, reg_datetime, name, age ==> row[0], row[1], row[2], row[3]
                # self.cursor = self.conn.cursor()

                # id, reg_datetime, name, age ==> row['id'], row['reg_datetime'], row['name'], row['age']
                self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
            ic('DB is connected')
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Execute Only
    ################################################
    def execute_only(self, sql, values=None):
        try:
            # 'select * from elias;'
            # 'select * form elias where name = "elias" and age = 20;'
            # sql = 'select * form elias where name = %s and age = %s;'
            # values = ('elias', 20)
            if values is None:
                self.cursor.execute(sql)
            else:
                self.cursor.execute(sql, values)
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Execute  and Commit
    ################################################
    def execute_and_commit(self, sql, values=None):
        try:
            self.execute_only(sql, values)
            self.conn.commit()
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Commit Only
    ################################################
    def commit_only(self):
        try:
            self.conn.commit()
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Execute and Return All
    ################################################
    def execute_and_return(self, sql, values=None):
        try:
            self.execute_only(sql, values)
            data_list = self.cursor.fetchall()
            return data_list
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Execute and Return One
    ################################################
    def execute_and_return_one(self, sql, values=None):
        try:
            # select count(*) as cnt from elias where age=10;
            self.execute_only(sql, values)
            data = self.cursor.fetchone()
            return data
        except Exception as e:
            message = f'--> Exception is {e} (Line: {sys.exc_info()[-1].tb_lineno})'
            ic(message)

    ################################################
    # Disconnect
    ################################################
    def disconnect_db(self):
        if self.conn is not None:
            self.conn.close()
            self.conn = None
            self.cursor = None
        ic('DB is disconnected')

if __name__ == '__main__':
    db = Database(host='45.115.155.124', user='dbadmin', passwd='dbadmin', db='lg_autotest')
    db.connect_db()

    table_name = 'elias'

    ################################################################
    # Create Table
    ################################################################
    # sql = f"CREATE TABLE `{table_name}`(" \
    #       "id int(11) NOT NULL AUTO_INCREMENT, " \
    #       "reg_datetime datetime DEFAULT current_timestamp(), " \
    #       "name varchar(32) DEFAULT NULL, " \
    #       "age int(11) DEFAULT NULL, " \
    #       "KEY id (id) ) " \
    #       "ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;"
    # db.execute_and_commit(sql)

    ################################################################
    # Insert Data
    ################################################################
    # for i in range(10):
    #     sql = f'insert into {table_name} (name, age) values(%s, %s);'
    #     values = (f'{table_name}_{i+1}', (20 + i))
    #     # db.execute_and_commit(sql, values)
    #     db.execute_only(sql, values)
    # db.commit_only()

    # name = 'Elias Kim'
    # age = 20
    # sql = f'insert into elias (reg_datetime, name, age) values("2023-09-21", "{name}", {age});'
    # db.execute_and_commit(sql)

    # ################################################################
    # # Get data from table
    # ################################################################
    # sql = 'select * from elias;'
    # data_list = db.execute_and_return(sql)
    # for data in data_list:
    #     ic(data)

    # ################################################################
    # # Get only one data from table
    # ################################################################
    # # sql = 'select * from elias where name = "Jack" and age = 22;'
    # sql = 'select count(*) as total_count from elias;'
    # data = db.execute_and_return_one(sql)
    # ic(data)

    # ################################################################
    # # Update data
    # ################################################################
    # id =1
    # new_name = 'Hong Gildong'
    # new_age = 30
    #
    # sql = 'update elias set name = %s, age = %s, reg_datetime = current_timestamp() where id = %s;'
    # values = (new_name, new_age, id)
    # db.execute_and_commit(sql, values)

    # ################################################################
    # # Delete data
    # ################################################################
    # id = 2
    # sql = f'delete from elias where id = {id};'
    # db.execute_and_commit(sql)

    sql = 'select name, age from elias'
    data_list = db.execute_and_return(sql)

    for data in data_list:
        name = data['name']
        age = data['age']

        if 'address' in data:
            address = data['address']
        else:
            address = ''

        ic('=================')
        ic(name)
        ic(age)
        ic(address)

    people_list = [{'name':'Honey', 'age':22},
                   {'name':'Evo', 'age':20}]

    for people in people_list:
        sql = 'insert into elias (name, age) values(%s, %s);'
        values = (people['name'], people['age'])
        db.execute_only(sql, values)
    db.commit_only()

    db.disconnect_db()













