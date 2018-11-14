from tkinter import *
from tkinter import ttk

class Pantalla(Frame):
    """Crea la intefaz gráfica del programa
    """
    def __init__(self, master, memoria, padre):
        """Crea la instancia de la clase Pantalla, la cual toma como parametros
           la dirección de la pantalla en la cual se colocaran los objetos de la
           interfaz, la memoria del sistema y el padre inicial del sistema.

           Entardas:
                     master: ventana que se utilizará
                     memoria: memoria del sistema
                     padre: padre principal

           Salida:
                     Pone ciertas caracteristicas de la ventana y llama a otros 
           	     metodos para que terminen de llenar la ventana
        """

        Frame.__init__(self, master) 
        self.root = master # Crea la pantalla
        self.root.resizable(0,0)
        self.root.title("Pantalla")
        self.memoria = memoria
        self.padre = padre
        self.index = 0 # Indice de la linea del cuadro de texto
        self.lstDir = [] # Lista de directorios

        self.objeto = Directorio(nombre=self.padre, iid='\\')
        self.objeto.direccion += self.padre
        
        self.listcolor = ['black', '#000000'] # Lista de colores utilizados
        self.lstDir.append(self.objeto)
        
        self.lstArc = [] # Lista de directorios
        self.createWidgets() # Ejecuta el método createWidgets

    def createWidgets(self):
        """Crea los widgets que se utilizarán en la pantalla

           Salidas: Crea los objetos que se utilizarán en la pantalla como la
                    notebook, el cuadro de texto, los scrollbar, los treeviews y
                    el canvas de la memoria.
        """
        
        #Imagenes
        imagenV = PhotoImage(file='1.gif')
        imagenL = PhotoImage(file='2.gif')
        self.imagenes = {'vacio':imagenV, 'lleno':imagenL} # Imagenes de los directorios
        
        # Style
        style = ttk.Style()

        # Text
        self.txtIns = Text(self.root, font=("Terminal",10), width=60, height=60, bg="black", fg="white") # Crea el cuadro de texto
        self.txtIns.grid(row=0, column=0)

        # Scroll
        self.scrollInsV = ttk.Scrollbar(self.root, orient=VERTICAL, command=self.txtIns.yview) # Crea el scrollbar del cuadro de texto
        self.txtIns["yscrollcommand"] = self.scrollInsV.set # Vincula el scroolbar con el cuadro de texto
        
        self.scrollInsV.grid(row=0, column=1, sticky=(N,S,W))

        # Notebook
        self.NB = ttk.Notebook(self.root, height=695, width=1040) # Crea el Notebook
        self.NB.enable_traversal() # Activa el boton TAB
        
        self.pag1 = ttk.Frame(self.NB) # Crea la pantalla 1 y 2
        self.pag2 = ttk.Frame(self.NB) #

        self.NB.add(self.pag1, text='Mapa')       # Vincula la página 1 y 2
        self.NB.add(self.pag2, text='Estructura') #

        self.NB.grid(row=0, column=2)

        # Canvas
        self.canvas = Canvas(self.pag1,height = 695,width = 1040,bg = 'white') # Crea el canvas para la memoria 
        self.canvas.grid()

        # Cuadricula
        self.repMemoria = cuadricula(self.canvas) # Dibuja la memoria
        self.repMemoria.dibujar()                 #

        # Treeview\Notebook
        self.tree = ttk.Treeview(self.pag2, height=30) # Crea el Treeview de la estructura de árbol
        self.tree.grid(row=0, column=0, sticky=(N,S,E,W))
        self.tree["columns"]=("one")

        self.tree.column("#0", width=300)
        self.tree.heading("#0")

        self.tree.column("one", width=0)
        self.tree.heading("one")

        self.tree.insert("", 0, self.padre, image=self.imagenes['vacio'], open=True, text=self.padre) # Crea el objeto raíz del sistema
        self.tree.item(self.padre, text='→%s'%self.padre)
        self.txtIns.insert("0.0 + %dl" %self.index, 'C: %s> ' %self.objeto.direccion)
        
        # Treeview\Notebook\Scroll
        self.scrollTreeV = ttk.Scrollbar(self.pag2, orient=VERTICAL,command=self.tree.yview) # Crea el scrollbar del treeview
        self.tree["yscrollcommand"] = self.scrollTreeV.set # Vincula el scroolbar con el treeview

        self.scrollTreeV.grid(row=0, column=1, sticky=(N,S,W))

        # Treeview\Notebook\Pag2
        self.treeNBpag2 = ttk.Treeview(self.pag2, height=38) # Crea el Treeview de la reprecentación de objetos
        self.treeNBpag2["columns"]=("one", "two", "three")

        self.treeNBpag2.column("#0", width=390)
        self.treeNBpag2.heading("#0", text='Nombre')
        
        self.treeNBpag2.column("one", width=102)
        self.treeNBpag2.heading("one", text='Tipo')

        self.treeNBpag2.column("two", width=102)
        self.treeNBpag2.heading("two", text='Tamaño')

        self.treeNBpag2.column("three", width=102)
        self.treeNBpag2.heading("three", text='Color')
        
        self.treeNBpag2.grid(row=0, column=2, sticky=(N,S,E,W))
        
        # Treeview\Notebook\Pag2\Scroll
        self.scrollTreeNBpag2 = ttk.Scrollbar(self.pag2, orient=VERTICAL,command=self.treeNBpag2.yview) # Crea el scrollbar de la reprecentación de objetos
        self.treeNBpag2["yscrollcommand"] = self.scrollTreeNBpag2.set # Vincula el scroolbar con de la reprecentación de objetos

        self.scrollTreeNBpag2.grid(row=0, column=19, sticky=(N,S,W))

        # Comandos
        self.root.bind("<Return>", lambda p: self.Cargue()) # Enlaza la ventana con el método
        self.tree.bind("<1>", self.Print)                   #

    def Print(self, event):
        """ Imprime el contenido del directorio al darle click a uno de ellos
            en el treeview.

            Entrada:
                     event: coordenadas de la posición indicada

            Salida:
                     Contenido del directorio indicado en el treeview 
        """
        
        while self.treeNBpag2.identify_row(30):       ##
            borrar = self.treeNBpag2.identify_row(30)  # Borra lo escrito en el treeview
            self.treeNBpag2.delete(borrar)            ##
            
        p = self.tree.identify_row(event.y)                                                                                 ##
        if p != '':                                                                                                          #
            for a in self.lstDir:                                                                                            #
                if a.iid == p:                                                                                               #
                    for b in a.lista:                                                                                        #
                        t = 0                                                                                                #
                        for tam in self.lstArc:                                                                              #
                            if b.direccion in tam.direccion:                                                                 # Imprime los elementos en el treeview 
                                t += tam.tam                                                                                 #
                        self.treeNBpag2.insert('', 'end', b.nombre, text=b.nombre.replace('_', ' '),                         #
                                               values=('Directorio','',''))                                                  #
                    for b in a.archivos:                                                                                     #
                        self.treeNBpag2.insert('', 'end', b.nombre, text=b.nombre.replace('_', ' '),                         #
                                               values=('Archivo','%d bloqu%s'%(b.tam,'e' if b.tam <= 1 else 'es'),b.color)) ##

    def Cargue(self):
        """ Carga la instrucción escrita en el cuadro de texto

            Salida:
                    Escribe en el cuadro de texto los errores o la información
                    necesaria para la siguiente linea.
        """

        text = self.txtIns.get("0.0 + %dl" %self.index, "end") # Lee la linea escrita en el índice indicado
        text = text.strip()
        text = text[len(self.objeto.direccion)+5:]

        if text != "":
            x = Scan(text, self.memoria, self.tree, self.padre, self.lstDir, self.lstArc, self.imagenes, self.repMemoria, self.listcolor, self.objeto).tokeniza() # Escanea la linea
            if type(x[0]) == tuple:
                if x[0][0] == None:
                    if x[1][0] == 'format':                                                                           ##
                        memoria = Disponibles(cantBloque = int(x[1][1]), listBloque=[])                                #
                        self.memoria =  memoria                                                                        #
                        self.objeto = Directorio(nombre='\\', padre='', canSubDir=0,                                   # Si el comando fue 'format' crea una memoria
                                                 listArchivo=[], direccion='\\', listSubDir=[],                        # nueva con los bloques restantes, crea un nuevo
                                                 iid='\\', lista=[], archivos=[])                                      # objeto raíz y posiciona el puntero en él,
                        self.lstDir = [self.objeto]                                                                    # limpia la lista de archivos, de directorios y
                        self.lstArc = []                                                                               # de colores.
                        self.tree.insert("", 0, self.objeto.iid, image=self.imagenes['vacio'], open=True, text='\\')   #
                        self.tree.item(self.objeto.iid, text='→%s'%self.objeto.nombre)                                 #
                        self.listcolor = []                                                                           ##
                        
                    elif x[1][0] == 'cd':                                                               ##
                        self.tree.item(self.objeto.iid, text=self.objeto.nombre.replace('_', ' '))       # Si el comando fue 'cd' coloca un identificador en el nombre y elimina el
                        self.objeto = x[0][1]                                                            # identificador del pasado.
                        self.tree.item(self.objeto.iid, text='→%s'%self.objeto.nombre.replace('_', ' ')) #
                        self.padre = self.objeto.nombre                                                 ##

                    elif x[1][0] == 'file':            # Si el comando fue file agrega el color del archivo a la lista de colores utilizados
                        self.listcolor.append(x[0][1]) #

                    elif x[1][0] == 'del':                                                                               ##
                        if isinstance(x[0][1], str):                                                                      #
                            self.listcolor.remove(x[0][1])                                                                #
                        elif isinstance(x[0][1], list):                                                                   # Si el comando fue 'del' elimina el color
                            for a in x[0][1]:                                                                             # de la lista de colores utilizados, modifica
                                self.listcolor.remove(a)                                                                  # la lista de archivos y directorios, y crea
                            self.lstArc = x[0][3]                                                                         # un nuevo objeto raíz si de elimina todos
                            self.lstDir = x[0][4]                                                                         # los objetos del sistema
                        elif x[1][1] == '\\':                                                                             #              ↑
                            self.objeto = Directorio(nombre='\\', padre='', canSubDir=0,                                  #              |
                                                     listArchivo=[], direccion='\\', listSubDir=[],                       #              |
                                                     iid='\\', lista=[], archivos=[])                                     #              |
                            self.lstDir = [self.objeto]                                                                   #              |
                            self.lstArc = []                                                                              #              |
                            self.listcolor = []                                                                           #              |
                            self.tree.insert("", 0, self.objeto.iid, image=self.imagenes['vacio'], open=True, text='\\')  #              |
                            self.tree.item(self.objeto.iid, text='→%s'%self.objeto.nombre)                                #              |
                            self.tree.item(self.objeto.iid, text=self.objeto.nombre)                                     ##              |
                                                                                                                          #              |
                    elif x[1][0] == 'rd':                                                                                ##              |
                        if isinstance(x[0][1], list):                                                                     #              |
                            for a in x[0][1]:                                                                             #              |
                                self.listcolor.remove(a)                                                                  #              |
                            self.lstArc = x[0][3]                                                                         #              |
                            self.lstDir = x[0][4]                                                                         #              |
                        elif x[1][1] == '\\':                                                                             # Hace exactamente lo mismo
                            self.objeto = Directorio(nombre='\\', padre='', canSubDir=0,                                  #
                                                     listArchivo=[], direccion='\\', listSubDir=[],                       #
                                                     iid='\\', lista=[], archivos=[])                                     #
                            self.tree.item(self.objeto.iid, text='→%s'%self.objeto.nombre)                                #
                            self.lstDir = [self.objeto]                                                                   #
                            self.lstArc = []                                                                              #
                            self.listcolor = []                                                                           #
                            self.tree.insert("", 0, self.objeto.iid, image=self.imagenes['vacio'], open=True, text='\\')  #
                            self.tree.item(self.objeto.iid, text=self.objeto.nombre)                                     ##

                    elif x[1][0] == 'dir':                                           ##
                        self.index += 1                                               # Si el comando fue 'dir' imprime los elementos del objeto
                        self.txtIns.insert("0.0 + %dl" %self.index, '%s\n' %x[0][1]) ##
                    
                    self.index += x[0][2]
                    self.txtIns.insert("0.0 + %dl" %self.index, 'C: %s> ' %self.objeto.direccion)
                else:                                                                             ##
                    self.index += x[0][2]                                                          #
                    self.txtIns.insert("0.0 + %dl" %self.index, '%s\n' %x[0][0])                   #
                    self.index += x[0][2]                                                          #
                    self.txtIns.insert("0.0 + %dl" %self.index, 'C: %s> ' %self.objeto.direccion)  #
            else:                                                                                  #
                self.index += x[2]                                                                 # Si se cometió un error al escribir el comando
                self.txtIns.insert("0.0 + %dl" %self.index, '%s\n' %x[0])                          #
                self.index += x[2]                                                                 #
                self.txtIns.insert("0.0 + %dl" %self.index, 'C: %s> ' %self.objeto.direccion)      #
        else:                                                                                      #
            self.index += 1                                                                        #
            self.txtIns.insert("0.0 + %dl" %self.index, 'C: %s> ' %self.objeto.direccion)         ##

