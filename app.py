from flask import Flask, session, render_template, request, redirect, url_for
import uuid  # Para generar IDs únicos

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar sesiones

# Inicializa la sesión si no tiene productos
@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

# Ruta principal que muestra todos los productos
@app.route('/')
def index():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

# Ruta para agregar un producto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': str(uuid.uuid4()),  # Genera un ID único
            'nombre': request.form['nombre'],
            'cantidad': int(request.form['cantidad']),
            'precio': float(request.form['precio']),
            'fecha_vencimiento': request.form['fecha_vencimiento'],
            'categoria': request.form['categoria']
        }
        # Agregar el producto a la sesión
        productos = session['productos']
        productos.append(nuevo_producto)
        session['productos'] = productos
        return redirect(url_for('index'))

    return render_template('agregar.html')

# Ruta para editar un producto existente
@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_producto(id):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id), None)

    if not producto:
        return redirect(url_for('index'))

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']
        session['productos'] = productos
        return redirect(url_for('index'))

    return render_template('editar.html', producto=producto)

# Ruta para eliminar un producto
@app.route('/eliminar/<string:id>')
def eliminar_producto(id):
    productos = session.get('productos', [])
    session['productos'] = [p for p in productos if p['id'] != id]
    return redirect(url_for('index'))

# Ejecuta la aplicación en modo depuración
if __name__ == '__main__':
    app.run(debug=True)
