from pymongo import MongoClient
import pymongo

MONGO_URI='mongodb://localhost'
client=MongoClient(MONGO_URI)
DataBase=client ['BaseFiles']
collection=DataBase['Alumnos']

DataBase.seqs.insert_one({
    'collection' : 'Alumnos',
    'id' : 0
})

def insert_doc(doc):
    doc['_id'] = str(DataBase.seqs.find_one_and_update(
        { 'collection' : 'Alumnos' },
        update={'$inc': {'id': 1}},
        fields={'id': 1, '_id': 0},
        new=True
    ).get('id'))
    try:
        collection.insert_one(doc)
    except pymongo.errors.DuplicateKeyError as e:
        insert_doc(doc)

def validarstr(x): ##esto te esta dadndo errores? estas validaciones?
    while x.isalpha==False :
        print ("La entrada es incorrecta: Solo ingrese caracteres alfabeticos")
        print ("Vuelva a ingresar")
        x=input()
    return x

def validarnota(a):
    while a.isdigit()==False:
        print ("La entrada es incorrecta: Solo ingrese caracteres numéricos")
        print ("Vuelva a ingresar la nota")
        a=input()

    a=float(a)
    while a<0 or a>10:
        print ("La entrada es incorrecta: Solo ingrese notas en el intervalo [0,10]")
        print ("Vuelva a ingresar la nota")
        a=input()

    a=float(a)
    return a

def validarid(a):
    
    while a.isdigit()==False:
        print ("La entrada es incorrecta: Solo ingrese valores numéricos")
        print ("Vuelva a ingresar la id")
        a=input()
    return a

def agregarEst():
    n=validarstr(input("Ingrese el Nombre: "))

    ap=validarstr(input("Ingrese los Apellidos: "))

    n1=validarnota(input("Ingrese la 1era Nota: "))
    n2=validarnota(input("Ingrese la 2da Nota: "))
    new_student = {
        "name" : n,
        "lname" : ap,
        "Nota 1" : n1,
        "Nota 2" : n2
        }
    insert_doc(new_student)


def eliminarEst():
    id=validarid(input("Ingrese la id del estudiante que desea eliminar:\t "))
    r=collection.find_one({"_id":id})
    print("Se ha eliminado a {} {}".format(r["name"],r["lname"]))
    collection.delete_one({"_id":id})


def validaropc(a):
    a=str(a)
    while a.isdigit()==False:
        print ("La entrada es incorrecta: Solo ingrese valores validos")
        print ("Vuelva a ingresar la opción")
        a=input()
    a=int(a)
    while a<1 or a>4:
        print ("La entrada es incorrecta: Solo ingrese valores validos")
        print ("Vuelva a ingresar la opción")
        a=int(input())
    return a

def validaropcmenu(a):
    a=str(a)
    while a.isdigit()==False:
        print ("La entrada es incorrecta: Solo ingrese valores validos")
        print ("Vuelva a ingresar la opción")
        a=input()
    a=int(a)
    while a<1 or a>5:
        print ("La entrada es incorrecta: Solo ingrese valores validos")
        print ("Vuelva a ingresar la opción")
        a=int(input())
    return a

def editarEst():
    id = validarid(input("Ingrese la id del estudiante: \t"))
    opc = validaropc(input(
        '''\tSeleccione que desea editar
        \t1. Nombre del estudiante
        \t2. Apellido del estudiante
        \t3. Nota 1
        \t4. Nota 2
        '''))
    if opc == 1:
        name = input("Ingrese nuevo nombre: ")
        collection.update_one({"_id":id},{'$set': {"name": name}}, upsert = False)
    if opc == 2:
        lname = input("Ingrese nuevo apellido: ")
        collection.update_one({"_id":id},{'$set': {"lname": lname}}, upsert = False)
    if opc == 3:
        note1 = validarnota(input("ingrese nueva nota 1: "))
        collection.update_one({"_id":id},{'$set': {"Nota 1": note1}}, upsert = False)
    if opc == 4:
        note2 = validarnota(input("Ingrese nueva nota 2: "))
        collection.update_one({"_id":id},{'$set': {"Nota 2": note2}}, upsert = False)


def mostrarReg():
    registros = collection.find()
    print('\tid\t\tnombre\t\tapellido\t\tnota1\t\tnota2')
    for r in registros:
        print('\t'+r["_id"],end='')
        print('\t\t'+r["name"],end='')
        print('\t\t'+r["lname"],end='')
        print('\t\t\t'+str(r["Nota 1"]),end='')
        print('\t\t\t'+str(r["Nota 2"]))



def menu():
    opc = validaropcmenu(input(
        '''\tPrograma de Calificaciones
        \t1. Ingresar un estudiante
        \t2. Editar un estudiante
        \t3. Eliminar registro
        \t4. Mostrar Registros
        \t5. Salir
        '''))
    return opc


#no funciona lo del id

if __name__ == '__main__':
    opc=0
    while opc!=5:
        opc = menu()
        if opc == 1:
            agregarEst()
            print("Estudiante agregado correctamente")
        if opc == 2:
            editarEst()
            print("Estudiante actualizado correctamente")
        if opc == 3:
            eliminarEst()
        if opc == 4:
            mostrarReg()