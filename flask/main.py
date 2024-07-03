from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

try:
    conn = mysql.connector.connect(
        host="Tunombre.mysql.pythonanywhere-services.com",
        user="Tunombre",
        password="Tupassword",
        db="Tunombre$basedatos"
    )
    message = "¡Estás conectado!"
    mycursor = conn.cursor()
except mysql.connector.Error as e:
    results = ["#"]
    message = f"NO ESTÁS CONECTADO: {e}"

def add_item(nombre, precio):
    query = "INSERT INTO articulos (nombre, precio) VALUES (%s, %s);"
    values = (nombre, precio)
    mycursor.execute(query, values)
    conn.commit()

def update_item(id, nombre, precio):
    query = "UPDATE articulos SET nombre = %s, precio = %s WHERE id = %s;"
    values = (nombre, precio, id)
    mycursor.execute(query, values)
    conn.commit()

def delete_item(id):
    query = "DELETE FROM articulos WHERE id = %s;"
    values = (id,)
    mycursor.execute(query, values)
    conn.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        add_item(nombre, precio)
        return redirect(url_for('index'))

    mycursor.execute("SELECT * FROM articulos")
    results = mycursor.fetchall()
    return render_template('index.html', message=message, results=results)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        update_item(id, nombre, precio)
        return redirect(url_for('index'))

    mycursor.execute("SELECT * FROM articulos WHERE id = %s", (id,))
    item = mycursor.fetchone()
    return render_template('update.html', item=item)

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    delete_item(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) # Cambié el puerto adrede.
