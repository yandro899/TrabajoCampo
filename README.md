# TrabajoCampo
Trabajo de campo de la materia Ingenieria del Conocimiento de la Universidad Nacional de Jujuy, referida a turismo de las Termas de Jordan

Aqui iria el futuro manual de usuario, pero enseño que deben hacer para usar esto.

Primero instalen Python, especificamente la version 3.8 porque es la que funciona. NO INSTALEN VERSIONES SUPERIORES A LA 3.10

Segundo, instalen "experta", que es la libreria de Python.

Luego ejecuten Python en el directorio de este proyecto y pongan "exec(open(TermasJordan.py").read()) para que cargue el archivo

Deben resetear el interprete usando:

>>> engine.reset()

Asi lo pueden usar. Para cargar hechos usen "engine.declare([HECHO])" donde "HECHO" puede ser por ejemplo:

>>> engine.declare(CondMedica("asma"))  # La persona padece Asma

Para hacer funcionar el motor de inferencias (una vez cargados todos los hechos necesarios), pongan:

>>> engine.run()

Para ver que hechos se pusieron, pueden poner en la consola de Python:

>>> engine.facts

PROXIMAMENTE SE VA A HACER MAS FUNCIONAL ESTO

TODO:

* Cargar los atractivos usando un json
* Agregar interactividad al programa
* Entregar recomendaciones
* Mostrar peligros para los turistas si es necesario
