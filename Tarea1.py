from random import random, randint, choice
from datetime import datetime, timedelta

from os import path
import csv
import json

# shlex.split es una función prácticamente idéntica a str.split(' '), pero respetando las oraciones entre
# comillas (") como una sóla palabra. 
# Ej: shlex.split('¿Cómo "estás hoy" amigo?') == ['¿Cómo','estás hoy', 'amigo?']
from shlex import split as xsplit
# tabulate.tabulate() es una función que permite desplegar listas de listas en forma de tabla, nada más
# que un recurso gráfico.
from tabulate import tabulate as mostrarTabla

import pyodbc

ESTADOS = [None, 'Envenenado', 'Paralizado', 'Quemado', 'Dormido', 'Congelado']

# La clase 'Consola' cumple la función de puente entre el Usuario y el Data Base Manager.
class Consola:
    # Descripción:  Esta función se encarga de Inicializar mi objeto 'Consola', estableciendo así conexión
    #               con la DB, con la terminal y creando tanto la tabla POYO como SANSANITO POKEMON.
    # Recibe:       No recibe parámetros.
    # Retorns:      No retorna.
    def __init__(self, *argumentos):
        self.dbmngr = DataBaseManager()
        self.dbmngr.CrearTablaPoyo()
        self.dbmngr.CrearTablaSansanito()
        self.dbmngr.Commit(False)
        
        # Aquí creo un diccionario comando-función que permitirá la interacción del programa vía consola.
        self.COMANDOS = {
            'CREATE':       self.Crear,
            'READ':         self.Leer,
            'UPDATE':       self.Actualizar,
            'DELETE':       self.Borrar,
            
            'INSERT':       self.Ingresar,
            'TOP10':        self.Top10,
            'BOTTOM10':     self.Bottom10,
            'CONDITION':    self.ListaPorEstado,
            'LEGENDARIES':  self.ListaLegendarios,
            'OLDESTONE':    self.MasViejo,
            'MOSTREPEATED': self.MasRepetido,
            'SHOWALL':      self.Mostrar,

            'EXIT':         self.Salir
        }
        self.Lector()

    # Descripción:  El Lector cumple la función de permanentemente pedir comandos vía terminal. 
    # Recibe:       No recibe parámetros.
    # Retorns:      No retorna.
    def Lector(self):
        while True:
            mensaje = input('[COMMAND] ')
            self.Interprete(mensaje)

    # Descripción:  El Intérprete se encarga de 'entender' lo que se ha escrito en consola y darle los
    #               correspondientes comandos a las funciones.
    # Recibe:       El mensaje a interpretar.
    # Retorns:      No retorna.
    def Interprete(self, mensaje):
        mensaje = xsplit(mensaje)
        
        # Si no hay mensaje no hay nada que interpretar, así que damos por concluida la acción.
        if (len(mensaje) == 0):
            return
        
        comando = mensaje[0]
        argumentos = mensaje[1:]

        self.COMANDOS.setdefault(comando, self.UnkCmd)(*argumentos)
    
    # Descripción:  Esta función se encarga de encontrar todas las instancias de un determinado Pokémon en
    #               el SANSANITO POKÉMON y da la posibilidad al usuario de elegir con cuál de ellas quiere
    #               trabajar (Si es que hay más de una).
    # Recibe:       El nombre del Pokémon cuya instancia se desea encontrar.
    # Retorns:      No retorna.
    def SeleccionarPokemon(self, nombrePkmn):
        pokemon = self.dbmngr.InfoPokemonPoyo(nombrePkmn)
        if pokemon == None:
            print('[ERROR  ] El Pokémon solicitado no existe en la tabla POYO.')
            return
        
        candidatos = []
        for info in self.dbmngr.MostrarSansanito(ordenarPrioridad=False):
            if info[2] == nombrePkmn:
                candidatos.append(info)
        if len(candidatos) == 0:
            print('[ERROR  ] No existe ningún {} en el SANSANITO POKEMON'.format(nombrePkmn))
            return
        
        if len(candidatos) > 1:
            ids = []
            for candidato in sorted(candidatos, key=lambda x: x[0]):
                idPkmn = candidato[0]
                ids.append(str(idPkmn))

                if candidato[8] == None:
                    mensaje ='[CONSOLE] Id: {0}, {1} {2}/{3} ({5} de prioridad), ingresado el día {6}.'
                else:
                    mensaje ='[CONSOLE] Id: {0}, {1} {2}/{3} {4} ({5} de prioridad), ingresado el día {6}.'
                print(mensaje.format(idPkmn, nombrePkmn, candidato[5], candidato[6], candidato[8], candidato[10], candidato[9].strftime('%d-%m-%Y a las %H:%M')))
            
            seleccionado = input('[CONSOLE] Seleccione el Id del Pokémon que desea seleccionar: ').strip()
            if seleccionado not in ids:
                print('[ERROR  ] Id no válido.')
                return None
            else:
                for candidato in candidatos:
                    if str(candidato[0]) == seleccionado:
                        seleccionado = candidato
                        break
                if type(seleccionado) == str:
                    print('[ERROR  ] Inesperadamente el programa a sido incapaz de identificar al Pokémon. Cerrando...')
                    self.Salir()
        else:
            seleccionado = candidatos[0]
        
        return seleccionado

    # Descripción:  Esta función se encarga de interpretar el valor de Hp Actual ingresado vía terminal y
    #               corroborar su validez.
    # Recibe:       El valor de hp actual.
    #               El hp máximo (Total) posible.
    #               (Opcional) El valor default de hp a retornar (Si hpActual es 'NONE').
    # Retorns:      Un valor entre 0 y el valor hpTotal si el hpActual ingresado es válido o -1 si es inválido.
    def HpActual(self, hpActual, hpTotal, valorDefault=None):
        if valorDefault == None:
            valorDefault = randint(0, hpTotal)
        
        if hpActual == 'NONE':
            hpActual = valorDefault
        elif hpActual in map(str, range(hpTotal+1)):
            hpActual = int(hpActual)
        else:
            return -1
        
        return hpActual

    # Descripción:  Esta función se encarga de interpretar el valor de Estado ingresado vía terminal y
    #               corroborar su validez.
    # Recibe:       El estado a buscar.
    #               (Opcional) El valor default de estado a retornar (Si estado es 'NONE').
    # Retorns:      EL propio estado ingresado (o el valor default) si este es válido o -1 si es inválido.
    def Estado(self, estado, valorDefault=None):
        if valorDefault == None:
            valorDefault = choice(ESTADOS)
        
        if estado == 'NONE':
            estado = valorDefault
        elif estado == 'NULL':
            estado = None
        elif estado not in ESTADOS:
            return -1
        
        return estado

    # Descripción:  Esta función se llama si se ha ingresado un comando no válido.
    # Recibe:       No recibe parámetros.
    # Retorns:      No retorna.
    def UnkCmd(self, *argumentos):
        print("[ERROR  ] El comando ingresado no existe.")

    # Descripción:  Esta función corresponde a la operación 'CREATE' del CRUD. Redirije a la función Consola.Ingresar.
    # Recibe:       El nombre del Pokémon que se desea insertar en el SANSANITO POKÉMON.
    #               El Hp actual del Pokémon.
    #               El Estado del Pokémon.
    # Retorns:      True si se ejecutó correctamente, False si no.
    def Crear(self, *argumentos):
        if len(argumentos) != 3:
            print('[ERROR  ] CREATE recibe el nombre del Pokémon a ingresar, su Hp actual y estado.\n[EXAMPLE] CREATE <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE')
            return False
        nombrePkmn, hpActual, estado = argumentos[0:3]
        return self.Ingresar(nombrePkmn, hpActual, estado)

    # Descripción:  Esta función corresponde a la operación 'READ' del CRUD. Lee la información de un Pokémon
    #               en el SANSANITO POKÉMON.
    # Recibe:       El nombre del Pokémon cuya información se desea leer de la tabla.
    # Retorns:      True si se ejecutó correctamente, False si no.
    def Leer(self, *argumentos):
        if len(argumentos) != 1:
            print('[ERROR  ] READ recibe el nombre del Pokémon perteneciente al SANSANITO POKEMON cuya información se desea conocer.\n[EXAMPLE] READ <POKÉMON>')
            return
        nombrePkmn = argumentos[0]
        pokemon = self.SeleccionarPokemon(nombrePkmn)
        if pokemon == None:
            return False
        print(mostrarTabla([pokemon], headers=['Id', 'Pokedex', 'Nombre', 'Tipo 1', 'Tipo 2', 'HP Act', 'HP Max', 'Legendario', 'Estado', 'Fecha de Ingreso', 'Prioridad']))

        return True

    # Descripción:  Esta función corresponde a la operación 'UPDATE' del CRUD. Actualiza la información de
    #               un Pokémon en el SANSANITO POKÉMON.
    # Recibe:       El nombre del Pokémon que se desea actualizar.
    #               El Hp actual que se desea asignar al Pokémon.
    #               El Estado que se desea asignar al Pokémon.
    #               La Fecha de ingreso que se desea asignar al Pokémon.
    # Retorns:      True si se ejecutó correctamente, False si no.
    def Actualizar(self, *argumentos):
        if len(argumentos) != 4:
            print('[ERROR  ] UPDATE recibe el nombre del Pokémon a actualizar, el hp actual, estado y fecha de ingreso que se desea establecer.\n[EXAMPLE] UPDATE <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE <FECHA DE INGRESO>/NULL/NONE')
            return False
        nombrePkmn = argumentos[0]
        pokemon = self.SeleccionarPokemon(nombrePkmn)
        if pokemon == None:
            return False
        hpTotal = int(pokemon[6])
        
        hpActual, estado, ingreso = argumentos[1:]
        aHpActual, aEstado, aIngreso = int(pokemon[5]), pokemon[8], pokemon[9]
        
        hpActual = self.HpActual(hpActual, hpTotal, aHpActual)
        if hpActual == -1:
            print('[ERROR  ] El Hp actual ingresado no es válido. El hp máximo de {} es de {}.'.format(nombrePkmn, hpTotal))
            return False
        
        estado = self.Estado(estado, valorDefault=aEstado)
        if estado == -1:
            print('[ERROR  ] El estado ingresado no es válido. Elija entre {} o NULL'.format(', '.join(ESTADOS[1:])))
            return False
        
        if ingreso == 'NONE':
            ingreso = aIngreso
        elif ingreso == 'NULL':
            ingreso = None
        else:
            try:
                ingreso = datetime.datetime.strptime(ingreso, '%d/%m/%Y;%H:%M:%S')
            except:
                print('[ERROR  ] El formato de fecha o la fecha ingresada no es válida.')
                return False

        self.dbmngr.ActualizarEnSansanito(pokemon[0], hpActual, estado, ingreso)
        self.dbmngr.Commit()
        return True

    # Descripción:  Esta función corresponde a la operación 'DELETE' del CRUD. Borra la información de
    #               un Pokémon en el SANSANITO POKÉMON.
    # Recibe:       El nombre del Pokémon que se desea borrar.
    # Retorns:      True si se ejecutó correctamente, False si no.
    def Borrar(self, *argumentos):
        if len(argumentos) == 0:
            print('[ERROR  ] DELETE recibe el nombre del Pokémon a dar de alta en el SANSANITO POKEMON.\n[EXAMPLE] DELETE <POKÉMON>')
            return False
        nombrePkmn = argumentos[0]
        pokemon = self.SeleccionarPokemon(nombrePkmn)
        if pokemon == None:
            return False
        idPkmn, nombre, hpActual, hpTotal, estado = int(pokemon[0]), pokemon[2], *pokemon[5:7], pokemon[8]
        
        self.dbmngr.BorrarEnSansanito(idPkmn, nombre, hpActual, hpTotal, estado)
        self.dbmngr.Commit()
        return True

    # Descripción:  Esta función se encarga de ingresar un Pokémon en el SANSANITO POKÉMON.
    # Recibe:       El nombre del Pokémon que se desea ingresar en el SANSANITO POKÉMON.
    #               El Hp actual del Pokémon.
    #               El Estado del Pokémon.
    # Retorns:      True si se ejecutó correctamente, False si no.
    def Ingresar(self, *argumentos):
        if len(argumentos) != 3:
            print('[ERROR  ] INSERT recibe el nombre del Pokémon a ingresar, su Hp actual y estado.\n[EXAMPLE] INSERT <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE')
            return False
        nombrePkmn = argumentos[0]
        
        cantidadNoLegendarios = self.dbmngr.CantidadPokemonSansanito(legendario=False)
        cantidadLegendarios = self.dbmngr.CantidadPokemonSansanito(legendario=True)
        espacioRestante = int(50 - cantidadNoLegendarios - (5*cantidadLegendarios))

        pokemon = self.dbmngr.InfoPokemonPoyo(nombrePkmn)
        if pokemon == None:
            print('[ERROR  ] El Pokémon solicitado no existe en la tabla POYO.')
            return False
        
        pokedex, nombrePkmn, tipo1, tipo2, hpTotal, esLegendario = pokemon
        pokedex = int(pokedex)
        hpTotal = int(hpTotal)
        esLegendario = bool(esLegendario)
        if esLegendario:
            coste = 5
        else:
            coste = 1
        
        if esLegendario and espacioRestante - coste < 0 and cantidadLegendarios == 0:
            print('[ERROR  ] No hay cupo para Pokémon legendarios en la tabla SANSANITO POKEMON.')
            return False
        
        hpActual = self.HpActual(argumentos[1], hpTotal)
        if hpActual == -1:
            print('[ERROR  ] El Hp actual ingresado no es válido. El hp máximo de {} es de {}.'.format(nombrePkmn, hpTotal))
            return False
        
        estado = self.Estado(argumentos[2])
        if estado == -1:
            print('[ERROR  ] El estado ingresado no es válido. Elija entre {} o NULL'.format(', '.join(ESTADOS[1:])))
            return False
            
        print('[INFO   ] El SANSANITO POKEMON está al {}/50 de su capacidad.'.format(50-espacioRestante))

        if esLegendario:
            for legendario in self.dbmngr.LegendariosEnSansanito():
                if legendario[1] == nombrePkmn:
                    prioridad = hpTotal - hpActual
                    if estado != None:
                        prioridad += 10
                    if prioridad > legendario[-1]:
                        self.dbmngr.BorrarEnSansanito(*legendario[:5])
                        self.dbmngr.EscribirEnSansanito(pokedex, nombrePkmn, tipo1, tipo2, hpActual, hpTotal, esLegendario, estado, datetime.now())
                        self.dbmngr.Commit()
                        return True
                    else:
                        print('[ERROR  ] Ya hay Pokémon legendario del mismo nombre con igual o más prioridad en el SANSANITO POKEMON.')
                        return False
        
        if espacioRestante - coste < 0:
            menorPrioridad = self.dbmngr.MenorPrioridadSansanito(legendario=esLegendario)
            prioridad = hpTotal - hpActual
            if estado != None:
                prioridad += 10

            if prioridad > menorPrioridad[-1]:
                self.dbmngr.BorrarEnSansanito(*menorPrioridad[:5])
            else:
                print('[ERROR  ] El Pokémon solicitado no tiene la suficiente prioridad para entrar al SANSANITO POKEMON.')
                return False
        
        self.dbmngr.EscribirEnSansanito(pokedex, nombrePkmn, tipo1, tipo2, hpActual, hpTotal, esLegendario, estado, datetime.now())
        self.dbmngr.Commit()
        return True

    # Descripción:  Muestra vía terminal los 10 Pokémon con mayor prioridad.
    # Recibe:       No recibe parámetros.
    # Retorna:      Las 10 filas con mayor valor prioridad.
    def Top10(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] TOP10 no recibe ningún parámetro.\n[EXAMPLE] TOP10')
            return
        top10 = list(map(lambda info: info[1:], self.dbmngr.Top10PrioridadSansanito()))
        if len(top10) > 0:
            print(mostrarTabla(top10, headers=['Nombre', 'HP Act', 'HP Max', 'Estado', 'Ingreso', 'Prioridad']))
        else:
            print('[INFO   ] El SANSANITO POKEMON está vacío.')
        
        return top10

    # Descripción:  Muestra vía terminal los 10 Pokémon con menor prioridad.
    # Recibe:       No recibe parámetros.
    # Retorna:      Las 10 filas con menor valor PRIORIDAD.
    def Bottom10(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] BOTTOM10 no recibe ningún parámetro.\n[EXAMPLE] BOTTOM10')
            return
        bottom10 = list(map(lambda info: info[1:], self.dbmngr.Bottom10PrioridadSansanito()))
        if len(bottom10) > 0:
            print(mostrarTabla(bottom10, headers=['Nombre', 'HP Act', 'HP Max', 'Estado', 'Ingreso', 'Prioridad']))
        else:
            print('[INFO   ] El SANSANITO POKEMON está vacío.')
        
        return bottom10
    
    #NONE para aleatorio
    # Descripción:  Muestra vía terminal todos los Pokémon con determinado estado.
    # Recibe:       El estado por el cual filtrar el SANSANITO POKÉMON.
    # Retorna:      Todas las filas con determinado valor ESTADO.
    def ListaPorEstado(self, *argumentos):
        if len(argumentos) != 1:
            print('[ERROR  ] CONDITION recibe sólo el estado a filtrar.\n[EXAMPLE] CONDITION <ESTADO>/NULL/NONE')
            return
        
        estado = self.Estado(argumentos[0])
        if estado == -1:
            print('[ERROR  ] El estado ingresado no es válido. Elija entre {} o NULL'.format(', '.join(ESTADOS[1:])))
            return
        
        pokemon = list(map(lambda info: (info[2], info[5], info[6], info[8], info[9], info[10]), self.dbmngr.PokemonConEstadoSansanito(estado)))
        if len(pokemon) > 0:
            print(mostrarTabla(pokemon, headers=['Nombre', 'HP Act', 'HP Max', 'Estado', 'Ingreso', 'Prioridad']))
        elif estado == None:
            print('[INFO   ] No hay Pokémon sin estado en el SANSANITO POKEMON.')
        else:
            print('[INFO   ] No hay Pokémon {}s en el SANSANITO POKEMON.'.format(estado))
        
        return pokemon

    # Descripción:  Muestra vía terminal todos los Pokémon legendarios.
    # Recibe:       No recibe parámetros.
    # Retorna:      Todas las filas con valor LEGENDARIO = 1.
    def ListaLegendarios(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] LEGENDARIES no recibe ningún parámetro.\n[EXAMPLE] LEGENDARIES')
            return

        legendarios = list(map(lambda info: info[1:6], self.dbmngr.LegendariosEnSansanito()))
        if len(legendarios) > 0:
            print(mostrarTabla(legendarios, headers=['Nombre', 'HP Act', 'HP Max', 'Estado', 'Ingreso', 'Prioridad']))
        else:
            print('[INFO   ] No hay Pokémon legendarios en el SANSANITO POKEMON.')
        
        return legendarios

    # Descripción:  Muestra vía terminal el Pokémon que lleva más tiempo ingresado.
    # Recibe:       No recibe parámetros.
    # Retorna:      La fila con menor valor INGRESO.
    def MasViejo(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] OLDESTONE no recibe ningún parámetro.\n[EXAMPLE] OLDESTONE')
            return
        masViejo = self.dbmngr.MasViejoSansanito()
        if masViejo == None:
            print('[INFO   ] El SANSANITO POKEMON está vacío.')
        else:
            if masViejo[8] == None:
                mensaje = '[INFO   ] El Pokémon que lleva más tiempo ingresado en el SANSANITO POKEMON es un {0} {1}/{2} ({4} de prioridad), ingresado el día {5}.'
            else:
                mensaje = '[INFO   ] El Pokémon que lleva más tiempo ingresado en el SANSANITO POKEMON es un {0} {1}/{2} {3} ({4} de prioridad), ingresado el día {5}.'
            print(mensaje.format(masViejo[2], masViejo[5], masViejo[6], masViejo[8], masViejo[10], masViejo[9].strftime('%d-%m-%Y a las %H:%M')))

        return masViejo

    # Descripción:  Muestra vía terminal el nombre del Pokémon con más instancias en el SANSANITO POKÉMON.
    # Recibe:       No recibe parámetros.
    # Retorna:      El nombre del Pokémon con más instancias en el SANSANITO POKÉMON.
    def MasRepetido(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] MOSTREPEATED no recibe ningún parámetro.\n[EXAMPLE] MOSTREPEATED')
            return
        masRepetido = self.dbmngr.PokemonMasRepetidoSansanito()
        if masRepetido == None:
            print('[INFO   ] El SANSANITO POKEMON está vacío.')
        else:
            if masRepetido[1] > 1:
                mensaje = '[INFO   ] El Pokémon más repetido del SANSANITO POKEMON es {} con {} apariciones.'
            else:
                mensaje = '[INFO   ] El Pokémon más repetido del SANSANITO POKEMON es {} con 1 aparición.'
            print(mensaje.format(masRepetido[0], int(masRepetido[1])))
        
        return masRepetido

    # Descripción:  Muestra vía terminal todos los valores de Nombre, HP Actual, HP Maximo y Prioridad de SANSANITO POKÉMON.
    # Recibe:       No recibe parámetros.
    # Retorna:      True si se ejecutó correctamente, False si no.
    def Mostrar(self, *argumentos):
        if len(argumentos) != 0:
            print('[ERROR  ] SHOWALL no recibe ningún parámetro.\n[EXAMPLE] SHOWALL')
            return False
        pokemon = list(map(lambda info: (info[2], info[5], info[6], info[10]), self.dbmngr.MostrarSansanito(ordenarPrioridad=True)))
        if len(pokemon) > 0:
            print(mostrarTabla(pokemon, headers=['Nombre', 'HP Act', 'HP Max', 'Prioridad']))
        else:
            print('[INFO   ] El SANSANITO POKEMON está vacío.')
            return False
        
        return True

    # Descripción:  Finaliza el programa.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def Salir(self, *argumentos):
        self.dbmngr.BorrarTablaSansanito()
        self.dbmngr.BorrarTablaPoyo()
        self.dbmngr.Commit(False)
        exit()

