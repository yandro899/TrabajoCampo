# Trabajo Campo: Sistema experto para guias turisticos de Termas de Jordan
## Introducción

## Instalación
### Requisitos
* Se requiere la instalacion de Python 3.8. Otra version puede causar problemas.
* Instalar la libreria "experta" de Python usando >pip install experta
* Descargar este repositorio

### Ejecución
Debe dirigirse al directorio del repositorio descargado y ejecutar "exec.bat". Se abrirá una ventana de consola de Windows.

## Uso
Le pedirá ingresar los siguientes datos personales:
* Apellido
* Nombre
* DNI
* Edad
* Grupo Sanguineo
* Facto Sanguineo

Luego le preguntará si hace deportes o tiene actividad fisica. Ponga 0 si no la hace, 1 que si lo hace.
Despues le preguntará si padece de alguna enfermedad, siendo las posibilidades:
* asma: Padece Asma
* sobrepeso: Padece sobrepeso
* sano: Esta saludable

Luego le preguntará sobre el clima actual, siendo las opciones:
* soleado
* nublado
* lluvia

Despues le preguntará la estacion del año, siendo las opciones:
* verano
* otoño
* invierno
* primavera

Por ultimo, debe elegir que atraccion desea hacer. En el programa aparecen las opciones y debe elegir una.

Finalmente el programa se ejecuta, recomendando al usuario si la atraccion que eligio es recomendable, ademas de imprimir en un papel (archivo "datosturistas.txt") los datos personales del turista para que el guía los tenga en casos de emergencia.

## Futuros agregados
* Que se puede trabajar con mas de un turista
* Que se pueda elegir mas de una atraccion por turista
* En caso de circuitos no aptos, recomendar otros
