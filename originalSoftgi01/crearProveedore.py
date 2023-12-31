
class creaProveedores:
    def __init__(self, DB, app):
        self.mysql = DB
        self.app = app
        self.conexion = self.mysql.connect()
        self.cursor = self.conexion.cursor()
        
    #Crear provedores
    def crear(self, agregar):
        bsdsql = F" INSERT INTO `proveedores`(`docprov`, `nomprov`, `contprov`, `emaprov`, `direprov`, `estado`) VALUES ('{agregar[0]}','{agregar[1]}','{agregar[2]}','{agregar[3]}','{agregar[4]}','ACTIVO')"
        self.cursor.execute(bsdsql)
        self.conexion.commit()


    #modificar Proveedores
    def modificar(self,proveedor):
        sql=f"UPDATE proveedores SET tipo={proveedor[0]},docprov={proveedor[1]},nomprov={proveedor[2]},contprov={proveedor[3]},emaprov='{proveedor[4]}', direprov='{proveedor[5]}' WHERE docprov='{proveedor[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        
    #Eliminar proveedores
    def borrar(self,documentoProveedores):
        sql=f"UPDATE proveedores SET estado='INACTIVO' WHERE docprov='{documentoProveedores}'"
        self.cursor.execute(sql)
        self.conexion.commit()
