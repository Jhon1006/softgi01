from flask import Flask, render_template, request, redirect, url_for, flash, g,session
from flaskext.mysql import MySQL
from flask_mail import Mail, Message
from email.mime.text import MIMEText
import hashlib, smtplib, random, string, re, datetime, secrets
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature,BadSignature
from email.message import EmailMessage

from crearProveedore import creaProveedores

from clientes import Clientes

 

 
# Crear una instancia de la aplicación Flask
app = Flask(__name__)
mysql = MySQL()
# Configura una clave secreta para la aplicación
app.secret_key = 'tu_clave_secreta_aqui'  # Clave secreta recordar cambiarla

# Configuración de la base de datos MySQL
app.config['MYSQL_DATABASE_SECRET_KEY'] = 'tu_clave_secreta_aqui'
app.config['MYSQL_DATABASE_USER'] = 'cristobulo_12345'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234Jena+'
app.config['MYSQL_DATABASE_DB'] = 'sofgi_01'
app.config['MYSQL_DATABASE_HOST'] = 'db4free.net'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_CHARSET'] = 'utf8mb4'

# Configuracion de servidor de envio de email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # el servidor SMTP de tu proveedor de correo
app.config['MAIL_PORT'] = 587  # Puerto SMTP recordar los puertos que se utilizan generalmente ( 587 o 465)
app.config['MAIL_USE_TLS'] = True  # Usar TLS (True o False según la configuración del servidor)
app.config['MAIL_USERNAME'] = 'jenasoft05@gmail.com'  # dirección de correo electrónico
app.config['MAIL_PASSWORD'] = 'laobfjwveaolryrt'  # contraseña de correo electrónico

# Crear una instacia de la fincion de email de flask
mail = Mail(app)

# Inicializar la extensión MySQL
mysql.init_app(app)


proveedores = creaProveedores(mysql, app)
losClientes = Clientes(mysql,app)#clientes = Clientes()# Crear una instancia de la clase Cliente

'''losClientes = Clientes(mysql, app)'''