class Scan:
    """Implementa un tokenizador que reconoce los tokens de un lenguaje que contiene identificadores      
    """
    def __init__(self, linea, memoria, tree, padre, lstDir, lstArc, imagenes,cuadri,listcolor,objeto):
        """Crea una instancia de la clase Tokenizador.

           Entradas:
                     linea: linea leida en el método Cargue de la clase Pantalla
                     memoria: memoria principal del sistema
                     tree: objeto treeview en el cual se crearon objetos
                     padre: padre del objeto en el que se está trabajando
                     lstDir: lista de directorios
                     lstArc: lista de archivos
                     imagenes: diferentes imagenes que tendran los objetos escritos en el treeview
                     cuadri: cuadricula de la reprecentación de la memoria del sistema
                     listcolor: lista de colores usados
                     objeto: objeto en el cual se esta tabajando

           Salida:
                     Si el comando cumple con los parametros establecidos, retorna una tupla con las
                     diferentes salidas de cada método, así como la una lista del comando escrito
                     para su verificación en en el método Cargue de la clase Pantalla; sino retorna
                     un mensaje de error el se cual se imprimirá en el cuadro de texto.
        """
        
        self.linea = linea
        self.memoria = memoria
        self.tree = tree
        self.padre = padre
        self.lstDir = lstDir
        self.lstArc = lstArc
        self.imagenes = imagenes
        self.cuadri = cuadri
        self.listcolor = listcolor
        self.objeto = objeto
 
    def _get_id(self):
        """Recibe un string que inicia con un caracter y retorna (identificador, restolinea)
        """
        i = 0
        while (i < len(self.linea)) and ((self.linea[i].isalpha()) or \
                                         (self.linea[i].isdigit()) or \
                                         (self.linea[i] is '_') or \
                                         (self.linea[i] is '\\')):
            i += 1
        return self.linea[:i], self.linea[i:]
  
    def tokeniza(self):
        """Lee la línea del cuadro de comandos

           Entadas:
                    linea: lista con los elementos
        """
        linea = self.linea.lstrip() # Quita los blancos al inicio de la linea
        lista = [] # Guarda los elementos de la linea en una lista
        
        while linea:
          if linea[0].isalpha(): # String
              idt, linea = Scan(linea, self.memoria, self.tree, self.padre, self.lstDir, self.lstArc, self.imagenes,self.cuadri,self.listcolor,self.objeto)._get_id() #idt = palabra de la línea
              lista.append(idt)

          elif linea[0].isdigit(): # Numero
              idt, linea = Scan(linea, self.memoria,self.tree, self.padre, self.lstDir, self.lstArc, self.imagenes,self.cuadri,self.listcolor,self.objeto)._get_id() #idt = palabra de la línea
              lista.append(idt)
              
          elif linea[0] == '.' : # Puntos
              if linea != '..' and linea != '.':
                  return 'Comando incorrecto', linea, 1
              lista.append(linea)
              linea = ""

          elif linea[0] == '#' and len(linea) == 7: # Color hexadecimal
              for a in linea: 
                  if a not in 'abcdefABCDEF1234567890#':
                      return 'El valor hexadecimal no es válido', linea, 1
              lista.append(linea)
              linea = ""

          elif linea[0:1] == '\\': # Dirección y raíz
              idt, linea = Scan(linea, self.memoria,self.tree, self.padre, self.lstDir, self.lstArc, self.imagenes,self.cuadri,self.listcolor,self.objeto)._get_id() #idt = palabra de la línea
              lista.append(idt)
                
          elif linea[0] in ' ':  # Saca los espacios
              idt, linea = linea[0],linea[1:]
              
          else:
              return 'Comando incorrecto', linea, 1
            
        if len(lista) <= 4 and not len(lista) == 0:
            x = CodigoIntermedio(lista, self.memoria, self.tree, self.padre, self.lstDir, self.lstArc, self.imagenes,self.cuadri,self.listcolor,self.objeto)._verificar()
            return (x,lista)
        else:
            return 'Comando incorrecto', linea, 1
  
