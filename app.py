from flask import Flask, render_template, request, redirect, session, flash

app = Flask(__name__)
app.secret_key = 'mi_clave_secreta'  # Cambia esto en producción

@app.route('/')
def index():
    productos = session.get('productos', [])
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        id_producto = request.form['id']
        nombre = request.form['nombre']
        cantidad = int(request.form['cantidad'])
        precio = float(request.form['precio'])
        fecha_vencimiento = request.form['fecha_vencimiento']
        categoria = request.form['categoria']

        # Validar ID único
        productos = session.get('productos', [])
        if any(p['id'] == id_producto for p in productos):
            flash('El ID ya existe. Por favor, elige uno diferente.', 'error')
            return redirect('/agregar')

        nuevo_producto = {
            'id': id_producto,
            'nombre': nombre,
            'cantidad': cantidad,
            'precio': precio,
            'fecha_vencimiento': fecha_vencimiento,
            'categoria': categoria
        }

        productos.append(nuevo_producto)
        session['productos'] = productos
        flash('Producto agregado exitosamente.', 'success')
        return redirect('/')

    return render_template('agregar.html')

@app.route('/editar/<string:id_producto>', methods=['GET', 'POST'])
def editar(id_producto):
    productos = session.get('productos', [])
    producto = next((p for p in productos if p['id'] == id_producto), None)

    if request.method == 'POST':
        producto['nombre'] = request.form['nombre']
        producto['cantidad'] = int(request.form['cantidad'])
        producto['precio'] = float(request.form['precio'])
        producto['fecha_vencimiento'] = request.form['fecha_vencimiento']
        producto['categoria'] = request.form['categoria']

        session['productos'] = productos
        flash('Producto editado exitosamente.', 'success')
        return redirect('/')

    return render_template('editar.html', producto=producto)

@app.route('/eliminar/<string:id_producto>')
def eliminar(id_producto):
    productos = session.get('productos', [])
    productos = [p for p in productos if p['id'] != id_producto]
    session['productos'] = productos
    flash('Producto eliminado exitosamente.', 'success')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
