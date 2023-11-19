from flask import render_template, redirect, session, request, flash
from flask_bcrypt import Bcrypt
from app_py import app
from app_py.models.usuarios import Usuario
from app_py.models.quotes import Quote

bcrypt = Bcrypt(app)

@app.route('/')
def main():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        data = {
            'id_usuario': session['user_id']
        }
        return render_template('dashboard.html', usuario=Usuario.get_one(data), quotes=Quote.get_all())
    else:
        return redirect('/')

@app.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    if not Usuario.validar_usuario(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['pasword'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'pasword': pw_hash
    }
    user_id = Usuario.crear_usuario(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/iniciar_sesion', methods = ['POST'])
def iniciar_sesion():
    data = {
        'email': request.form['email']
    }
    usuario = Usuario.get_by_email(data)
    if not usuario:
        flash("Email/Contraseña Inválidos", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(usuario.pasword, request.form['pasword']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['user_id'] = usuario.id_usuario

    return redirect('/dashboard')

@app.route('/delete_session')
def eliminar_sesion():
    if 'email' in session:
        session.pop('email', None)
    return redirect("/")

@app.route('/edit_acc/<int:id_usuario>', methods=['POST'])
def edit_account(id_usuario):
    id_usuario = session['user_id']
    if 'user_id' in session:
        data = {
            'id_usuario': id_usuario,
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
        }
        Usuario.edit_user(data)
        return redirect('/edit_user')

@app.route('/back_page')
def back_page():
    return redirect('/dashboard')

@app.route('/edit_user')
def edit_user():
    if 'user_id' in session:
        data = {
            'id_usuario': session['user_id']
        }
        return render_template('edit_account.html', usuario=Usuario.get_one(data))
    

@app.route('/create_quote', methods=['POST'])
def create_quote():
    data = {
        'id_usuario': session['user_id'],
        'quote': request.form['quote'],
        'autor': request.form['autor']
    }
    Quote.create_quote(data)
    print(data)
    return redirect('/dashboard')

@app.route('/userquotes')
def userquotes():
    return render_template('userquotes.html', quote=Quote.get_all())