class CodigoIntermedio:
 
    def __init__(self, lista, memoria, tree, padre, lstDir, lstArc, imagenes, cuadri,listcolor,objeto):
        """Crea una instancia de la clase CodigoIntermedio.

           Entradas:
                     lista: lista de tokens
                     memoria: memoria principal del sistema
                     tree: objeto treeview en el cual se crearon objetos
                     padre: padre del objeto en el que se está trabajando
                     lstDir: lista de directorios
                     lstArc: lista de archivos
                     imagenes: diferentes imagenes que tendran los objetos escritos en el treeview
                     cuadri: cuadricula de la reprecentación de la memoria del sistema
                     listcolor: lista de colores usados
                     objeto: objeto en el cual se esta tabajando
                     
           Salida:
                     Estas salidas dependen del método en el cual se trabaje, ya sea para modificar el
                     objeto del directorio actual, o para modificar la lista de directorios, archivos o
                     colores.
        """
        
        self.lista = lista
        self.memoria = memoria
        self.tree = tree
        self.padre = padre
        self.lstDir = lstDir
        self.lstArc = lstArc
        self.imagenes = imagenes
        self.cuadri = cuadri
        self.listcolor = listcolor
        self.objeto = objeto
     
    def _verificar(self):
        """Verifica que no ocurran errores de sintanxis y ejecuta el comando.

           Entradas:
                     lista: lista de la linea que contiene una palabra reservada en la posición [0]

           Salidas:
                     Retorna una tupla con las diferentes salidas.
                     Estas salidas dependen de cada método.
                     Retorna el índece de la proxima línea a leer.
                     Retorna en la primera posición de la tupla un None si el comando fue escrito
                     y ejecutado con exito, sino retorna un mensaje de error.
        """

        if len(self.lista) == 1:
            
            if self.lista[0].lower() == 'dir': # Muestra los archivos del directorio actual
                msj = 'Directorio de %s\n' %self.objeto.nombre.replace('_', ' ')                                        ##
                for a in self.objeto.listSubDir:                                                                         #
                    msj += '<DIR>   %s\n' %a.replace('_', ' ')                                                           #
                for a in self.objeto.listArchivo:                                                                        # Crea el mensaje sacando los elementos del
                    msj += '<FILE>  %s\n' %a.replace('_', ' ')                                                           # directorio actual
                msj += '%d directori%s\n' %(len(self.objeto.listSubDir), 'os' if len(self.objeto.listSubDir)>1 else 'o') # Retorna el mensaje y la próxima línea
                msj += '%d archiv%s' %(len(self.objeto.listArchivo), 'os' if len(self.objeto.listArchivo)>1 else 'o')    # a leer
                return None, msj, len(self.objeto.listSubDir) + len(self.objeto.listArchivo) + 3                         #
            else:                                                                                                       ##
                return 'Comando incorrecto', None, 1 # Mensaje de error
        
        elif len(self.lista) == 2:
            
            if self.lista[0].lower() == 'cd': # Ingresa a un archivo
                if self.lista[1] == '.':        # No modifica ningúna posición en la estructura
                    return None, self.objeto, 1 # Retorna el mismo objeto y la próxima línea a leer
                
                elif self.lista[1] == '..':    ##
                    objeto = self.objeto.padre  # Regresa al directorio padre
                    return None, objeto, 1     ## Retorna el directorio padre y la próxima línea a leer
                
                else:                                           ##
                    if self.lista[1] in self.objeto.listSubDir:  #
                        for a in self.objeto.lista:              # Ingresa a un directorio en el directorio actual
                            if a.nombre == self.lista[1]:        # Retorna el directorio leido y la próxima línea a leer
                                return None, a, 1               ##
                    else:                                          ##
                        for a in self.lstDir:                       #
                            if self.lista[1] == '\\':               # Ingresa a un directorio por medio de una dirección específica
                                return None, a, 1                   # Retorna el directorio leido y la próxima línea a leer
                            elif a.direccion[:-1] == self.lista[1]: #
                                return None, a, 1                  ##
                    return 'El directorio no existe', None, 1 # Mensaje de error

            elif self.lista[0].lower() == 'format' and self.lista[1].isdigit(): # Formatea la memoria
                self.cuadri.vaciar()                     ##
                self.cuadri.bloques = int(self.lista[1])  # Modifica la memoria
                self.cuadri.dibujar()                     # Retorna la próxima línea a leer
                self.tree.delete('\\')                    #
                return None, None, 1                     ##

            elif self.lista[0].lower() == 'dir': # Muestra información
                if self.lista[1] in self.objeto.listArchivo:                                                                                              ##
                    for a in self.objeto.archivos:                                                                                                         # Muestra la infomación del archivo
                        if a.nombre == self.lista[1]:                                                                                                      # Retorna el mensaje y la próxima
                            msj = 'Archivo %s \ncolor: %s \ntamaño: %d \nbloques: %s' %(a.nombre.replace('_', ' '), a.color, a.tam, a.obtenerBloques()[0]) # línea a leer
                            return None, msj, 4                                                                                                           ##
                elif self.lista[1] in self.objeto.listSubDir:                                                    ##
                    for a in self.objeto.lista:                                                                   #
                        if a.nombre == self.lista[1]:                                                             #
                            msj = 'Directorio %s\n' %a.nombre.replace('_', ' ')                                   #
                            for b in a.listSubDir:                                                                # Muestra la información de un directorio en el
                                msj += '<DIR>   %s\n' %b.replace('_', ' ')                                        # directorio actual
                            for b in a.listArchivo:                                                               # Retorna el mensaje y la próxima línea y la próxima
                                msj += '<FILE>  %s\n' %b.replace('_', ' ')                                        # línea a leer
                            msj += '%d directori%s\n' %(len(a.listSubDir), 'os' if len(a.listSubDir)>1 else 'o')  #
                            msj += '%d archiv%s' %(len(a.listArchivo), 'os' if len(a.listArchivo)>1 else 'o')     #
                            return None, msj, len(a.listSubDir) + len(a.listArchivo) + 3                         ##
                else:
                    for a in self.lstDir:                                                             ##
                        if a.direccion[:-1] == self.lista[1]:                                          # Muestra la información de un directorio por medio una
                            x = CodigoIntermedio(['dir', a.nombre], self.memoria, self.tree,           # dirección específica
                                                 self.padre, self.lstDir, self.lstArc, self.imagenes,  # Retorna el mensaje y la próxima línea y la próxima línea a
                                                 self.cuadri, self.listcolor, a.padre)._verificar()    # leer
                            return x                                                                  ##
                    return 'El objeto no existe', None, 1 # Mensaje de error
                    
            elif self.lista[0].lower() == 'del': # Borra elementos
                if self.lista[1] in self.objeto.listArchivo:                                     ##
                    m = 0                                                                         #
                    for a in self.lstArc:                                                         # Borra el archivo indicado, buscando desde la lista de archivos
                        if a.nombre == self.lista[1] and a.padre == self.objeto.nombre:           # y comparandolo por su nombre y el padre del archivo para 
                            self.objeto.borrarArchivo(a)                                          # verificar que sea esté el archivo incluido en la lista de
                            self.cuadri.eliminar(a.iid)                                           # archivos del directorio actual
                            if self.objeto.listArchivo == []:                                     # Retorna el color a elinimar de la lista de colores usados y 
                                self.tree.item(self.objeto.nombre, image=self.imagenes['vacio'])  # la próxima línea a leer
                            break                                                                 #
                        else:                                                                     #
                            m += 1                                                                #
                    self.lstArc.pop(m)                                                            #
                    return None, a.color, 1                                                      ##
                
                elif self.lista[1] in self.objeto.listSubDir:       ##
                    color = []                                       #
                    nuevaArc = []                                    #
                    nuevaDir = []                                    #
                    for a in self.objeto.lista:                      #
                        if a.nombre == self.lista[1]:                #
                            self.tree.delete(a.iid)                  #
                            break                                    # Borra el directorio indicado, buscando desde la lista directorios y comparandolo por su nombre
                                                                     # lo elimina por su iid. Luego borra todos los directorios de la lista de directorios del
                    for n in self.lstDir:                            # sistema por medio de su dirección. Si esta direccion no se encuentra en la dirección del
                        if a.direccion not in n.direccion:           # directorio borrado, lo agrega a una lista de directorios nuevos para retornarla y modificar
                            nuevaDir.append(n)                       # a la lista total de directoios. La eliminación de archivos es igual solo que esta módifica 
                                                                     # la lista total de archivos y la lista de colores usados. Si el directorio a borrar es el raíz
                    for b in self.lstArc:                            # borra completamente la lista total de directorios, archivos y colores.
                        if a.direccion in b.direccion:               # Si borra el directorio raíz retorna la próxima línea a leer
                            color.append(b.color)                    # Si borra algún otro directorio retorna la lista de colores a borrar, la lista de archivos y
                            a.borrarArchivo(b)                       # directorios nueva y la próxima línea a leer
                            self.cuadri.eliminar(b.iid)              #
                        else:                                        #
                            nuevaArc.append(b)                       #
                                                                     #
                    self.lstArc = nuevaArc                           #
                    self.lstDir = nuevaDir                           #
                    self.objeto.borrarSubDir(a)                      #
                    return None, color, 1, self.lstArc, self.lstDir  #
                                                                     #
                elif self.lista[1] == '\\':                          #
                    for a in self.lstArc:                            #
                        a.eliminaArchivo()                           #
                        self.cuadri.eliminar(a.iid)                  #
                    self.tree.delete('\\')                           #
                    return None, None, 1                            ##
                
                else:
                    if self.objeto.direccion[:-1] != self.lista[1]:                                      ##
                        for a in self.lstDir:                                                             # Borra el directorio por medio de una dirección específica
                            if a.direccion[:-1] == self.lista[1]:                                         # Retorna la lista de colores a borrar, la lista de archivos y
                                x = CodigoIntermedio(['del', a.nombre], self.memoria, self.tree,          # la próxima línea a leer
                                                     self.padre, self.lstDir, self.lstArc, self.imagenes, #
                                                     self.cuadri,self.listcolor,a.padre)._verificar()    ##
                                return x
                        return 'El nombre que escribió no existe', None, 1     ##
                    else:                                                       # Mensajes de error
                        return 'No puede borrar el directorio actual', None, 1 ##
                    

            elif self.lista[0].lower() == 'md': # Crear un directorio
                iid = ''                                                                                                 ##
                if self.lista[1] != '\\':                                                                                 # Crea un directorio, verificando que no
                    if self.lista[1] not in self.objeto.listSubDir:                                                       # exista uno con el mismo nombre en el
                        iid = self.lista[1]                                                                               # directorio actual. Este crea un iid
                        while self.tree.exists(iid):                                                                      # único para cada directorio, para que
                            iid += '.'                                                                                    # puedan ser eliminados en el treeview.
                        nom = self.lista[1].replace('_', ' ')                                                             #
                        x = Directorio(nombre=self.lista[1], padre=self.objeto, canSubDir=0,                              # Esto lo hace agregandole un punto si
                                       listArchivo=[], direccion=self.objeto.direccion + self.lista[1] + '\\',            # ya existe un directorio con ese mismo
                                       listSubDir=[], iid=iid, lista=[], archivos=[])                                     # iid
                        self.tree.insert(self.objeto.iid, 'end', iid, image=self.imagenes['vacio'], open=True, text=nom)  # Retorna la próxima línea a leer
                        self.objeto.agregaSubDir(x)                                                                       #
                        self.lstDir.append(x)                                                                             #
                        return None, None, 1                                                                             ##
                    else:                                                  ##
                        return 'El directorio ya existe', None, 1           # Mensajes de error
                else:                                                       #
                    return 'No pueden existir 2 directorios raíz', None, 1 ##

            elif self.lista[0].lower() == 'rd': # Elimina un directorio
                if self.lista[1] in self.objeto.listSubDir:         ##
                    color = []                                       #
                    nuevaArc = []                                    #
                    nuevaDir = []                                    #
                    for a in self.objeto.lista:                      #
                        if a.nombre == self.lista[1]:                #
                            self.tree.delete(a.iid)                  #
                            break                                    # Borra el directorio indicado, buscando desde la lista directorios y comparandolo por su nombre
                                                                     # lo elimina por su iid. Luego borra todos los directorios de la lista de directorios del
                    for n in self.lstDir:                            # sistema por medio de su dirección. Si esta direccion no se encuentra en la dirección del
                        if a.direccion not in n.direccion:           # directorio borrado, lo agrega a una lista de directorios nuevos para retornarla y modificar
                            nuevaDir.append(n)                       # a la lista total de directoios. La eliminación de archivos es igual solo que esta módifica 
                                                                     # la lista total de archivos y la lista de colores usados. Si el directorio a borrar es el raíz
                    for b in self.lstArc:                            # borra completamente la lista total de directorios, archivos y colores.
                        if a.direccion in b.direccion:               # Si borra el directorio raíz retorna la próxima línea a leer
                            color.append(b.color)                    # Si borra algún otro directorio retorna la lista de colores a borrar, la lista de archivos y
                            a.borrarArchivo(b)                       # directorios nueva y la próxima línea a leer
                            self.cuadri.eliminar(b.iid)              #
                        else:                                        #
                            nuevaArc.append(b)                       #
                                                                     #
                    self.lstArc = nuevaArc                           #
                    self.lstDir = nuevaDir                           #
                    self.objeto.borrarSubDir(a)                      #
                    return None, color, 1, self.lstArc, self.lstDir  #
                                                                     #
                elif self.lista[1] == '\\':                          #
                    for a in self.lstArc:                            #
                        a.eliminaArchivo()                           #
                        self.cuadri.eliminar(a.iid)                  #
                    self.tree.delete('\\')                           #
                    return None, None, 1                            ##
                
                else:
                    if self.objeto.direccion[:-1] != self.lista[1]:                                      ##
                        for a in self.lstDir:                                                             # Borra el directorio por medio de una dirección específica
                            if a.direccion[:-1] == self.lista[1]:                                         # Retorna la lista de colores a borrar, la lista de archivos y
                                x = CodigoIntermedio(['del', a.nombre], self.memoria, self.tree,          # la próxima línea a leer
                                                     self.padre, self.lstDir, self.lstArc, self.imagenes, #
                                                     self.cuadri,self.listcolor,a.padre)._verificar()    ##
                                return x
                        return 'El nombre que escribió no existe', None, 1     ##
                    else:                                                       # Mensajes de error
                        return 'No puede borrar el directorio actual', None, 1 ##
            else:
                return 'Comando incorrecto', None, 1

        elif len(self.lista) == 3:

            if self.lista[0].lower() == 'expand' and self.lista[2].isdigit() == True: # Expandir el tamaño de un archivo
                if not len(self.memoria.listBloque) < int(self.lista[2]):        ##
                    for a in self.objeto.archivos:                                # Expande el archivo si hay espacio suficiente en la memoria del sistema. Verifica
                        if self.lista[1] == a.nombre:                             # que el archivo exista en la lista de archivos del directorio actual.
                            a.aumentarEspacio(int(self.lista[2]))                 # Retorna la próxima línea a leer
                            self.cuadri.agregar(a.color,int(self.lista[2]),a.iid) #
                            return None, None, 1                                 ##
                    return 'El archivo no existe', None, 1        ##
                else:                                              #
                    return 'No hay espacio en la memoria', None, 1 # Mensajes de error
                                                                   #
            else:                                                  #
                return 'Comando incorrecto', None, 1              ##

        elif len(self.lista) == 4:
            
            if self.lista[0].lower() == 'file' and self.lista[2].isdigit() == True: # Crea un archivo
                iid = ''                                                                             ##
                if not len(self.memoria.listBloque) < int(self.lista[2]):                             #
                    if self.lista[1] not in self.objeto.listArchivo:                                  #
                        if self.lista[3] not in self.listcolor:                                       # Crea un archivo, verifincando que no exista una con el mismo
                            iid = self.lista[1]                                                       # nombre en el directorio actual. Este crea un iid único para 
                            for a in self.lstArc:                                                     # cada archivo, para que puedan ser eliminados de la memoria.
                                if self.lista[1] == a.nombre:                                         # Esto lo hace agregandole un punto si ya existe un archivo con
                                    iid += '.'                                                        # el mismo iid.
                            tono = self.lista[3].replace('_', ' ')                                    # Retorna el color utilizado y la próxima línea a leer
                            y = Archivo(nombre=self.lista[1], tam=int(self.lista[2]), bloques=[],     # 
                                        color=tono, padre=self.padre, memoria=self.memoria,           #
                                        direccion=self.objeto.direccion, iid=iid)                     #
                            self.objeto.agregaArchivo(y)                                              #
                            self.lstArc.append(y)                                                     #
                            self.tree.item(self.objeto.iid, image=self.imagenes['lleno'])             #
                            self.cuadri.agregar(tono,int(self.lista[2]),iid)                          #
                            return None, self.lista[3], 1                                            ##
                        else:                                                                ##
                            return 'Este color ya está siendo usado', None, 1                 #
                    else:                                                                     #
                        return 'El directorio ya contiene un archivo con ese nombre', None, 1 #
                else:                                                                         # Mensajes de error
                    return 'No hay espacio en la memoria', None, 1                            #
            else:                                                                             #
                return 'Comando incorrecto', None, 1                                          #
        else:                                                                                 #
            return 'Comando incorrecto', None, 1                                             ##

