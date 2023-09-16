
from conexion import * # Importa solo lo que necesitas de Flask

class Clientes:
    def __init__(self, mysql, app):  # Recibe mysql y app como parámetros
        self.mysql = mysql
        self.app = app
        self.conexion = self.mysql.connect()  # Usa el método connect() para crear la conexión
        self.cursor = self.conexion.cursor()

    def crear_cliente(self, cliente):
    
                now = datetime.now()
                tiempo = now.strftime("%Y%m%d%H%M%S")
                
                sql = f"INSERT INTO clientes(docclie, nomclie, apeclie, contclie, emaclie, direclie, tipopersona) VALUES ('{cliente[0]}','{cliente[1]}','{cliente[2]}','{cliente[3]}','{cliente[4]}','{cliente[5]}','{cliente[6]}')"
                self.cursor.execute(sql)
                self.conexion.commit()
    

    def cliente_existe_en_db(self, cliente):
        sql = f"SELECT COUNT(*) FROM clientes WHERE doc_cliente = '{cliente}'"

        self.cursor.execute(sql)
        resultado = self.cursor.fetchone()

        if resultado[0] > 0:
            return True
        else:
            return False
