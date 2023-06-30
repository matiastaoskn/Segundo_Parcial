import sqlite3

with sqlite3.connect("mi_base_de_datos.db") as conexion:
    try:
        #Create Table
        sentencia = '''
                    create table Empleados
                    (
                        id integer primary key autoincrement,
                        nombre text,
                        apellido text,
                        sueldo real
                    )
                    '''
        # sentencia = '''
        # alter table Empleados
        # add direccion text
        #'''

        # sentencia = '''
        # insert into Empleados(nombre, apellido, sueldo, direccion) values(?,?,?,?)
        # '''
        # nombre = "Matias"
        # apellido = "Skenen"
        # sueldo = 150.000
        # direccion = "casa"

        #conexion.execute(sentencia)
        #Parametros#
        #conexion.execute(sentencia, (nombre, apellido, sueldo, direccion))

        sentencia = 'select * from Empleados order by sueldo desc limit 3'
        cursor = conexion.execute(sentencia)

        for fila in cursor:
            print(fila)


        #Actualizo valores
        id = 3
        sueldo = 100

        sentencia = 'update Empleados set sueldo = ? where id = ?'
        cursor = conexion.execute(sentencia, (sueldo, id))

        print("Tabla creada!")
    except:
        print("Error!")
        