class cuadricula:
    """Clase que crea la cuadricula donde se va a simular la memoria

       Entradas:
                 master: canvsa donde se va a dibujar
                 bloques: cantidad de bloques que se desean agregar

       Salidas:
                 Va a dibujar una cuadricula segun las especificaciones ingresadas
    """
    
    def __init__(self,master,bloques = 3174):
        self.master = master
        
        self.cuadrados = [] # Matriz donde se van a almacenar las filas y columnas de la cuadricula
        
        self.bloques = bloques
        

    def dibujar(self):
        """Metodo que dibuja la cuadricula de acuerdo a las epsecificaiones
        """
        
        limite = 0 # Variable para la salida del ciclo
        
        for y in range(46): #Ciclo para crear las filas
            fila = [] #Lista que va a contener las filas
            for x in range(69): #Ciclo para crear las columnas
                if limite == self.bloques: #Condicion de salida 
                    break

                else:
                    posx1 = 15 * x
                    posy1 = 15 * y
                    posx2 = 15 * (x + 1)
                    posy2 = 15 * (y + 1)
                    cuadro = cuadrado(self.master,posx1,posx2,posy1,posy2,color = 'black') # Se dibuja el cuadrado
                    fila.append(cuadro)
                    limite += 1
            
            if limite == self.bloques:
                self.cuadrados.append(fila)
                break

            elif len(fila) < 15:
                self.cuadrados.append(fila)
                break

            else:
                self.cuadrados.append(fila)

    def vaciar(self):
        """Metodo que borra la cuadricula

           Salidas:
                    Se borra todo el contenido del canvas y se vacia la lista con los cuadrados
        """
        
        self.master.delete('all')
        self.cuadrados = []

    def agregar(self,color,cantidad,nombre):
        """Metodo que va a modificar los colores de un cantidad determinada de cuadros

           Entradas:
                     color: color que se le va a poner a una cantidad especifica cuadros
                     cantidad: cantidad de cuadros a cambiar
                     nombre: identificador para saber a cual archivo pertenece
           Salidas:
                     Va a cambiar el color
        """
        
        rellenados = 0
        for x in range(len(self.cuadrados)):
            for y in range(len(self.cuadrados[0])):
                if rellenados == cantidad:
                    break
                
                elif self.cuadrados[x][y].color == 'black':
                    self.master.itemconfigure(self.cuadrados[x][y].cuadro,fill = color,outline = 'white')
                    self.cuadrados[x][y].nombre = nombre
                    self.cuadrados[x][y].color = color
                    rellenados += 1
            if rellenados == cantidad:
                break

    def eliminar(self,nombre):
        """Metodo que elimina un archivo de la memoria

           Entradas:
                     nombre: nombre del archivo a eliminar
           Salidas:
                     Se cambia el color de los cuadros donde estaba ese archivo
        """
        
        eliminados = 0
        for x in range(len(self.cuadrados)):
            for y in range(len(self.cuadrados[0])):
                if self.cuadrados[x][y].nombre == nombre:
                    self.master.itemconfigure(self.cuadrados[x][y].cuadro,fill = 'black',outline = 'white')
                    self.cuadrados[x][y].nombre = ''
                    self.cuadrados[x][y].color = 'black'

