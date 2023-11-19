from app_py.config.mysqlconnections import connectToMySQL
from flask import flash,request
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class Usuario():
    def __init__(self,data):
        self.id_usuario = data['id_usuario']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pasword = data['pasword']

    @classmethod
    def crear_usuario(cls,data):
        query = ('INSERT INTO usuario (first_name, last_name, email, pasword) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pasword)s)')
        return connectToMySQL('exam2_python').query_db(query,data)

    @classmethod
    def get_one(cls,data):
        query = ('SELECT * FROM usuario WHERE usuario.id_usuario = %(id_usuario)s')
        resultados = connectToMySQL('exam2_python').query_db(query,data)
        if (len(resultados) > 0):
            print(resultados)
            return cls(resultados[0])
        else:
            return None
        
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM usuario WHERE usuario.email = %(email)s;"
        result = connectToMySQL("exam2_python").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
        
    @staticmethod
    def validar_usuario(usuario):
        is_valid = True
        if usuario:
            if len(usuario['first_name']) < 2:
                flash("El nombre debe tener almenos 2 caracteres.", 'registro')
                is_valid = False
            if len(usuario['last_name']) < 2:
                flash("El apellido debe tener alemenos 2 caracteres.", 'registro')
                is_valid = False
            if not EMAIL_REGEX.match(usuario['email']):
                flash("Correo electrónico inválido.", 'registro')
                is_valid = False
            if len(usuario['pasword']) < 8:
                flash("La contraseña debe tener almnenos 8 caracteres.", 'registro')
                is_valid = False
            if not re.search(r'\d', usuario['pasword']):
                flash("La contraseña debe contener al menos un número.", 'registro')
                is_valid = False
            if not re.search(r'[A-Z]', usuario['pasword']):
                flash("La contraseña debe contener al menos una letra mayúscula.", 'registro')
                is_valid = False
            if usuario['pasword'] != usuario['c_password']:
                flash("Las contraseñas no coinciden.", 'registro')
                is_valid = False
        return is_valid
    
    @classmethod
    def edit_user(cls,data):
        query = ('UPDATE usuario SET first_name = %(first_name)s , last_name = %(last_name)s, email = %(email)s WHERE usuario.id_usuario = %(id_usuario)s')
        return connectToMySQL('exam2_python').query_db(query,data)
    
    
