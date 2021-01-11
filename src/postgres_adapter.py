"""
This file is a generic postgres database for a scraper.
We will tweak it to our operation. 
"""
import psycopg2
import os
#################################################################
commands = (
# This is a generic table entry
"""
CREATE TABLE %s (
    id VARCHAR(255) PRIMARY KEY,
    timestamp VARCHAR(255),
    username VARCHAR(15), 
    sent_to VARCHAR(255),
    replies INTEGER,
    retweets INTEGER,
    favorites INTEGER,
    text VARCHAR(512),
    geo VARCHAR(255),
    mentions VARCHAR(255),
    hashtags VARCHAR(255),
    permalink VARCHAR(255)
);
""")
commands2 = (
"""
CREATE TABLE %s (
    id INTEGER PRIMARY KEY,
    username VARCHAR(255)
);
""")
#################################################################
class TwitterDBClient():
    HOST       = 'localhost'
    DB_NAME    = 'utilizedb'
    TABLE_NAME = 'utilize_data'
    USER       = 'utilize'
    PASSWD     = ''
    session    = None
    cursor     = None
    def init_session(self, host=HOST, db=DB_NAME,user=USER,passwd=PASSWD):
	    if host is None:
		    print("[init_session] Error: No host provided.\n")
		    return None
	    if db is None:
		    print("[init_session] Error: No database specified.\n")
		    return None
	    try:
		    if passwd is None or passwd == '':
			    self.session = psycopg2.connect(host=host, database=db, user=user)
		    else:
			    self.session = psycopg2.connect(host=host, database=db, user=user, password=passwd)
		    self.cursor = self.session.cursor()
	    except:
		    print("[init_session] Error: could not connect to host %s"%(host))
    
    def create_table(self, table_name=TABLE_NAME, preparedStmt=commands):
	    if table_name is None:
		    print("[create_table] Error: table name not specified.\n")
		    return None
	    if preparedStmt is None:
		    print("[create_table] Error: no table structure provided.\n")
		    return None
	    try:
		    self.cursor.execute(preparedStmt%(table_name))
		    self.session.commit()
		    print("[create_table] Table %s created.\n"%(table_name))
	    except:
		    print("[create_table] Error: table creation failed.\n")
		    return None
    
    def delete_table(self, table_name=None):
	    if table_name is None:
		    print("[delete_table] Error: no table name provided.\n")
		    return None
	    sql = "DROP TABLE %s"%(table_name)
	    try:
		    self.cursor.execute(sql)
		    self.session.commit()
	    except:
		    print("[delete_table] Error: could not delete table.\n")
		    self.session.commit()
		    return None
    
    def insert_row_by_id(self, table_name=TABLE_NAME, row_id=None):
	    if row_id is None:
		    print("[insert_row_by_id] Error: no row id provided.\n")
		    return None
	    sql = """INSERT INTO %s(id)"""%(table_name)
	    sql += """ VALUES(%s);"""
	    try:
		    if row_id is int:
			    row_id = str(row_id)
		    sql = sql%("'"+str(row_id)+"'")
		    self.cursor.execute(sql)
		    self.session.commit()
	    except:
		    print("[insert_row_by_id] Error: could not insert row.\n")
		    print("SQL: %s"%(sql))
		    self.session.commit()
		    return None
    
    def populate_row_data(self, table_name=TABLE_NAME, row_id=None, row_data=None):
	    if row_id is None:
		    print("[populate_row_data] Error: no row id provided.\n")
		    return None
	    if row_data is None:
		    print("[populate_row_data] Error: no row data provided.\n")
		    return None
	    try:
		    if row_id is int:
			    row_id = str(row_id)
		    sql = """UPDATE %s"""%(table_name)
		    select_clause = " WHERE id = '%s';"%(row_id)
		    key_list = [key for key in row_data.keys()]
		    for key in key_list:
			    if key == 'id':
				    #self.insert_row_by_id(table_name, row_data[key])
				    continue
			    if key == 'to':
				    row_data['sent_to'] = row_data['to']
				    key = 'sent_to'
			    if key == 'text':
				    try:
					    sql = "UPDATE %s"%(table_name)
					    sql += " SET %s = \'%s\'"%(key, str(row_data[key]))
					    sql += select_clause
					    try:
						    self.cursor.execute(sql)
						    self.session.commit()
						    continue
					    except:
						    print("Error: malformed text.")
						    print("\t%s"%(row_data[key]))
						    self.session.commit()
						    continue
				    except:
					    pass
			    sql = "UPDATE %s"%(table_name)
			    sql += " SET %s = '%s' "%(key, str(row_data[key]))
			    sql += select_clause
			    #print(sql)
			    try:
				    self.cursor.execute(sql)
				    self.session.commit()
			    except:
				    print("[populate_row_data] Error: could not execute query '%s'.\n"%(sql))
				    self.session.commit()
				    return None
	    except:
		    print("[populate_row_data] Error: could not insert row data\n")
		    return None

    def insert_row(self, table=TABLE_NAME, row_data=None):
	    if row_data is None:
		    print("[insert_row] Error: row_data is none.\n")
		    return None
	    try:
		    row_id = row_data['id']
		    self.insert_row_by_id(table, str(row_id))
		    self.populate_row_data(table, str(row_id), row_data)
	    except:
		    print("[insert_row] Error: could not insert row.\n")
		    self.session.commit()
		    return None