class cuadrado:
    """Clase que crea los cuadrados necesarios para simular la memoria

       Entradas:
                 canvas: canvas en donde se va a dibujar
                 posx1: primer punto el eje x donde se va a crear el cuadrado
                 posx2: segundo punto el eje x donde se va a crear el cuadrado
                 posy1: primer punto el eje y donde se va a crear el cuadrado
                 posy2: segundo punto el eje y donde se va a crear el cuadrado
                 nombre: identificador
                 color: color del fonde del cuadrado
       Salidas:
                 Un cuadrado con las dimensiones escogidas
    """
    
    def __init__(self,canvas,posx1,posx2,posy1,posy2,nombre = '',color = 'black'):
        self.canvas = canvas
        
        self.nombre = nombre # Para identificar en caso de que se quiera cambiar el color
        
        self.color = color # Determina el fondo del cuadrado
        
        self.posx1 = posx1 ##
        self.posy1 = posy1  # Posiciones para dibujar el cuadrado
        self.posx2 = posx2  #
        self.posy2 = posy2 ##

        self.cuadro = canvas.create_rectangle(posx1,posy1,posx2,posy2,fill = self.color, outline = 'white') # Se crea el cuadrado

class Disponibles:
    """Crea la memoria del programa
    """

    def __init__(self, cantBloque=3174, listBloque=[]):
        """Crea una instancia de la clase Disponibles la cual toma como parametros

           Entradas:
                     cantBloque: cantidad de bloques en la memoria
                     listBloques: lista de lis bloques que se pueden utilizar

           Salida:
                     Si se crea un archivo retorna la lista de los bloques asignados
        """

        self.cantBloque = cantBloque
        self.listBloque = listBloque

        for x in range(self.cantBloque):
            self.listBloque.append(x)

    def asignarEspacio(self, numBloque):
        """Asignas los espacios a ocupar

           Entrada:
                    numBloques: cantidad de bloques a utilizar

           Salida:
                    Lista con los bloques a dar
        """

        lista = self.listBloque[0:numBloque]
        del self.listBloque[0:numBloque]
        return lista
            
    def devolver(self, agreBloques):
        """Devuelve espacio a la memoria

           Entrada:
                    agreBloques: lista de los bloques a devolver
        """
        for a in agreBloques:
            self.listBloque.append(a)
        self.listBloque.sort()
            
