from flask import *
import os
import sqlite3 as sql

app = Flask(__name__)
app.config['SECRET_KEY'] = "CRY baby"

conn = sql.connect('todolist.db', check_same_thread =  False)
conn.cursor().execute('CREATE TABLE IF NOT EXISTS clients( username text NOT NULL PRIMARY KEY);')
conn.cursor().execute('CREATE TABLE IF NOT EXISTS todolist( id integer PRIMARY KEY, username text NOT NULL, info text, done boolean);')
cor = conn.cursor()


@app.route('/')
def x():
	return render_template('index.html')

@app.route('/user/<username>')
def home(username):
	#cor = conn.cursor()
	get_cloumn = '''SELECT todolist.info FROM todolist JOIN clients ON todolist.username = clients.username where clients.username = ? and todolist.done = ?'''
	todolist = cor.execute(get_cloumn, ( username, 0)).fetchall()
	get_cloumn = '''SELECT todolist.id FROM todolist JOIN clients ON todolist.username = clients.username where clients.username = ? and todolist.done = ?'''
	get_id = cor.execute(get_cloumn, ( username, 0)).fetchall()
	get_cloumn = '''SELECT todolist.info FROM todolist JOIN clients ON todolist.username = clients.username where clients.username = ? and todolist.done = ?'''
	get_uncomplete = cor.execute(get_cloumn, ( username, 1)).fetchall()
	return render_template('user.html', name = username, data1 = zip(todolist, get_id), data2 = get_uncomplete, )

#add new list
@app.route('/add', methods = ['POST'])
def add():
	#cor = conn.cursor()
	id = len(cor.execute('SELECT id FROM todolist').fetchall())
	todo =  '''INSERT INTO todolist values(?,?,?,?)'''
	cor.execute(todo, (id, session['login_in'],request.form['todoitem'],0))
	return redirect(url_for('home', username = session['login_in']))

@app.route('/complete/<id>')
def complete(id):
	get_cloumn = '''UPDATE todolist SET done = 1 where id = ?'''
	cor.execute(get_cloumn, (id,))
	return redirect(url_for('home', username = session['login_in']))

@app.route('/delete/<id>')
def delete(id):
	get_cloumn = '''UPDATE todolist SET username = "cry boby cry boby" where id = ?'''
	cor.execute(get_cloumn, (id,))
	return redirect(url_for('home', username = session['login_in']))

@app.route('/getupdate/<id>')
def getupdate(id):
	return render_template('update.html', id = id)

@app.route('/update/<id>', methods = ['GET','POST'])
def update(id):
	if request.method == 'POST':
		get_cloumn = '''UPDATE todolist SET info = ? where id = ?'''
		cor.execute(get_cloumn,(request.form.get('info'), id))
		return redirect(url_for('home', username = session['login_in']))
	return render_template('update.html', id = id)


@app.route('/register', methods = ['GET', 'POST'])
def register():
	reg = None
	#cor = conn.cursor()
	username = cor.execute('SELECT username from clients').fetchall()
	if request.method == 'POST':
		for index in range(len(username)):
			if request.form['regs'] == ''.join(username[index]):
				reg = "this username adrealy register"
				return render_template('register.html', reg = reg) 
	if request.form.get('regs') != None:
		cor.execute('INSERT INTO clients values(?)', (request.form.get('regs'),))
		reg = "you register"
	return render_template('register.html', reg = reg) 

#Route for handing the login page
@app.route('/login', methods = ['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
	#	cor = conn.cursor()
		username = cor.execute('SELECT username from clients').fetchall()
		for index in range(len(username)):
			if request.form['username'] == ''.join(username[index]):
				session['login_in'] = request.form['username']
				return redirect(url_for('home', username = request.form['username']))		
		error = "not corret username or password"
	return render_template('login.html', error = error) 


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

if __name__ == '__main__':	
	app.run(debug=True)