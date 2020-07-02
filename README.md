# Integrantes
Zarko Kuljis, 2018235233-7
# Descripción
Este programa cumple como gestor de una base de datos específica desarrollada para el llamado *SANSANITO POKÉMON*.

El usuario deberá ejecutar comandos vía terminal con el programa en ejecución para realizar operaciones sobre la base de datos.
# Consideraciones
weás que importé
# Información relevante
Este programa se reserva las palabras *NONE* y *NULL*:
* NULL: Refiere a dejar el campo nulo, sin ningún valor.
* NONE: Esta palabra cumplirá dos funciones dependiendo de comando ejecutado:
    1. En comandos de **creación**: Establecerá un valor aleatorio o conveniente.
    2. En comandos de **actualización**: Conservará el valor anterior (En la tabla) del parámetro al que refiera.

Además, si se desean ingresar **parámetros que contengan espacios deben ser introducidos entre comillas dobles (")**, de lo contrario se interpretará como más de un valor.

Ej:

`CREATE "Mr. Mime" 10 Quemado` :heavy_check_mark:

Creará un Mr. Mime con 10 de hp Quemado.

`CREATE Mr. Mime 10 Quemado` :x:

Dará error.
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

`CONDITION <ESTADO>/NONE`

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