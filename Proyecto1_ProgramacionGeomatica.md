# Proyecto 1 Programación Aplicada a la Geomática
- Programa que cree un archivo vectorial a partir de los datos históricos de población mundial del banco mundial y un archivo vectorial de las geometrás de cada país. Este archivo deberá contener los datos históricos de población por año, asociados a la geometría de cada país.
- Otro programa que a partir del archivo vectorial anterior calcule las tasas de variación poblacional anual y genere mapas de variación poblacional de cada año, que resalten el 20% de los paises con mayor crecimiento poblacional y el 20% con menor crecimiento poblacional para cada año.


Para el primer apartado de se hará un **join** de ambos dataset por medio del código **ISO-A3** del archivo que contiene las geometrias y el **Country Code** del archivo que contiene los datos históricos de población.
Un paso de suma importancia es comprobar que ambos datasets contengan los mismos paises y de no ser así, descartar aquellos que no se encuentren en el dataset de los datos históricos, se realiza una intersección de las llaves que se utilizan para realizar el join menciaonado anteriormente.
Una vez que se tiene esto el primer punto del proyecto se cumplió y como resultado se tiene un archivo vectorial que contiene las geometrias de los paises y sus respectivos datos historicos.

Para el segundo apartado se pide calcular la variación anual de población, en este caso la solución es la siguiente:

Tenemos datos desde 1960 a 2021, en algunos casos no se tienen datos de población de algunos años, para esto se sustituyen por un **0**, se compara el año de inicio con su inmediato siguiente, por lo que se puede resumir en una iteración que realiza una operación con los valores correspondientes. Ejemplo:

$$TasaVarciación_{anual} = ({(\frac{ValorAnual_{n}}{ValorAnual_{n+1}})-1) \ast 100}$$

De esta manera se calcula la tasa de variación anual para cada país.