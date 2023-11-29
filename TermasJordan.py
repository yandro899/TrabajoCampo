from experta import *
import json
import math

g_iRecomendacion = 0

class CondFisica(Fact):
    """Condicion fisica del turista"""
    pass

class CondMedica(Fact):
    """Condicion medica del turista"""
    pass

class NivelAptFisica(Fact):
    """Nivel aptitud fisica del turista"""
    pass

class DificultadAtractivo(Fact):
    """Nivel de dificultad del atractivo"""
    pass

class NivelAptGeneral(Fact):
    """Nivel aptitud general del turista"""
    pass

class Clima(Fact):
    """Clima para poder hacer un atractivo"""
    pass

class Epoca(Fact):
    """Epoca del año para hacer un atractivo"""
    pass

class AtraccionTipo(Fact):
    """Tipo de atraccion"""
    pass

class AptitudClima(Fact):
    """Determina si el clima es el ideal para la atraccion seleccionada"""
    pass

class Edad(Fact):
    """Edad del turista"""
    pass

class AptitudEdad(Fact):
    """Aptitud del turista segun la edad"""
    pass

class RecomendacionCircuito(Fact):
    """Recomendacion final del circuito"""
    pass

class TermasJodan(KnowledgeEngine):
    """
    Aptitud Fisica
    Al analiar las reglas, para simplificar operaciones logicas se pudo corroborar
    observando las tablas de decision que:
    * El Sobrepeso es condicion necesaria y suficiente para que alguien no sea apto
    * Tener Asma es condicion necesaria y suficiente para que alguien este medianamente apto, pero no debe padecer sobrepeso
    """
    @Rule(CondFisica("si"), CondMedica("sano"))
    def nAptFis_sano(self):
        self.declare(NivelAptFisica("sano"))
        print("Turista apto fisicamente para el circuito")

    @Rule(CondMedica("asma"), NOT(CondMedica("sobrepeso")))
    def nAptFis_medSano(self):
        self.declare(NivelAptFisica("med_sano"))
        print("Turista medianamente apto fisicamente para el circuito")

    @Rule(CondMedica("sobrepeso"))
    def nAptFis_noSano(self):
        self.declare(NivelAptFisica("no_sano"))
        print("Turista NO apto fisicamente para el circuito")

    """
    Nivel aptitud general del turista
    """

    @Rule(OR(
            AND(NivelAptFisica("sano"), DificultadAtractivo("alta")),
            AND(NivelAptFisica("sano"), DificultadAtractivo("baja")),
            AND(NivelAptFisica("med_sano"), DificultadAtractivo("baja")),
            AND(NivelAptFisica("sano"), DificultadAtractivo("media"))
            )
        )
    def nAptGen_apto(self):
        self.declare(NivelAptGeneral("apto"))
        print("Turista APTO para el circuito")

    @Rule(OR(
            AND(NivelAptFisica("med_sano"), DificultadAtractivo("alta")),
            AND(NivelAptFisica("no_sano"), DificultadAtractivo("baja")),
            AND(NivelAptFisica("med_sano"), DificultadAtractivo("media"))
            )
        )
    def nAptGen_medApto(self):
        self.declare(NivelAptGeneral("med_apto"))
        print("Turista MEDIANAMENTE APTO para el circuito")

    @Rule(OR(
            AND(NivelAptFisica("no_sano"), DificultadAtractivo("alta")),
            AND(NivelAptFisica("no_sano"), DificultadAtractivo("media"))
            )
        )
    def nAptGen_noApto(self):
        self.declare(NivelAptGeneral("apto"))
        print("Turista NO APTO para el circuito")
    
    """
    Aptitud segun edad
    """

    @Rule(OR(
        Edad("<5"), Edad(">50")
    ))
    def nAptEdad_noApto(self):
        self.declare(AptitudEdad("no_apto"))
        print("Edad NO APTA")

    @Rule(Edad("5-50"))
    def nAptEdad_apto(self):
        self.declare(AptitudEdad("apto"))
        print("Edad APTA")

    """
    Aptitud del clima
    Se consulto a la experta si se puede ir a las cascadas si esta nublado, ya que nos fataba saber eso
    """

    @Rule(OR(
        AND(AtraccionTipo("cascada"), OR(Clima("soleado"), Clima("nublado"))),
        AND(AtraccionTipo("termas"), NOT(Epoca("verano"))),
        AND(AtraccionTipo("mirador"), Clima("soleado")),
        AND(AtraccionTipo("canon"), OR(Clima("soleado"), Clima("nublado")))
    ))
    def nAptClima_apto(self):
        self.declare(AptitudClima("apto"))
        print("Clima APTO para el circuito")

    @Rule(OR(
        AND(AtraccionTipo("cascada"), Clima("lluvia")),
        AND(AtraccionTipo("termas"), Epoca("verano")),
        AND(AtraccionTipo("mirador"), OR(Clima("lluvia"), Clima("nublado"))),
        AND(AtraccionTipo("canon"), Clima("lluvia"))
    ))
    def nAptClima_noApto(self):
        self.declare(AptitudClima("no_apto"))
        print("Clima NO APTO para el circuito")
    
    """
    PARTE FINAL
    Recomendacion del circuito
    """

    @Rule(AptitudClima("apto"), NivelAptGeneral("apto"), AptitudEdad("apto"))
    def recAtract_muyBien(self):
        self.declare(RecomendacionCircuito("muy_bien"))
        #print("EL ATRACTIVO SELECCIONADO ES MUY RECOMENDABLE PARA EL TURISTA")
        global g_iRecomendacion
        g_iRecomendacion = 3

    @Rule(OR(
            AND(AptitudClima("apto"), NivelAptGeneral("apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("apto"), AptitudEdad("apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("med_apto"), AptitudEdad("apto")),
    ))
    def recAtract_bien(self):
        self.declare(RecomendacionCircuito("bien"))
        #print("EL ATRACTIVO SELECCIONADO ES RECOMENDABLE PARA EL TURISTA")
        global g_iRecomendacion
        g_iRecomendacion = 2
    
    @Rule(OR(
            AND(AptitudClima("no_apto"), NivelAptGeneral("apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("med_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("med_apto"), AptitudEdad("apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("no_apto"), AptitudEdad("apto")),
    ))
    def recAtract_advertencia(self):
        self.declare(RecomendacionCircuito("adv"))
        #print("EL ATRACTIVO SELECCIONADO TIENE CIERTOS PROBLEMAS PARA EL TURISTA")
        global g_iRecomendacion
        g_iRecomendacion = 1

        
    @Rule(OR(
            AND(AptitudClima("no_apto"), NivelAptGeneral("med_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("no_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("no_apto"), AptitudEdad("apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("no_apto"), AptitudEdad("no_apto")),
    ))
    def recAtract_noRec(self):
        self.declare(RecomendacionCircuito("no_rec"))
        #print("EL ATRACTIVO SELECCIONADO NO ES NADA RECOMENDABLE PARA EL TURISTA")
        global g_iRecomendacion
        g_iRecomendacion = 0

def calcPitagoras(x1, x2, y1, y2):
    return int(math.sqrt(math.pow(x2-x1,2)+math.pow(y2-y1,2)))

def findCaminoMasCorto(x0, y0, atractivos):
    nearAtract = 0
    i = 0
    nearDist = 100000
    for atract in atractivos:
        x1 = int(atract["ubicacion"]["x"])
        y1 = int(atract["ubicacion"]["y"])
        newDist = calcPitagoras(x0,x1,y0,y1)
        if ( newDist < nearDist):
            nearDist = newDist
            nearAtract = i
        i = i+1
    
    return nearAtract

def calcDistCircuito(atractivos):
    newAtractivos = atractivos.copy()
    # Este punto avanza por cada atractivo armando la distancia
    pos = {
        "x": 0,
        "y": 0
    }

    dist = 0

    while len(newAtractivos) > 0:
        index = findCaminoMasCorto(pos["x"], pos["y"], newAtractivos)
        selectAtract = newAtractivos[index]["ubicacion"]
        dist = dist + calcPitagoras(pos["x"], int(selectAtract["x"]), pos["y"], int(selectAtract["y"]))
        pos["x"] = int(selectAtract["x"])
        pos["y"] = int(selectAtract["y"])
        newAtractivos.pop(index)

    dist = dist + calcPitagoras(pos["x"], 0, pos["y"], 0)

    return dist

engine = TermasJodan()

"""
Como se hara el programa?

* Cargamos primero los atractivos en el json

* Pedimos nombre del turista (por ahora uno solo)

* Ingresamos datos medicos y fisicos

* Ingresamos clima y epoca del año

** Mostramos atractivos que quiere visitar. Elige los que quiera ir.

** Procesa los atractivos armando un circuito

Lanza las recomendaciones

"""
with open('atractivos\data.json') as user_file:
  file_contents = user_file.read()

parsed_json = json.loads(file_contents)

data_atractivos = parsed_json['atractivos']

# Datos del turista
datos_turista = {
    "nombre": "",
    "apellido": "",
    "dni":  0,
    "edad": 0,
    "grupo_sanguineo": "",
    "factor_sanguineo": "",
    "act_deport": 0,
    "est_medico": "",
    "atractivos": [],
    "rec_atractivos": []
}

estado_tiempo = {
    "clima": "",
    "epoca": "",
}

# TODO: Control de entradad de datos
datos_turista["apellido"] = input("Cual es su apellido? ")
datos_turista["nombre"] = input("Cual es su nombre? ")

error = True
while error:
    error = False
    try:
        datos_turista["dni"] = int(input("Cual es su dni? "))
    except:
        error = True

datos_turista["edad"] = int(input("Cual es su edad? "))
datos_turista["grupo_sanguineo"] = input("Cual es su grupo sanguineo? ")
datos_turista["factor_sanguineo"] = input("Cual es su factor sanguineo? ")
datos_turista["act_deport"] = bool(input("hace deportes o alguna actividad fisica? "))
datos_turista["est_medico"] = input("padece alguna enfermedad? ")

estado_tiempo["clima"] = input("Cual es el clima actual? ")
estado_tiempo["epoca"] = input("Cual es la estacion del año actual? ")

#print(datos_turista)
#print(estado_tiempo)

print("Se ven las siguientes atracciones, elija una")
i = 1
for atractivo in data_atractivos:
    print(i," - ", atractivo["nombre"])
    i = i+1

opcionAtractivo = int(input("Numero de atraccion: "))

datos_turista["atractivos"].append(data_atractivos[opcionAtractivo-1])

hechos_individuales = []

# Setea hechos de edad
if datos_turista["edad"] < 5:
    hechos_individuales.append(Edad("<5"))
elif datos_turista["edad"] > 50:
    hechos_individuales.append(Edad(">50"))
else:
    hechos_individuales.append(Edad("5-50"))

# Setea hechos de clima y epoca
hechos_individuales.append(Clima(estado_tiempo["clima"]))
hechos_individuales.append(Epoca(estado_tiempo["epoca"]))

# Setea hechos turista
hechos_individuales.append(CondMedica(datos_turista["est_medico"]))
if datos_turista["act_deport"]:
    hechos_individuales.append(CondFisica("si"))
else:
    hechos_individuales.append(CondFisica("no"))

# Setea hechos por atractivo
for select_atract in datos_turista["atractivos"]:
    
    engine.reset()

    for hecho in hechos_individuales:
        engine.declare(hecho)

    if (select_atract["dificultad"] == "Alta"):
        engine.declare(DificultadAtractivo("alta"))
    elif (select_atract["dificultad"] == "Media"):
        engine.declare(DificultadAtractivo("media"))
    else:
        engine.declare(DificultadAtractivo("baja"))

    engine.declare(AtraccionTipo(select_atract["tipo"]))

    engine.run()

    datos_turista["rec_atractivos"].append(g_iRecomendacion)
    
distTotal = calcDistCircuito(datos_turista["atractivos"])
print("El circuito elegido (", datos_turista["atractivos"][0]["nombre"], ") tiene la recomendacion:")

if (datos_turista["rec_atractivos"][0] == 3):
    print(" ***** MUY buena eleccion ***** ")
elif (datos_turista["rec_atractivos"][0] == 2):
    print(" ***** Buena eleccion ***** ")
elif (datos_turista["rec_atractivos"][0] == 1):
    print(" ***** Eleccion con algunos problemas ***** ")
else:
    print(" ***** NO recomendable ***** ")

print("La distancia de recorrido total es de", distTotal, "metros, y el tiempo aproximado de recorrido es de minimamente", int(distTotal/4000), "horas.")

with open('datosturistas.txt', 'w') as f:
    f.write("Nombre: {}".format(datos_turista["nombre"]))
    f.write("\nApellido: {}".format(datos_turista["apellido"]))
    f.write("\nEdad: {}".format(datos_turista["edad"]))
    f.write("\nGrupo Sanguineo: {}".format(datos_turista["grupo_sanguineo"]))
    f.write("\nFactor Sanguineo: {}".format(datos_turista["factor_sanguineo"]))
    f.write("\nDNI: {}".format(datos_turista["dni"]))
    if (datos_turista["act_deport"]):
        f.write("\nHace deportes: Si")
    else:
        f.write("\nHace deportes: No")
    f.write("\nEnfermedad: {}".format(datos_turista["est_medico"]))