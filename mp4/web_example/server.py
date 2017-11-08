import sqlite3
from bottle import route, run, template, get, post, request


@route('/')
def index():
	return template('index')

@route('/fulliframe')
def fulliframe():
	return template('fulliframe')

@get('/ssn')
def ssn():
	name = request.query['name']
	COB = request.query['cob']
	ssn = run_query(name, COB)
	return template('info', type="GET", name=name, cob=COB, ssn = ssn if ssn == None else ssn[0])

@post('/ssn')
def ssn():
	name = request.forms.get('name')
	COB = request.forms.get('cob')
	ssn = run_query(name, COB)
	return template('info', type="POST", name=name, cob=COB, ssn = ssn if ssn == None else ssn[0])

def run_query(name, COB):
	"""
	This function takes a name and COB, and then looks in the database to see if there is a User
	with the specified credentials. If there is, this returns the first one.
	"""
	print(name)
	print(COB)
	conn = sqlite3.connect("test2.db")
	c = conn.cursor()
	c.execute("SELECT SSN FROM Users WHERE Name = ? AND COB = ?", (name, COB))  # This is a prepared statement. This allows you to paste in variables to a SQL statment, and then execute it
	result = c.fetchone()
	c.close()
	print(result)
	return result
	
run(host='localhost', port=8080)