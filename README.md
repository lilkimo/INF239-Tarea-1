# Integrantes
Zarko Kuljis, 2018235233-7
# Descripción
Este programa cumple como gestor de una base de datos específica desarrollada para el llamado *SANSANITO POKÉMON*.
# Consideraciones
weás que importé
# Información relevante
Este programa se reserva las palabras 'NONE' y 'NULL'.
* NULL: Refiere a dejar el campo en nulo, sin ningún valor.
* NONE: Esta palabra cumplirá dos funciones dependiendo de comando ejecutado:
    1. En comandos de actualización: No modifica el valor del campo especificado; a diferencia de NULL, conservará el valor anterior en tabla del parámetro al que se refiera.
    2. En comandos de creación: Establecerá un valor aleatorio o conveniente.

Además, si se desean ingresar parámetros que contengan espacios deben ser introducidos entre comillas dobles ("), de lo contrario se interpretará como más de un valor.

Ej:

`CREATE "Mr. Mime" 10 Quemado`

Creará un 'Mr. Mime' con 10 de hp y con el estado 'Quemado'.
# Comandos
`CREATE <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE`

`READ <POKÉMON>`

`UPDATE <POKÉMON> <HPACTUAL>/NULL/NONE <ESTADO>/NULL/NONE <FECHA DE INGRESO>/NULL/NONE`

`DELETE <POKÉMON>`

`INSERT <POKÉMON> <HPACTUAL>/NONE <ESTADO>/NULL/NONE`

`TOP10`

`BOTTOM10`

`CONDITION <ESTADO>/NONE`

`LEGENDARIES`

`OLDESTONE`

`MOSTREPEATED`

`SHOWALL`

`EXIT`