# La clase 'File Manager' es la encargada de extraer los datos de los archivos y distribuirlos.
class FileManager:
    RAIZ = path.dirname(__file__)

    # Descripción:  Lee el archivo 'pokemon.csv' y retorna una lista con su contenido.
    # Recibe:       No recibe parámetros.
    # Retorna:      Una lista con el contenido de cada línea de 'pokemon.csv'.
    def ObtenerDatosPoyo(self):
        datos = []
        with open(path.join(self.RAIZ,'pokemon.csv'), encoding='utf-8') as archivo:
            next(archivo)
            lector = csv.reader(archivo)
            for linea in lector:
                datos.append(linea)
            archivo.close()
        
        return datos

    # Descripción:  Extrae las credenciales de acceso a ORACLE.
    # Recibe:       No recibe parámetros.
    # Retorna:      Las credenciales.
    def ObtenerCredenciales(self):
        with open(path.join(self.RAIZ, 'config.json'), encoding='utf-8') as archivo:
            config = json.load(archivo)
            archivo.close()
        
        credenciales = 'DRIVER={{{}}}; Uid={}; Pwd={}'.format(config['driver'], config['usuario'], config['contrasena'])
        return credenciales

# La clase 'Data Base Manager' se encarga de operar sobre la base de datos Oracle, modelando
# las operaciones que nos interesan y restringiendo así el manejo directo de la BD a otras clases.
class DataBaseManager:
    # Descripción:  Instancia una entidad FileManager y solicita una conexión a la base de datos.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def __init__(self, *argumentos):
        self.fileManager = FileManager()
        self.Conectar()

    # Descripción:  Establece una conexión con la base de datos.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def Conectar(self):
        credenciales = self.fileManager.ObtenerCredenciales()
        try:
            self.conexion = pyodbc.connect(credenciales)
        except:
            print('[ERROR  ] Credenciales inválidas. Finalizando...')
            exit()

    # Descripción:  Cierra la conexión con la base de datos.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def Desconectar(self):
        self.conexion.close()

    # Descripción:  Crea la tabla POYO y la rellena con 44 Pokémon aleatorios no legendarios.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def CrearTablaPoyo(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE POYO(
                POKEDEX    INTEGER      NOT NULL,
                NOMBRE     VARCHAR(255) PRIMARY KEY,
                TIPO1      VARCHAR(255) NOT NULL,
                TIPO2      VARCHAR(255),
                HPTOTAL    INTEGER      NOT NULL,
                LEGENDARIO NUMBER(1,0)  NOT NULL
            );
        ''')
        
        datos = self.fileManager.ObtenerDatosPoyo()
        for conjuntoDatos in datos:
            pokedex, nombre, tipo1, tipo2 = conjuntoDatos[:4]
            if tipo2 == '':
                tipo2 = None
            hpTotal = conjuntoDatos[5]
            if conjuntoDatos[12] == 'True':
                legendario = 1
            else:
                legendario = 0

            self.EscribirEnPoyo(pokedex, nombre, tipo1, tipo2, hpTotal, legendario)

        cursor.close()
        print('[DBMNGR ] Tabla POYO creada exitosamente.')

    # Descripción:  Borra la tabla POYO.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def BorrarTablaPoyo(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            DROP TABLE POYO;
        ''')
        
        cursor.close()
        print('[DBMNGR ] Tabla POYO eliminada exitosamente.')

    # Descripción:  Inserta una fila en POYO.
    # Recibe:       Numero de Pokédex.
    #               Nombre del Pokémon.
    #               Primer tipo.
    #               Segundo tipo.
    #               Hp máximo (Total).
    #               Un bool (0 ó 1) que indica si es un Pokémon legendario o no.
    # Retorna:      No retorna.
    def EscribirEnPoyo(self, *valores):
        cantValores = len(valores)
        if cantValores < 2:
            print('[ERROR  ] Se ha intentado insertar una fila con menos de 2 valores en la tabla POYO.')
            return
        
        if cantValores > 6:
            print('[ERROR  ] Se ha intentado insertar una fila con más de 6 valores en la tabla POYO.')
            return
        
        if valores[1] == None:
            print('[ERROR  ] Se ha intentado insertar una fila sin Nombre del Pokémon en la tabla POYO.')
            return
        
        if ([valores[0], valores[2]] + list(valores[4:6])).count(None) != 0:
            print('[ERROR  ] Se ha intentado insertar una fila sin uno o más valores esenciales en la tabla POYO.')
            return
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            INSERT
            INTO POYO
            VALUES(?, ?, ?, ?, ?, ?)
            ''', *valores)
        
        cursor.close()
    
    # Descripción:  Permite obtener todos los datos de un Pokémon que provee la tabla POYO.
    # Recibe:       El nombre del Pokémon cuya información se desea conocer.
    # Retorna:      La información de este Pokémon (Según la tabla POYO).
    def InfoPokemonPoyo(self, nombrePkmn):
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT *
            FROM POYO
            WHERE NOMBRE=?
            ''', nombrePkmn)
        info = cursor.fetchone()
        cursor.close()

        return info

    # Descripción:  Crea la tabla SANSANITO (Correspondiente al SANSANITO POKÉMON) en la base de datos,
    #               también crea un trigger para la tabla que actualiza la prioridad y 2 vistas para
    #               legendarios y los 10 Pokémon con menor prioridad respectivamente.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def CrearTablaSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            CREATE TABLE SANSANITO(
                ID         INTEGER      GENERATED BY DEFAULT ON NULL AS IDENTITY PRIMARY KEY,
                POKEDEX    INTEGER      NOT NULL,
                NOMBRE     VARCHAR(255) NOT NULL,
                TIPO1      VARCHAR(255) NOT NULL,
                TIPO2      VARCHAR(255),
                HPACTUAL   INTEGER      NOT NULL,
                HPTOTAL    INTEGER      NOT NULL,
                LEGENDARIO NUMBER(1,0)  NOT NULL,
                ESTADO     VARCHAR(255),
                INGRESO    DATE,
                PRIORIDAD  INTEGER
            );
        ''')
        cursor.execute('''
            CREATE TRIGGER ACTUALIZARPRIORIDAD
            BEFORE INSERT OR UPDATE ON SANSANITO
            FOR EACH ROW
            BEGIN
                :NEW.PRIORIDAD := :NEW.HPTOTAL - :NEW.HPACTUAL;
                IF :NEW.ESTADO IS NOT NULL THEN
                    :NEW.PRIORIDAD := 10 + :NEW.PRIORIDAD;
                END IF;
            END;
        ''')
        cursor.execute('''
            CREATE OR REPLACE VIEW BOTTOM10
            AS (
                SELECT ID, NOMBRE, HPACTUAL, HPTOTAL, ESTADO, INGRESO, PRIORIDAD
                FROM (
                    SELECT ID, NOMBRE, HPACTUAL, HPTOTAL, ESTADO, INGRESO, PRIORIDAD
                    FROM SANSANITO
                    ORDER BY PRIORIDAD
                )
                WHERE ROWNUM<=10
            );
        ''')
        cursor.execute('''
            CREATE OR REPLACE VIEW LEGENDARIOS
            AS (
                SELECT ID, NOMBRE, HPACTUAL, HPTOTAL, ESTADO, INGRESO, PRIORIDAD
                FROM SANSANITO
                WHERE LEGENDARIO=1
            );
        ''')

        # Fuente:       https://gist.github.com/rg3915/db907d7455a4949dbe69
        # Descripción:  Genera una fecha aleatoria.
        # Recibe:       El año mínimo de generación.
        #               El año máximo de generación.
        # Retorna:      Una fecha aleatoria entre ambas años provistos.
        def gen_datetime(min_year=2018, max_year=datetime.now().year):
            start = datetime(min_year, 1, 1, 00, 00, 00)
            years = max_year - min_year + 1
            end = start + timedelta(days=365 * years)
            return start + (end - start) * random()
        
        cursorAuxiliar = self.conexion.cursor()
        cursorAuxiliar.execute('''
            SELECT *
            FROM (
                SELECT *
                FROM POYO
                WHERE LEGENDARIO=0
                ORDER BY DBMS_RANDOM.RANDOM
            )
            WHERE ROWNUM<=44;
        ''')
        for fila in cursorAuxiliar:
            pokedex, nombre, tipo1, tipo2, hpTotal, legendario = fila
            hpActual = randint(0, hpTotal)
            estado = choice(ESTADOS)
            ingreso = gen_datetime()
            self.EscribirEnSansanito(pokedex, nombre, tipo1, tipo2, hpActual, hpTotal, legendario, estado, ingreso, False)
		
        cursorAuxiliar.close()
        cursor.close()
        print('[DBMNGR ] Tabla SANSANITO POKEMON creada exitosamente.')

    # Descripción:  Borra la tabla SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      No retorna.
    def BorrarTablaSansanito(self):
        cursor = self.conexion.cursor()
        
        cursor.execute('''
            DROP VIEW LEGENDARIOS;
        ''')
        cursor.execute('''
            DROP VIEW BOTTOM10;
        ''')
        cursor.execute('''
            DROP TRIGGER ACTUALIZARPRIORIDAD;
        ''')
        cursor.execute('''
            DROP TABLE SANSANITO;
        ''')
        
        cursor.close()
        print('[DBMNGR ] Tabla SANSANITO POKEMON eliminada exitosamente.')

    # Descripción:  Inserta una fila en SANSANITO.
    # Recibe:       Numero de Pokédex.
    #               Nombre del Pokémon.
    #               Primer tipo.
    #               Segundo tipo.
    #               Hp actual del Pokémon.
    #               Hp máximo (Total).
    #               Un bool (0 ó 1) que indica si es un Pokémon legendario o no.
    #               El estado del Pokémon.
    #               La fecha de ingreso.
    #               (Opcional) Un bool que indica si se debe mostrar un mensaje vía terminal al completar la operación o no.
    # Retorna:      No retorna.
    def EscribirEnSansanito(self, pokedex, nombre, tipo1, tipo2, hpActual, hpTotal, legendario, estado, ingreso, mensaje=True):
        if [pokedex, nombre, tipo1, hpActual, hpTotal, legendario].count(None) != 0:
            print('[ERROR  ] Se ha intentado insertar una fila sin uno o más valores esenciales en la tabla SANSANITO POKEMON.')
            return
        
        if hpActual > hpTotal:
            print('[ERROR  ] Se ha intentado insertar una fila con un Pokémon cuyo HP máximo es menor a su HP actual en la tabla SANSANITO POKEMON.')
            return
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            INSERT
            INTO SANSANITO
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', None, pokedex, nombre, tipo1, tipo2, hpActual, hpTotal, legendario, estado, ingreso, None)
        
        cursor.close()
        if mensaje:
            if estado == None:
                print('[DBMNGR ] Se insertó un {} {}/{} en la tabla SANSANITO.'.format(nombre, hpActual, hpTotal))
            else:
                print('[DBMNGR ] Se insertó un {} {}/{} {} en la tabla SANSANITO.'.format(nombre, hpActual, hpTotal, estado))
    
    # Descripción:  Borra un registro de la tabla SANSANITO.
    # Recibe:       Id del Pokémon.
    #               Nombre del Pokémon.
    #               Hp actual del Pokémon.
    #               Hp máximo.
    #               Estado.
    #               (Opcional) Un bool que indica si se debe mostrar un mensaje vía terminal al completar la operación o no.
    # Retorna:      No retorna.
    def BorrarEnSansanito(self, idPkmn, nombre, hpActual, hpTotal, estado, mensaje=True):
        if type(idPkmn) is not int or idPkmn < 1:
            print('[ERROR  ] Se ha intentado borrar una fila con una Id no válida en la tabla SANSANITO POKEMON.')
            return

        cursor = self.conexion.cursor()
        cursor.execute('''
            DELETE
            FROM SANSANITO
            WHERE ID=?
        ''', idPkmn)

        cursor.close()
        if mensaje and [nombre, hpActual, hpTotal].count(None) == 0:
            if estado == None:
                print('[DBMNGR ] Se removió un {} {}/{} de la tabla SANSANITO.'.format(nombre, hpActual, hpTotal))
            else:
                print('[DBMNGR ] Se removió un {} {}/{} {} de la tabla SANSANITO.'.format(nombre, hpActual, hpTotal, estado))

    # Descripción:  Actualiza una fila de la tabla SANSANITO.
    # Recibe:       El id del Pokémon a actualizar.
    #               El hp actual del Pokémon.
    #               El estado del Pokémon.
    #               La fecha de ingreso.
    # Retorna:      No retorna.
    def ActualizarEnSansanito(self, idPkmn, hpActual, estado, ingreso):
        if idPkmn == None:
            print('[ERROR  ] Se debe proporcionar una id válida para actualizar el Pokémon.')
            return
        if hpActual == None:
            print('[ERROR  ] El Hp actual de un Pokémon no puede ser nulo.')
            return
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            UPDATE SANSANITO
            SET HPACTUAL = ?, ESTADO = ?, INGRESO = ?
            WHERE ID=?
        ''', hpActual, estado, ingreso, idPkmn)
        cursor.close()
        
        print('[DBMNGR ] Pokémon actualizado correctamente.')
    
    # Descripción:  Obtiene la información del Pokémon con menor prioridad.
    # Recibe:       Un bool que determina si se busca la menor prioridad de Pokémon legendarios o corrientes.
    # Retorna:      Toda la información relevande del Pokémon con menor prioridad.
    def MenorPrioridadSansanito(self, legendario):
        if legendario:
            tabla = 'LEGENDARIOS'
        else:
            tabla = 'BOTTOM10'
        
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT ID, NOMBRE, HPACTUAL, HPTOTAL, ESTADO, INGRESO, PRIORIDAD
            FROM {0}
            WHERE PRIORIDAD=(
                SELECT MIN(PRIORIDAD)
                FROM {0}
            );
        '''.format(tabla))
        prioridad = cursor.fetchone()
        if prioridad != None:
            prioridad[0] = int(prioridad[0])
            prioridad[2] = int(prioridad[2])
            prioridad[3] = int(prioridad[3])
            prioridad[6] = int(prioridad[6])
        cursor.close()

        return prioridad
    
    # Descripción:  Obtiene la cantidad de Pokémon en la tabla SANSANITO.
    # Recibe:       Un bool que determina si la búsqueda se realizará entre Pokémon legendarios o corrientes.
    # Retorna:      La cantidad de Pokémon en SANSANITO.
    def CantidadPokemonSansanito(self, legendario):
        cursor = self.conexion.cursor()
        if legendario:
            cursor.execute('''
                SELECT COUNT(*)
                FROM LEGENDARIOS;
            ''')
        else:
            cursor.execute('''
                SELECT COUNT(*)
                FROM SANSANITO
                WHERE LEGENDARIO=0;
            ''')
        
        cantidad = cursor.fetchone()[0]
        cursor.close()

        return cantidad
    
    # Descripción:  Obtiene los 10 Pokémon con mayor prioridad en la tabla SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      Todos los datos de interés de las 10 filas con mayor valor PRIORIDAD.
    def Top10PrioridadSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
        SELECT * FROM (
            SELECT ID, NOMBRE, HPACTUAL, HPTOTAL, ESTADO, INGRESO, PRIORIDAD
            FROM SANSANITO
            ORDER BY PRIORIDAD DESC
        )
        WHERE ROWNUM<=10;
        ''')
        top10 = cursor.fetchall()
        cursor.close()

        return top10
    
    # Descripción:  Obtiene los 10 Pokémon con menor prioridad en la tabla SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      Todos los datos de interés de las 10 filas con menor valor PRIORIDAD.
    def Bottom10PrioridadSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT *
            FROM BOTTOM10;
        ''')
        bottom10 = cursor.fetchall()
        cursor.close()

        return bottom10
    
    # Descripción:  Obtiene todos los Pokémon legendarios de SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      Los datos de interés de todas las filas cuyo valor LEGENDARIO = 1.
    def LegendariosEnSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT *
            FROM LEGENDARIOS;
        ''')
        legendarios = cursor.fetchall()
        cursor.close()
        
        for legendario in legendarios:
            legendario[0] = int(legendario[0])
            legendario[2] = int(legendario[2])
            legendario[3] = int(legendario[3])
            legendario[6] = int(legendario[6])
        return legendarios
    
    # Descripción:  Obtiene el Pokémon que lleva más tiempo ingresado en SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      El registro con menor valor INGRESO.
    def MasViejoSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT *
            FROM SANSANITO
            WHERE INGRESO=(
                SELECT MIN(INGRESO)
                FROM SANSANITO
            );
        ''')
        masViejo = cursor.fetchone()
        cursor.close()

        return masViejo
    
    # Descripción:  Obtiene todos los Pokémon con determinado estado en SANSANITO.
    # Recibe:       El estado a buscar.
    # Retorna:      Todas los registros cuyo valor ESTADO = estado solicitado.
    def PokemonConEstadoSansanito(self, estado):
        if estado not in ESTADOS:
            print('[ERROR  ] Se ha intentado solicitar todos los Pokémon con un estado inexistente.')
        
        cursor = self.conexion.cursor()
        if estado == None:
            cursor.execute('''
                SELECT *
                FROM SANSANITO
                WHERE ESTADO IS NULL
            ''')
        else:
            cursor.execute('''
                SELECT *
                FROM SANSANITO
                WHERE ESTADO=?
            ''', estado)
        pokemon = cursor.fetchall()
        cursor.close()

        return pokemon
    
    # Descripción:  Obtiene el nombre más repetido en SANSANITO.
    # Recibe:       No recibe parámetros.
    # Retorna:      El nombre del Pokémon y cuantas instancias de él existen en SANSANITO.
    def PokemonMasRepetidoSansanito(self):
        cursor = self.conexion.cursor()
        cursor.execute('''
            SELECT *
            FROM (
                SELECT NOMBRE, COUNT(NOMBRE) AS REPETICIONES
                FROM SANSANITO
                GROUP BY NOMBRE
                ORDER BY REPETICIONES DESC
                )
                WHERE ROWNUM<=1;
        ''')
        masRepetido = cursor.fetchone()
        cursor.close()

        return masRepetido
    
    # Descripción:  Obtiene todos los registros de SANSANITO.
    # Recibe:       Un bool que deterima si ordenar los registros por prioridad o no.
    # Retorna:      Todos los registros de SANSANITO.
    def MostrarSansanito(self, ordenarPrioridad):
        cursor = self.conexion.cursor()
        if ordenarPrioridad:
            cursor.execute('''
                SELECT *
                FROM SANSANITO
                ORDER BY PRIORIDAD DESC;
            ''')
        else:
            cursor.execute('''
                SELECT *
                FROM SANSANITO
            ''')
        pokemon = cursor.fetchall()
        cursor.close()

        return pokemon

    # Descripción:  Ejecuta los cambios en la base de datos.
    # Recibe:       (Opcional) Un bool que indica si se debe mostrar un mensaje vía terminal al completar la operación o no.
    # Retorna:      No retorna.
    def Commit(self, mensaje=True):
        self.conexion.commit()
        if mensaje:
            print('[DBMNGR ] Los cambios en las tablas se han guardado exitosamente.')

# Descripción:  Ejecuta el programa.
# Recibe:       No recibe parámetros.
# Retorna:      No retorna.
def Main():
    Consola()

if __name__ == "__main__":
    Main()