from tkinter import *
from tkinter import filedialog
from setup import *

# Definicion de variables

formatocargado = "sin formato cargado"
formatovalores = []
producto = ""


def hola():
    global formatovalores, formatocargado
    print(formatovalores)
    print(formatocargado)
    print("Hola mundo!")


def cargarformato(): # Cargamos archivo de formato

    formato = filedialog.askopenfilename(filetypes=(("Text files","*.txt"),("all files","*.*")))
    archivo = open(formato,"r")
    
    global formatovalores, formatocargado, producto
    formatovalores=[]

    for linea in archivo:
        formatovalores.append(int(linea))
    
    i = len (formato) - 5
    while  formato[i] != "/" :
        i -= 1
    formato = formato[i+1:len(formato)-4]
    producto = formato

    formato = Button(raiz, text=formato, fg="blue",command=cargarformato, width=30, height=1).place(x=100, y=0)
    formatocargado = formato   
     
    archivo.close()
    return

def NuevoFormato():
    print("Ingrese nombre de archivo")
    nombre = input()
    DefinirFormato(20,10,10,10,10,10,10,nombre)
    return

def EditarFormato():
    global formatovalores, formatocargado, producto
    if formatocargado == "sin formato cargado":
        return
    DefinirFormato(formatovalores[0],formatovalores[1],formatovalores[2],formatovalores[3],formatovalores[4],formatovalores[5],
                   formatovalores[6], producto)
    return
    
# Loop Principal

# Definio ventana principal raiz
raiz = Tk()
raiz.title("Vision PI")
raiz.geometry("520x480")
raiz.iconbitmap(r"C:\Users\tbermudez\Desktop\python\reconocimiento\ojo.ico")

# Agrego barra de manus
menu = Menu(raiz)
raiz.config(menu = menu)
subMenu = Menu(menu,tearoff=0)
menu.add_cascade(label = "Producto", menu = subMenu)
subMenu.add_command(label = "Cargar formato", command=cargarformato)
#subMenu.add_separator()
subMenu.add_command(label = "Editar formato", command=EditarFormato)
#subMenu.add_separator()
subMenu.add_command(label = "Nuevo formato", command=NuevoFormato)

#Agrego botones de inicio/fin
formato = Button(raiz, text=formatocargado, fg="blue",command=cargarformato, width=30, height=1).place(x=100, y=0)
detener = Button(raiz, text="DETENER", fg="red",command=hola).place(x=455, y=0)
iniciar = Button(raiz, text="INICIAR", fg="green",command=hola).place(x=400, y=0)

raiz.mainloop()