class Archivo:
    """Crea un archivo
    """
    
    def __init__(self, nombre="", tam=0, bloques=[], color="", padre="", memoria="", listSubDir=[], direccion='', iid=''):
        """Crea una instancia de la clase Archivo la cual toma como parametros

           Entradas:
                     nombre: nombre del archivo
                     tam: tamaño del archivo
                     bloques: bloques utilizados
                     color: color del archivo
                     padre: padre del archivo
                     memoria: memoria del sistema
                     listSubDir: lista de subdirectorios
                     direccion: dirección del archivo
                     iid: identificador del archivo

           Salida:
                     Archivo creado
        """
        
        self.nombre = nombre
        self.tam = tam
        self.bloques = bloques
        self.color = color
        self.padre = padre
        self.memoria = memoria
        self.listSubDir = listSubDir
        self.direccion = direccion
        self.iid = iid
        
        self.lista = [] # Lista con los bloques del archivo
        
        for x in self.memoria.asignarEspacio(self.tam):
            self.lista.append(x)
    
    def aumentarEspacio(self, tamaño):
        """Aumenta el espacio de un archivo

           Entrada:
                    tamaño: cantidad de bloques a aumentar
        """
        
        lista = self.memoria.asignarEspacio(tamaño)
        
        for x in lista:
            self.lista.append(x)
        self.tam += tamaño
        self.lista.sort()

    def obtenerBloques(self):
        """ Obtiene la información de los bloques que utiliza de la forma --> 1-4,15-20,24

            Salida:
                    Retorna el mensaje y la lista de bloques del archivo
        """
        
        acum = 0
        msj = ""
        bandera = True
        for x in self.lista:
            if bandera == True: # Entra el primero de cada bloque
                msj += "%d" % x
                bandera = False
                acum += 1
                if len(self.lista) > acum + 1: 
                    if self.lista[acum] != x + 1:
                        msj += ","
                        bandera = True
                    
            elif len(self.lista) > acum + 1:
                if self.lista[acum + 1] == x + 1:
                    acum += 1
                    
                elif self.lista[acum + 1] != x + 1:
                    msj += "-%d," % x
                    bandera = True
                    acum += 1
                    
            elif len(self.lista) == acum + 1:  # El ultimo del bloque
                msj += "-%d" % x

        return msj, self.lista

    def eliminaArchivo(self):
        """Elimina un archivo y devuelve los bloques a la memoria
        """
        
        self.memoria.devolver(self.obtenerBloques()[1])

