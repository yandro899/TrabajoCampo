from experta import *
import json

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

class TermasJordan(KnowledgeEngine):
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
    def nAptGen_apto(self):
        self.declare(NivelAptGeneral("apto"))
        print("Turista NO APTO para el circuito")

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
    PARTE FINAL
    Recomendacion del circuito
    """

    @Rule(AptitudClima("apto"), NivelAptGeneral("apto"), AptitudEdad("apto"))
    def recAtract_muyBien(self):
        self.declare(RecomendacionCircuito("muy_bien"))
        print("EL ATRACTIVO SELECCIONADO ES MUY RECOMENDABLE PARA EL TURISTA")

    @Rule(OR(
            AND(AptitudClima("apto"), NivelAptGeneral("apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("apto"), AptitudEdad("apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("med_apto"), AptitudEdad("apto")),
    ))
    def recAtract_bien(self):
        self.declare(RecomendacionCircuito("bien"))
        print("EL ATRACTIVO SELECCIONADO ES RECOMENDABLE PARA EL TURISTA")

    @Rule(OR(
            AND(AptitudClima("no_apto"), NivelAptGeneral("apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("med_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("med_apto"), AptitudEdad("apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("no_apto"), AptitudEdad("apto")),
    ))
    def recAtract_advertencia(self):
        self.declare(RecomendacionCircuito("adv"))
        print("EL ATRACTIVO SELECCIONADO TIENE CIERTOS PROBLEMAS PARA EL TURISTA")

        
    @Rule(OR(
            AND(AptitudClima("no_apto"), NivelAptGeneral("med_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("apto"), NivelAptGeneral("no_apto"), AptitudEdad("no_apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("no_apto"), AptitudEdad("apto")),
            AND(AptitudClima("no_apto"), NivelAptGeneral("no_apto"), AptitudEdad("no_apto")),
    ))
    def recAtract_advertencia(self):
        self.declare(RecomendacionCircuito("no_rec"))
        print("EL ATRACTIVO SELECCIONADO NO ES NADA RECOMENDABLE PARA EL TURISTA")

#engine = TermasJordan()

"""
Como se hara el programa?

Cargamos primero los atractivos en el json

Pedimos nombre del turista (por ahora uno solo)

Ingresamos datos medicos y fisicos

Ingresamos clima y epoca del año

Mostramos atractivos que quiere visitar. Elige los que quiera ir.

Procesa los atractivos armando un circuito

Lanza las recomendaciones

"""
with open('atractivos\data.json') as user_file:
  file_contents = user_file.read()

parsed_json = json.loads(file_contents)

data_atractivos = parsed_json['atractivos']

#print(data_atractivos[0]['nombre'])
""" f = open('atractivos\data.json')
data = json.load(f)
for i in data['atractivos']:
    print(i)

f.close() """

# Datos del turista



