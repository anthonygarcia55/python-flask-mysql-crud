from flask import Flask, render_template, request, redirect, url_for,flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql Connection
app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'dbcontactos'
mysql = MySQL(app)

app.secret_key = "mysecretkey"

@app.route('/')
def Index ():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactox')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contact = data)

@app.route('/agregar_contacto', methods=['POST'])
def agregar_contacto():
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contactox')
        date = cur.fetchall()
        for dato in date:
            if dato[2] == email:
                cur.close()
                flash('EL Correo ya Existe')
                return redirect(url_for('Index'))
                            
        cur.execute("INSERT INTO contactox (fullname, email) VALUES (%s,%s)", (fullname, email))
        mysql.connection.commit()
        return redirect(url_for('Index'))
    
@app.route('/editar/<id>', methods = ['POST','GET'])
def editar_contacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contactox WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close
    return render_template('edit_contact.html', contact = data[0])

@app.route('/actualizar/<id>', methods = ['POST'])
def update_co(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE contactox 
            SET fullname = %s,
                email = %s
            WHERE id = %s
        """, (fullname,email, id))
        mysql.connection.commit()
        return redirect(url_for('Index'))    

@app.route('/eliminar/<string:id>', methods = ['POST','GET'])
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contactox WHERE id = {0}'.format(id))
    mysql.connection.commit()
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port =3000, debug =True)
