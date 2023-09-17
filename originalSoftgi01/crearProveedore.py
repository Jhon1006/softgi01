
class creaProveedores:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    def crear(self, agregar):
        bsdsql = F" INSERT INTO `proveedores`(`docprov`, `nomprov`, `contprov`, `emaprov`, `direprov`) VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}')"
        self.cursor.execute(bsdsql)
        self.conexion.commit()