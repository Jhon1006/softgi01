 def modificar(self,proveedor):
        sql=f"UPDATE proveedores SET tipo={proveedor[0]},docprov={proveedor[1]},nomprov={proveedor[2]},contprov={proveedor[3]},emaprov='{proveedor[4]}', direprov='{proveedor[5]}' WHERE docprov='{proveedor[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        
        self.cursor.execute(sql)
        self.conexion.commit()
    
    def borrar(self,docprov):
        sql=f"UPDATE proveedores SET BORRADO=1 WHERE docprov='{docprov}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        