class Directorio:
    """Crea un directorio
    """
    
    def __init__(self, nombre="", canArchivo=0, listArchivo=[], padre="", canSubDir=0, listSubDir=[], direccion='', iid='', lista=[], archivos=[]):
        """Crea una instancia de la clase Directorio la cual toma como parametros

           Entradas:
                     nombre: nombre del directorio
                     canArchivo: cantidad de archivos en el directorio
                     listArchivo: nombre de los archivo en el directorio
                     padre: padre del directorio
                     canSubDir: cantidad de subdirectorios en el directorio
                     listSubDir: nombre de los subdirectorios en el directorio
                     direccion: dirección del directorio
                     iid: identificador del directorio
                     lista: objetos de directorios
                     archivos: objetos de archivos

           Salida:
                     Directorio creado
        """

        self.nombre = nombre
        self.canArchivo = canArchivo
        self.listArchivo = listArchivo # Nombre de los archivos
        self.padre = padre
        self.canSubDir = canSubDir
        self.listSubDir = listSubDir # Nombre de los directorios
        self.lista = lista # Objetos de directorios
        self.direccion = direccion
        self.archivos = archivos # Objetos de archivos
        self.iid = iid
        
    def agregaSubDir(self, directorio):
        """Agrega un directorio a este directorio

           Entrada:
                    directorio: objeto del directorio a agregar
        """
        
        self.lista.append(directorio)
        self.listSubDir.append(directorio.nombre)
        self.canSubDir += 1

    def borrarSubDir(self, directorio):
        """Borra un directorio de este directorio

           Entrada:
                    directorio: objeto del directorio a borrar
        """

        m = 0
        for a in self.lista:
            if a.nombre == directorio.nombre:
                self.lista.pop(m)
                break
            m += 1

        self.listSubDir.remove(directorio.nombre)
        
    def agregaArchivo(self, archivo):
        """Agrega un archivo a este directorio

           Entrada:
                    archivo: objeto del archivo a agregar
        """

        self.archivos.append(archivo)
        self.listArchivo.append(archivo.nombre)
        self.canArchivo += 1

    def borrarArchivo(self, archivo):
        """Borra un archivo de este directorio

           Entrada:
                    archivo: objeto del archivo a borrar
        """

        m = 0
        archivo.eliminaArchivo()
        for a in self.archivos:
            if a.nombre == archivo.nombre:
                self.archivos.pop(m)
                break
            else:
                m += 1
        if archivo.nombre in self.listArchivo:
            self.listArchivo.remove(archivo.nombre)
        self.canArchivo -= 1

