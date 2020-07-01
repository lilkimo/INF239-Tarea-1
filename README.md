Comandos:

CREATE [Datos] [SANSANITO POKEMON]
    La operación «CREATE» añade una nueva fila en la tabla POYO.
    [Datos] corresponde a los datos del Pokémon en el formato de la tabla POYO.
Estos deben ir en el orden especificado en la Tarea (Número en la PokéDex, Nombre, Type 1, etc...) y separados por comas («,»); Si un dato no existe o se desconoce escriba «Missing» (Sin las comillas).
Si no escribe todos los datos se asumirán los faltantes como Missing.
    [SANSANITO POKEMON] es un valor booleano que por default es False.
Declarar este valor como True insertará forzosamente a la tabla SANSANITO POKEMON, omitiendo el protocolo y así pudiendo generar resultados no deseados (Por ejemplo; Que esta tabla tenga 51 Pokémon en ella).
Todos los datos que no posean equivalente en la tabla POYO se establecerán nulos o tomarán el valor Default.
Se recomienda no declarar este parámetro o declararlo False. Para inserciones preferiblemente use «INSERT_PKMN»
Ejemplo:
    In:CREATE 6,Charizard,Missing,Flying
*Este comando es equivalente a:
    In:CREATE 6,Charizard,Missing,Flying,Missing,Missing False

READ [Tipo de Dato] [Dato]
    La operación «READ» lee la información de una fila en la tabla POYO, en el orden que se define en la tarea.
Si el Pokémon también se encuentra en SANSANITO POKEMON, leerá los datos en el formato de esta tabla y mostrará tantas instancias como existan, ordenadas arbitrariamente. Añadiendo los datos exclusivos de esta tabla.
    [Tipo de Dato] es la definición del dato que se ingresará a continuación para así filtrar la tabla.
    [Dato] refiere al valor del tipo de dato especificado anteriormente.
Ejemplo:
    In[1] :READ nombre Bulbasaur
    Out[1]:1,Bulbasaur,Grass,Missing,318
*Este Pokémon no está en la tabla SANSANITO POKEMON

    In[1] :Read pokedex 1
    Out[1]:1,1,Bulbasaur,Grass,Missing,28,318,False,Missing,12-10-1998 21:05:43,290
    Out[2]:1,1,Bulbasaur,Grass,Missing,54,318,False,Paralizado,12-17-1998 10:47:02,274
*Este Pokémon está en la tabla SANSANITO POKEMON, 2 veces.

//Pokemones con hp actual >=0


=====BORRAR=====
TRIGGERS:
Al cambiar el HP_Actual y/o el ESTADO debe cambiar la prioridad.

VISTAS:
Consultas sobre la tabla.
================

