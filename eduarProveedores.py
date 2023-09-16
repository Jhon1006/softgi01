 def modificar(self,proveedor):
        sql=f"UPDATE proveedores SET tipo={proveedor[1]},docprov={proveedor[2]},={carrito[3]},modelo={carrito[5]},color='{carrito[4]}' WHERE placa='{carrito[0]}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        if carrito[6].filename != "":
            # Subir la foto nueva
            now = datetime.now()
            tiempo = now.strftime("%Y%m%d%H%M%S")
            nombre,extension = os.path.splitext(carrito[6].filename)
            nuevoNombre = "F" + tiempo + extension
            carrito[6].save("uploads/"+nuevoNombre)
            # Consultar y borrar la foto vieja
            sql = f"SELECT foto FROM carritos WHERE placa='{carrito[0]}'"
            self.cursor.execute(sql)
            fotoVieja = self.cursor.fetchall()
            self.conexion.commit()
            os.remove(os.path.join(self.programa.config['CARPETAU'],fotoVieja[0][0]))
            # Actualizo nombre de la nueva foto en la db
            sql = f"UPDATE carritos SET foto='{nuevoNombre}' WHERE placa='{carrito[0]}'"
            self.cursor.execute(sql)
            self.conexion.commit()
    
    def borrar(self,pla):
        sql=f"UPDATE carritos SET BORRADO=1 WHERE placa='{pla}'"
        self.cursor.execute(sql)
        self.conexion.commit()
        