class Espera(Frame):
    """Crea la ventana de espera
    """
    def __init__(self):
        """Crea una instancia de la clase Espera
        """    
        self.ventana = Tk() # Crea una ventana
        Frame.__init__(self, self.ventana)
        
        self.ventana.resizable(0,0)

        self.fondo = PhotoImage(file="Fondo.gif") # Crea una imagen de fondo
        self.lblFondo = Label(self.ventana, image=self.fondo, background='white')

        self.logo = PhotoImage(file="logo.gif") # Crea una imagen de logo
        self.lblLogo = Label(self.ventana, image=self.logo, background='white')
        
        self.progress = ttk.Progressbar(self.ventana, orient="horizontal", length=700, mode="determinate") # Crea una Progressbar
        
        self.lblLogo.place(x=0, y=20)
        self.lblFondo.grid(row=0, column=0)

        self.bytes = 0
        self.maxbytes = 0

        self.progress.place(x=335, y=700)
        
        self.progress["value"] = 0
        self.maxbytes = 1000
        self.progress["maximum"] = 1000
        self.leer_bytes()

    def leer_bytes(self):
        """Lee los bytes para la Progressbar
        """
        self.bytes += 25
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            self.ventana.after(100, self.leer_bytes)
        else:
            self.ventana.destroy()
            inicio()
                
def inicio():
    """Desarrollo de la interfaz del programa
    """
    
    memoria = Disponibles() # Creación de la memoria     
    root = Tk() # Creación de la Ventana principal
    app = Pantalla(root, memoria, '\\') # Clase principal de sistema
    app.mainloop() # Espera a que se cierre la panatalla

Espera()
