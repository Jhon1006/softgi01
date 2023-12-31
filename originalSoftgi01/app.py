from conexion import * #Importo la conexion de la base de datos y las funciones de flask, que en este caso se encuentra en el archivo conexion.py 
from clientes import Clientes  # Importa la clase Clientes desde clientes.py





@app.route('/') # Inicio la ruta princimpla del programa en este caso home que me muestra como pagina principal un login
def registro(): # Defino la funcion de la ruta principal en este caso la funcion se llama registro
    return redirect('/home') # Retorno o lo devuelvo la ruta home para que me muestre la pagina segun la definicion

def generate_token(length=32): # Esta funcion genera un token de 32 caracteres el token generado se utiliza para enviar un token unico a cada usuario registrado 
    characters = string.ascii_letters + string.digits  # defino esta variable con pertenecias de caracteres especiales permitiendo letras ascii en mayusculas y minusculas y numeros haciendo que cada token sea generado de manera impredecible 
    token01 = ''.join(secrets.choice(characters) for _ in range(length)) # Genero la cadena o el token aleatorio y lo guardo en la variable token01
    return token01 # Retorno o lo devuelvo la variable token01 para ver su resultado en este caso esta comentado por que nomas era una prueba


@app.route('/registroF') # defino la ruta de registro
def registroF(): # defino la funcion de la ruta de registro llamada registroF
    return render_template('/registro_usuario.html') # lo retorno o lo devuelvo a el html de registro de usuario en este caso el archivo registro_usuario.html y para eso se untiliza render_template


