# Integrantes
Zarko Kuljis, 2018235233-7
# Descripción
Este programa cumple como gestor de una base de datos específica desarrollada para el llamado *SANSANITO POKÉMON*.

El usuario deberá ejecutar comandos vía terminal con el programa en ejecución para realizar operaciones sobre la base de datos.
# Consideraciones
Este programa se realizó en la versión 3.7.7 de Python.

Un Pokémon legendario, en caso de no haber suficiente espacio, sólo podrá reemplazar a otro Pokémon legendario. Esto **no se cumple para los Pokémon no-legendarios** (Desde ahora llamados *corrientes*); un Pokémon corriente puede reemplazar, tanto a otros Pokémon corrientes como a legendarios.

Asumo que el valor *HP Max* de SANSANITO POKÉMON corresponde al valor *HP Total* presente en POYO.

A la hora de realizar consultas sobre la tabla (Si no se ha especificado el formato de estas en la Tarea) se mostrarán sólamente los datos exclusivos de la tabla SANSANITO POKÉMON (A excepción de ID) y el hp máximo, puesto que considero redundante mostrar los datos presentes en POYO pues son invariables aunque se den instancias diferentes del mismo Pokémon.
Por otra parte, la ID no es mostrada puesto que el usuario no tiene ningún control sobre ella y no es necesaria para realizar ninguna operación.
Me adhiero a la libertad de formato planteada en el foro de preguntas de la tarea: https://aula.usm.cl/mod/forum/discuss.php?d=503864

Siguiendo el hilo anterior, a la hora de desplegar datos no habrá distinción entre Pokémon si estos fueron ingresados con el mismo hp actual, mismo estado y al mismo tiempo. Que esto llegase a pasar se considerará **mal uso del programa** puesto que esta situación es bastante límite e imposible mediante el uso normal (y lógico) del programa.

Al finalizar el programa todos los datos que se hayan generado se borrarán, por ende el programa no tiene memoria y acciones realizadas en sesiones anteriores no se verán reflejadas.

A la hora de llenar el SANSANITO POKÉMON con registros aleatorios (Al inicio de la ejecución del programa) cabe la posibilidad de que la fecha de ingreso de algunos Pokémon sea mayor a la fecha actual del dispositivo.
# Información relevante
Este programa se reserva las palabras *NONE* y *NULL*:
* NULL: Refiere a dejar el campo nulo, sin ningún valor.
* NONE: Esta palabra cumplirá dos funciones dependiendo de comando ejecutado:
    1. En comandos de **creación**: Establecerá un valor aleatorio o conveniente.
    2. En comandos de **actualización**: Conservará el valor anterior (En la tabla) del parámetro al que refiera.
Que un comando en esta misma documentación incorpore, por ejemplo, */NULL* significa que ese valor es válido para ese parámetro. Si no contiene esta sentencia entonces no lo será.

Además, si se desean ingresar **parámetros que contengan espacios deben ser introducidos entre comillas dobles (")**, de lo contrario se interpretará como más de un valor.

Ej:

`CREATE "Mr. Mime" 10 Quemado` :heavy_check_mark:

Insertará un 'Mr. Mime' con 10 de hp 'Quemado'.

`CREATE Mr. Mime 10 Quemado` :x:

Intentará insertar un 'Mr.' con 'Mime' de hp y con estado 10, además de un valor overflow 'Quemado'. Esto, por supuesto, dará error.
# Comandos
Es importante resaltar que todos estos comandos se aplican sobre el SANSANITO POKÉMON.
## CREATE
Agrega un Pokémon.

`CREATE <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE`

## READ
Lee toda la información de un Pokémon.

`READ <POKÉMON>`

## UPDATE
Actualiza la información de un Pokémon.

`UPDATE <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE <FECHA DE INGRESO>/NULL/NONE`

## DELETE
Borra la información de un Pokémon.

`DELETE <POKÉMON>`

## INSERT
Agrega un Pokémon.

`INSERT <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE`

## TOP 10
Muestra los 10 Pokémon con más prioridad.

`TOP10`

## BOTTOM 10
Muestra los 10 Pokémon con menos prioridad.

`BOTTOM10`

## CONDITION
Muestra todos los Pokémon con determinado estado.

`CONDITION <ESTADO>/NULL/NONE`

## LEGENDARIES
Muestra todos los Pokémon legendarios.

`LEGENDARIES`

## OLDEST ONE
Muestra el Pokémon más viejo.

`OLDESTONE`

## MOST REPEATED
Muestra el nombre más repetido.

`MOSTREPEATED`

## SHOW ALL
Muestra toda la tabla.

`SHOWALL`

## EXIT
Finaliza el programa.

`EXIT`