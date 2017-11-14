import MySQLdb as mdb
from bottle import FormsDict
from hashlib import md5

# connection to database project2
def connect():
    """makes a connection to MySQL database.
    @return a mysqldb connection
    """
    
    #TODO: fill out function parameters. Use the user/password combo for the user you created in 2.1.2.1
    
    return mdb.connect(host="localhost",
                       user="yschiu2",
                       passwd="2fe03986865f8acf8713d7ac5bf9cb2e1b3ed3d51699a2ecf606a6106ceae739",
                       db="project2");

def createUser(username, password):
    """ creates a row in table named user 
    @param username: username of user
    @param password: password of user
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query creates a row in table user
    m = md5()
    m.update(password)
    passwordhash = m.hexdigest()
    # qry = """INSERT INTO user (username, password, passwordhash) VALUES (%s, %s, %s)"""
    # args = (username, password, passwordhash)
    # cur.execute(qry, args)
    qry = """PREPARE stm1 FROM 'INSERT INTO user (username, password, passwordhash) VALUES (?, ?, ?)'"""
    cur.execute(qry)
    qry = """SET @a = %s"""
    args = (username, )
    cur.execute(qry, args)
    qry = """SET @b = %s"""
    args = (password, )
    cur.execute(qry, args)
    qry = """SET @c = %s"""
    args = (passwordhash, )
    cur.execute(qry, args)
    qry = """EXECUTE stm1 USING @a, @b, @c"""
    cur.execute(qry)
    db_rw.commit()

def validateUser(username, password):
    """ validates if username,password pair provided by user is correct or not
    @param username: username of user
    @param password: password of user
    @return True if validation was successful, False otherwise.
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects a row from table user
    # qry = """SELECT * FROM user WHERE user.username = %s and user.password = %s"""
    # args = (username, password)
    # cur.execute(qry, args)
    qry = """PREPARE stm1 FROM 'SELECT * FROM user WHERE user.username = ? and user.password = ?'"""
    cur.execute(qry)
    qry = """SET @a = %s"""
    args = (username, )
    cur.execute(qry, args)
    qry = """SET @b = %s"""
    args = (password, )
    cur.execute(qry, args)
    qry = """EXECUTE stm1 USING @a, @b"""
    cur.execute(qry)
    if cur.rowcount < 1:
        return False
    return True

def fetchUser(username):
    """ checks if there exists given username in table users or not
    if user exists return (id, username) pair
    if user does not exist return None
    @param username: the username of a user
    @return The row which has username is equal to provided input
    """

    db_rw = connect()
    cur = db_rw.cursor(mdb.cursors.DictCursor)
    print username
    #TODO: Implement a prepared statement so that this query selects a id and username of the row which has column username = username
    # qry = """SELECT id, username FROM user WHERE user.username = %s"""
    # args = (username, )
    # cur.execute(qry, args)
    qry = """PREPARE stm1 FROM 'SELECT id, username FROM user WHERE user.username = ?'"""
    cur.execute(qry)
    qry = """SET @a = %s"""
    args = (username, )
    cur.execute(qry, args)
    qry = """EXECUTE stm1 USING @a"""
    cur.execute(qry)
    if cur.rowcount < 1:
        return None
    return FormsDict(cur.fetchone())

def addHistory(user_id, query):
    """ adds a query from user with id=user_id into table named history
    @param user_id: integer id of user
    @param query: the query user has given as input
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statment using cur.execute() so that this query inserts a row in table history
    # qry = """INSERT INTO history (user_id, query) VALUES (%s, %s)"""
    # args = (user_id, query)
    # cur.execute(qry, args)
    qry = """PREPARE stm1 FROM 'INSERT INTO history (user_id, query) VALUES (?, ?)'"""
    cur.execute(qry)
    qry = """SET @a = %s"""
    args = (user_id, )
    cur.execute(qry, args)
    qry = """SET @b = %s"""
    args = (query, )
    cur.execute(qry, args)
    qry = """EXECUTE stm1 USING @a, @b"""
    cur.execute(qry)
    db_rw.commit()

#grabs last 15 queries made by user with id=user_id from table named history
def getHistory(user_id):
    """ grabs last 15 distinct queries made by user with id=user_id from 
    table named history
    @param user_id: integer id of user
    @return a first column of a row which MUST be query
    """

    db_rw = connect()
    cur = db_rw.cursor()
    #TODO: Implement a prepared statement using cur.execute() so that this query selects 15 distinct queries from table history
    # qry = """SELECT DISTINCT query FROM history WHERE user_id = 1 GROUP BY query ORDER BY max(id) DESC LIMIT 15"""
    # args = (user_id, )
    # cur.execute(qry, args)
    qry = """PREPARE stm1 FROM 'SELECT DISTINCT query FROM history WHERE user_id = ? GROUP BY query ORDER BY max(id) DESC LIMIT 15'"""
    cur.execute(qry)
    qry = """SET @a = %s"""
    args = (user_id, )
    cur.execute(qry, args)
    qry = """EXECUTE stm1 USING @a"""
    cur.execute(qry)
    rows = cur.fetchall();
    return [row[0] for row in rows]