# Ruta de registro de usuario
@app.route('/registro', methods=['POST']) # defino la ruta que me envia los datos ingresado en el formulario a la base de datos con el metodo post que se utiliza para envio de datos 
def registro_usuario(): #defino la funcion de la ruta 
    
    conn = mysql.connect() # Uso mysql.connect para conectar o hacer la conexion con la base de datos, mysql.connect es una de las funciones que utliza flask para conectarse a una base de dato
    cursor = conn.cursor() # Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    docempl = request.form['documento'] # Utilizo request.form Para trear los datos dijitados en el formulario y la variable docempl la almacena
    nomempl = request.form['nombre']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable nomempl la almacena
    apeempl = request.form['apellido']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable apempl la almacena
    emaempl = request.form['correo']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable emaempl la almacena
    rol = request.form['rol']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable rol la almacena
    
    # Validación del correo electrónico
    if not re.match(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", emaempl):# Hago una toma de desicion donde el correo no tenga los carateres suficiente q se les requieren muestre un mensaje de error 
        return render_template('/registro_usuario.html', flash="Correo electrónico inválido. Intente nuevamente.") # muestra el mesaje de la toma de desiciones anterior
    
    clave1 = request.form['contrasena'] # Utilizo request.form Para trear los datos dijitados en el formulario y la variable clave1 la almacena
    clave2 = request.form['confirmada']# Utilizo request.form Para trear los datos dijitados en el formulario y la variable clave2 la almacena
    if clave1 == clave2: # Comparo las contraseñas digitadas para confirmar si conciden 
        cifrada = hashlib.sha512(clave1.encode("utf-8")).hexdigest() # Cifro la contraseña con el metodo hashlib 
        consul = f"SELECT * FROM empleados WHERE docempl='{docempl}' OR emaempl='{emaempl}'"# Consulto en la base de dato que el usuario digitado no  exista ni su correo ni su numero de documento
        cursor.execute(consul)# Ejecuto la consulta de la base de dato
        resultado_1 = cursor.fetchone() # guardo los datos de la consulta que se hizo 
        if resultado_1 is not None: # hago una toma de desicion que donde la consulta resultado tiene dato o no esta vacia me haga el siguiente metodo
            flash('Este usuario ya ha sido registrado') # que envie este mensaje para que el usuario lo vea 
            return redirect(url_for('home'))# me retorne o me devuelva a la pagina home en este caso untilizo redirect(url_for('home')) para que me redirija desde python a esa funcion llamada home
        else: # en caso de que la consulta hecha no exista en la base de datos que me tome la siguiente desicion
            mi_token2 = generate_token()  # agrego a la variable mi_token2 la funcion generar token, cada vez que se quiera resgistrar un suario nuevo se genera un token nuevo ya q se ejecuta la funcion generate_token()

            # Envía el correo de confirmación
            enviar_correo_confirmacion(nomempl, emaempl, mi_token2)# ejecuto la funcion de enviar_correo_confirmacion(nomempl, emaempl, mi_token2) enviado 3 variables que son nomempl, emaempl, mi_token2 para enviar como imformacion al correo segun definido en la variable emaempl con un on token unico y el nombre de la persona q se le envia el correo
            
            
            sql = "INSERT INTO empleados (docempl, nomempl, apeempl, emaempl, contrasena, rol ) VALUES ( %s, %s, %s, %s, %s, %s)"# Inserto o registro los datos en la base de datos en la tabla empleado 
            cursor.execute(sql, (docempl, nomempl, apeempl, emaempl, cifrada, rol)) # ejecuto el registro hecho 
            conn.commit()#hago un conn.commit confirmando la transacción actual
            
            fecha_registro = datetime.datetime.now()#la variable fecha _registro optiene el tiempo hora fecha año y segundo que estas actual
            tok = f"INSERT INTO tokens (doc_empleado, nom_empleado, email_empleado, token, confir_user, tiemp_registro) VALUES ('{docempl}', '{nomempl}', '{emaempl}','{mi_token2}', 'no confirmado', '{fecha_registro}' )" # Inserto o registro los datos en la base de datos en la tabla tokens
            cursor.execute(tok)# ejecuto el registro hecho
            conn.commit()#hago un conn.commit confirmando la transacción actual
            conn.close()# Utilizamos esta funcion para cerrar la conexion aunque la conexion se ciera sola cuando sale de alcance
            flash('Tu usuario ha sido registrado exitosamente') # mostramos este mensaje donde el registro sea exitoso
            flash("Se envio un correo para confirmar tu registro, revisa la bandeja de entrada o spam")# mostramos un mensaje donde el registro sea exitoso y le idicamos que se envio un correo
            return render_template('login.html')# se envia a login.html ya cumplido todo
            

            """ # Insertar los datos del usuario en la base de datos 
            sql = "INSERT INTO empleados (docempl, nomempl, apeempl, emaempl, contrasena, rol, conemail,  token) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (docempl, nomempl, apeempl, emaempl, cifrada, rol, 'sin_confirmar', mi_token2))
            conn.commit()
            conn.close()
            flash('Tu usuario ha sido registrado exitosamente')
            return render_template('login.html') """
            
    else:# en el caso de que las contraseña no considan se aplicara esta desicion
        flash('la contraseña no coincide')# muestra un mensaje indicando lo sucedido
        return redirect(url_for('/registro_usuario'))# redirige  a la la funcion de registro_usuario


# Función para enviar el correo de confirmación
def enviar_correo_confirmacion(nombre, email, token):#Esta funcion recibe lo enviando en las variable nomempl, emaempl, mi_token2 para enviar como imformacion al correo 
    confirm_url = url_for('confirmar_correo', token=token, email=email, _external=True)# genero el link agregandole el token unico y el email digitado 
    render_html = render_template('correoMsj.html', nombre=nombre, correo_url=confirm_url)# Creo una variable que me trae el mesaje de un html en este caso correoMsj.html que va hacer el envio que se va hacer al correo
    msg = Message('Confirmación de correo electrónico', sender='jenasoft05@gmail.com', recipients=[email])#defino el titulo el correo que envia y al correo q va ser enviado el mesaje 
    msg.html =  render_html # agrego el mensaje que va a llegar al correo y su informacion segun dada
    mail.send(msg)# envio el mensaje al correo 
        
        

# Ruta de confirmación de correo electrónico    
@app.route('/confirmar_correo/<token>', methods=['GET', 'POST'])# ruta de confirmacion  de correo recibe el token segun el correo y pongo el metdo recibir y enviar GET y POST
def confirmar_correo(token): #dlaclaro la funcion con el nombre confirma_correo
    cursor = mysql.get_db().cursor()
    # Consulto el usuario que tiene tiene el token que se envio segun el correo 
    cursor.execute("SELECT doc_empleado, nom_empleado, email_empleado, confir_user FROM tokens WHERE token = %s", (token,)) #ejecuto la consulta 
    usuario_data = cursor.fetchone() # agrego el resultado de la consulta a la variable usuario_data
    if not usuario_data: # # esta toma de desicion se aplica si el usuario no tiene token 
            flash('El token de confirmación no es válido.', 'danger') # le indico el mensaje al usuario
            return redirect(url_for('home')) # redirijo a la pagina home

    email = usuario_data[2] # Almaceno  el campo email_empleado de la base de dato a la variable email
    correo_confirmado = usuario_data[3] # Almaceno el campo confir_user de la base de dato a la variable correo_confirmado

    if correo_confirmado == 'confirmado':# toma de desicion que se aplica en el caso de que el correo este confirmado
        flash('El correo ya ha sido validado.', 'danger')# le indico el mensaje
        return redirect(url_for('home'))# redirijo a la pagina home
    
    #en caso tal de que no se apliquen los metodos anteriores 
    if request.method == 'POST': # Verifico si la solicitud HTTP es un método POST
        confi= request.form['confir'] # Utilizo request.form Para trear los datos dijitados en el formulario
        # Actualizar el estado de correo a "confirmado"
        cursor.execute(f"UPDATE tokens SET confir_user = '{confi}' WHERE email_empleado = '{email}'") # ejecuto la atualizacion a la base de datos
        mysql.get_db().commit()# obtengo la conexion a la base de dato y confirmo los cambio
        flash('Tu correo ha sido confirmado correctamente.', 'success')# le indico un mensaje
        return redirect(url_for('home'))# redirijo a la pagina home
    
    return render_template('confirmar.html')# renderizo a la pagina confirmar.html



#--------------------------------------------------Inicio de sesion------------------------------------------------------------------------------------------------

@app.route('/inicio')# Ruta de inicio
def inicio(): # hago la funcion de la ruta en este caso su nombre es inicio
    if "emaempl" in session:# verifico que se alla iniciado sesion
        return render_template('index.html') # renderizo a la pagina inicioexitoso.html
    else: # de lo contrario que no alla inicado sesion
        flash('Algo esta mal en sus datos digitados') # indico un mensaje 
        return redirect(url_for('home')) # redirijo a la pagina home


@app.route('/home')# Ruta de home
def home():# hago la funcion de la ruta en este caso su nombre es home
    return render_template('login.html')# rederizo a la pagina login.html

@app.route('/login', methods=["POST"])# Ruta de login
def login():# hago la funcion de la ruta en este caso su nombre es login
    email = request.form['correo'] # Utilizo request.form Para trear los datos dijitados en el formulario
    password = request.form['contrasena'] # Utilizo request.form Para trear los datos dijitados en el formulario
    connt = mysql.connect()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cursor = connt.cursor()# Utilizo el con.cursor para ejecutar declaraciones  para comunicarse con la base de dato
    cifrado = hashlib.sha512(password.encode('utf-8')).hexdigest()# Cifro la contraseña con el metodo hashlib 
    """  bsql_emp = f"SELECT emaempl='{email}', contrasena='{cifrado}' FROM empleados WHERE conemail='confirmado'" """
    bsql_emp = f"SELECT empleados.emaempl, empleados.contrasena='{cifrado}', tokens. confir_user  FROM empleados INNER JOIN tokens ON empleados.docempl = tokens.doc_empleado WHERE empleados.emaempl = '{email}'"
    cursor.execute(bsql_emp)# ejecuto la consulta 
    resultado = cursor.fetchone()# agrego el resultado de la consulta a la variable resultado
    if resultado is not None:# hago una toma de desicion que donde la consulta resultado tega dato o no esta vacia me haga el siguiente metodo
        if resultado[2] == 'confirmado':# toma de desicion que se aplica en el caso de que el correo este confirmado 
            session["emaempl"] = resultado[0]# Utilizo session para guardar la informacion de la persona ingresada
            return redirect(url_for('inicio'))#redirijo 
        else:
            flash("No has confirmado tu cuenta, por favor revisa la bandeja de entrada o spam", category="danger")
            return redirect(url_for('home'))
    else:
        flash('ALgo esta mal en tus credenciales o tu correo no ha sido confirmado.', 'success')
        return redirect(url_for('home'))
    
    
    
#--------------------------------------------------recuperacion de contraseña------------------------------------------------------------------------------------------------

# Clase User definida previamente
class User:# creo una clase User que la utlizare para crear objetos en este caso User se esta utilizado como plantilla
    def __init__(self, id, email, nombre):# defino el metodo, con sus parametro y los argumentos 
        self.id = id # hago una copia propia de la variable id
        self.email = email  # hago una copia propia de la variable email
        self.nombre = nombre  # hago una copia propia de la variable nombre
        
class PasswordResetToken:# creo una clase User que la utlizare para crear objetos en este caso PasswordResetToken se esta utilizado como plantilla
    def __init__(self, userio_id):# defino el metodo, con sus parametro y los argumentos 
        self.userio_id = userio_id # hago una copia propia de la variable usuario_id
        
        
        
# Función para enviar correos electrónicos de restablecimiento de contraseña
def envio_correo(user, token_rctsn):
    token_url = url_for('recuperar_contraseña', token_rctsn=token_rctsn, user=user, _external=True)
    print(token_url)
    rendered_html = render_template('correoEnv.html', user=user, token_url=token_url)
    msg = Message('Recuperación de contraseña', sender='jenasoft05@gmail.com', recipients=[user.email])
    msg.html = rendered_html
    mail.send(msg)



# Ruta para solicitar el restablecimiento de contraseña
@app.route('/solicitarCambio_contraseña', methods=['GET', 'POST'])
def solicitarCambio_contraseña():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = mysql.get_db().cursor()
        msql = f"SELECT * FROM empleados  WHERE emaempl  = '{email}'"
        cursor.execute(msql)
        userio_data = cursor.fetchone()

        if userio_data:
            userio = User(id=userio_data[0], email=userio_data[3], nombre=userio_data[1])
            

            cursor = mysql.get_db().cursor()

            # Verificar si hay registros en la tabla recuperarcontrasena para ese correo electrónico
            cursor.execute("SELECT * FROM recuperarcontrasena WHERE email = %s", (userio.email,))
            existing_token = cursor.fetchone()
            token_recuperar = token_recuperar_contrasena()  #Token que se genera para cambio de contraseña
            """ if existing_token:
                # Si ya existe un token para ese correo, actualiza su fecha de vencimiento
                expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
                cursor.execute("UPDATE recuperarcontrasena SET fhsoli= %s, fhexp = %s, codigo = %s WHERE email = %s", (datetime.datetime.now(),expiration_time, token_recuperar, userio.email))
            else:
                # Si no existe un token para ese correo, crea uno nuevo
                expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
                cursor.execute("INSERT INTO recuperarcontrasena (idsoli, email, fhsoli, fhexp, codigo, usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                                (userio.nombre, userio.email, datetime.datetime.now(), expiration_time, token_recuperar, userio.id)) """
            # Si no existe un token para ese correo, crea uno nuevo
            expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=3)
            cursor.execute("INSERT INTO recuperarcontrasena (idsoli, email, fhsoli, fhexp, codigo, usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                            (userio.nombre, userio.email, datetime.datetime.now(), expiration_time, token_recuperar, userio.id)) 
            mysql.get_db().commit()
            
            
            envio_correo(userio, token_recuperar)
            print(userio, token_recuperar)
            flash('Se ha enviado un correo electrónico con instrucciones para restablecer la contraseña.', 'success')
            return redirect(url_for('home'))
        else:
            flash('No se encontró ninguna cuenta con ese correo electrónico.', 'danger')

    return render_template('recuperar_contrasena.html')


# Función para generar un token aleatorio
def token_recuperar_contrasena(length=32):
    characters = string.ascii_letters + string.digits  # Caracteres permitidos en el token
    token02 = ''.join(secrets.choice(characters) for _ in range(length))
    return token02






# Ruta para restablecer la contraseña
@app.route('/recuperar_contraseña/<token_rctsn>', methods=['GET', 'POST'])
def recuperar_contraseña(token_rctsn):
    print(f"Token recibido: {token_rctsn}")
    cursor = mysql.get_db().cursor()
    cursor.execute("SELECT  fhexp, codigo, usuario FROM recuperarcontrasena WHERE codigo  = %s", (token_rctsn,))
    datos_db = cursor.fetchone()

    if not datos_db:
        flash('El token de confirmación no es válido.', 'danger')
        return redirect(url_for('solicitarCambio_contraseña'))
    
    usuario = datos_db[2]
    codigo = datos_db[1]

    expiration_time = datos_db[0]  # Obtener la fecha de vencimiento del token desde la base de datos
    current_time = datetime.datetime.now()
    if current_time > expiration_time:
        # El token ha caducado, mostrar un mensaje de error
        flash('El enlace de restablecimiento de contraseña ha caducado.', 'danger')
        return redirect(url_for('solicitarCambio_contraseña'))

    if request.method == 'POST':
        password = request.form.get('password')
        cifrado = hashlib.sha512(password.encode('utf-8')).hexdigest()

        cursor.execute("UPDATE empleados SET contrasena  = %s WHERE docempl = %s", (cifrado, usuario))
        cursor.execute("UPDATE recuperarcontrasena SET usado ='si' WHERE codigo = %s", (codigo))
        mysql.get_db().commit()

        flash('Tu contraseña ha sido restablecida.', 'success')
        return redirect(url_for('home'))

    return render_template('reset_password.html')

#-----------------conexión de la clase cliente------------------

""" @app.route("/clientes")
def clientes():
    if session.get("logueado"):
        resultado = losClientes.consultar()
        return render_template('/clientes.html', clien=resultado, nom=session.get("nom_cliente"))
    else:
        return render_template('/index.html') """

""" @app.route("/clientes/crear", methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        
        docclie = request.form['docclie']
        nomclie = request.form['nomclie']
        apeclie = request.form['ape_cliente']
        contclie = request.form['contclie']
        emaclie = request.form['emaclie']
        direclie = request.files['direclie']
        tipopersona = request.form['tipopersona']
        
        if not losClientes.buscar(docclie):
            losClientes.agregar([docclie, nomclie, apeclie, contclie, emaclie, direclie, tipopersona])
            return redirect('/clientes')
        else:
            mensaje="Cliente ya existe"
            cliente =["",nomclie, apeclie, contclie, emaclie, direclie,tipopersona]
            return render_template('registrocliente.html', mensaje=mensaje, cliente=cliente)
    else
        return render_template('/index.html') """


    
@app.route('/buscar_cliente', methods=['POST'])
def buscar_cliente():
    if request.method == 'POST':
        busqueda = request.form['busqueda']
        # Realiza la consulta en la base de datos utilizando MySQL y Flask-MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM clientes WHERE nombre LIKE %s", (f"%{busqueda}%",))
        resultados = cursor.fetchall()
        conn.close()
        return render_template('registroclientes.html', resultados=resultados) # Envía los resultados al mismo formulario de registroclientes.html
    

    #------------DELETE PROVEEDORES-----------------   
#----------------------------------------------Modificar Provedores ------------------------------------------------       
@app.route("/modificarprovee", methods=['POST', 'GET'])
def modificarprovee():
    documento = request.form['documentoProveedor']
    nombre = request.form['nombreProveedor']
    numero = request.form['numeroProveedores']
    correo = request.form['correoProveedores']
    direcion = request.form['direccionProveedores']
    proveedores.modificar([documento,nombre,numero,correo,direcion])
    return redirect('/proveedores')


@app.route('/borraprovee/<docprov>')
def borraprovee(docprov):
    proveedores.borrar(docprov)
    return redirect('/muestra_Proveedores')




#-----------------------------------------------------------Crear proveedores---------------------------------------
@app.route('/proveedores')
def proveedoress():
    return render_template('/provedor/proveedore.html')

@app.route('/crearProveedores', methods=['POST'])
def crearProveedores():
    documento = request.form['documentoProveedor']
    nombre = request.form['nombreProveedor']
    numero = request.form['numeroProveedores']
    correo = request.form['correoProveedores']
    direcion = request.form['direccionProveedores']
    proveedores.crear([documento,nombre,numero,correo,direcion])
    return render_template('/htmldeprueba/registradoX.html')
    
    
#-----------------------------------------------------------mostrar proveedores---------------------------------------

@app.route('/muestra_Proveedores')
def muestra_Proveedores():
    sql = "SELECT * FROM `proveedores` WHERE estado='ACTIVO'"           # consulta toda la info de proveedores.
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    conn.commit()
    if (len(resultado) >= 1):
        return render_template("/provedor/muestra_proveedores.html", resul=resultado)   # si hay resultados se muestran.
    else:
        resultado2 = "No hay proveedores registrados"
        return render_template("/provedor/muestra_proveedores.html", resul2=resultado2)   # sino se muestra el mensaje de resultado2.

                                        




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port="5085")