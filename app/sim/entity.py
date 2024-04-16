import math
from astropy.constants import G

"""
Los vectores polares son cantidades con magnitud y dirección
Cálculos para sumar dos vectores en coordenadas polares y obtener el vector resultante.
Devuelve un nuevo vector en coordenadas polares (magnitud, ángulo).
"""
def add_vectors(vector1, vector2):
    # agregarlos conectándolos de un extremo a otro para formar un vector resultante
    # sumamos los componentes x e y para obtener un triángulo rectángulo con hipotenusa de la magnitud del vector resultante
    mag1, angle1 = vector1
    mag2, angle2 = vector2
    x = mag1 * math.sin(angle1) + mag2 * math.sin(angle2)
    y = mag1 * math.cos(angle1) + mag2 * math.cos(angle2)

    # utilizar Pitágoras para calcular la magnitud del vector resultante
    mag = math.hypot(x, y)
    # uso de la trigonometría inversa para encontrar el ángulo del triángulo rectángulo, restar 90 grados para obtener el ángulo vecotr resultante
    # atan2 se encarga de x = 0
    angle = (math.pi / 2) - math.atan2(y, x)

    return (mag, angle)
"""
Clase Entidad (Planetas o satélites)
"""
class Entity():
       
    def __init__(self, colour, position, diameter, mass, central_mass, e = 0, a = 1, p = 0, arg_periapsis = 0, name = ''):
        # posición: tuple (x, y) que describe la distancia en UA desde el centro del sistema (0, 0)
        # diámetro: medido en UA
        # masa: medida en kg
        # velocidad: magnitud de la velocidad inicial medida en UA/día
        # ángulo: ángulo de la velocidad inicial dado en rad
        # e: excentricidad de la órbita, 0-1
        # a: semieje mayor medido en UA

        self.x, self.y = position
        # convertir a float para optimizar la velocidad en las operaciones
        self.x, self.y = float(self.x), float(self.y)

        self.diameter = diameter
        self.mass = mass
        self.density = self.mass / (4/3 * math.pi * (self.diameter/2)**3)
        self.e = e
        self.a = a
        self.orbital_period_days = p
        try:
            self.orbital_period_years = self.orbital_period_days / 365.256
        except ValueError:
            self.orbital_period_years = 0
        try:
            self.b = a * math.sqrt(1 - e**2)
        except ValueError:
            self.b = 0
        self.arg_periapsis = math.radians(arg_periapsis)
        self.colour = colour
        self.name = name

        self.speed = 0
        self.angle = 0
        # G = m³/kg/s²
        self.G = 6.674e-11
        # GForce = [AU^3 * kg^-1 * d^-2]
        self.GForce = G.to('AU3 / (kg d2)').value
        """
        try:
            # Keplerian orbital period formula: T = 2π√(a^3 / (G * M))
            self.orbital_period_seconds = 2 * math.pi * math.sqrt((a * 1.4961e11) ** 3 / (self.G * central_mass))
            self.orbital_period_days = self.orbital_period_seconds / 86400
            self.orbital_period_years = self.orbital_period_days / 365.25636
        except ValueError:
            self.orbital_period_seconds = 0
            self.orbital_period_days = 0
            self.orbital_period_years = 0
        """
        #self.orbital_points = []
        
        # sim_rate: establecido externamente, describe el número de días que pasan en la simulación por cada segundo de la vida real (en tiempo real es 1.2e-5)
        # delta_t: el tiempo en ms entre fotogramas utilizado para mantener constante la tasa de simulación
        self.sim_rate = 1
        self.delta_t = 16
    """
    Cálculos físicos para el movimiento
    """
    def days_per_update(self):
        # Devuelve el número de días que pasan en un intervalo dado delta_t
        # Utilizado para simular el movimiento en función de la tasa de simulación y el tiempo entre fotogramas.
        return 1 / ( (1000 / self.sim_rate) / self.delta_t )
    def move(self):
        # Simula el movimiento de la entidad en función de su velocidad y ángulo.
        # Actualiza las coordenadas de la entidad en el plano.
        dpu = self.days_per_update()
        x, y = math.sin(self.angle) * self.speed * dpu, math.cos(self.angle) * self.speed * dpu
        self.x += x
        self.y -= y # resta debido al sistema de coordenadas de pygame porque 0,0 corresponde a la esquina superior en vez de la inferior
        #self.orbital_points.append((self.x, self.y))
        """
        a = math.hypot(self.x, self.y)
        if a > self.a: self.a = a
        """
    def accelerate(self, acceleration):
        # Ajusta la magnitud de la aceleración para los días pasados por fotograma
        # Aplica una aceleración a la entidad en función de su velocidad actual y la nueva aceleración.
        # Utiliza funciones trigonométricas para combinar las aceleraciones en coordenadas polares.
        acc_mag, acc_angle = acceleration
        acc_mag *= self.days_per_update()
        self.speed, self.angle = add_vectors((self.speed, self.angle), (acc_mag, acc_angle))
    def attract(self, other):
        # Calcula la atracción gravitatoria entre dos entidades y ajusta sus velocidades en consecuencia.
        dx = self.x - other.x
        dy = self.y - other.y
        theta = math.atan2(dy, dx)
        distance = math.hypot(dx, dy)

        # Calcular la fuerza de atracción debida a la gravedad utilizando la ley de gravitación universal de Newton:
        # F = G * m1 * m2 / r^2
        force = (self.GForce * self.mass * other.mass) / (distance ** 2)
     
        # Acelerar ambos cuerpos uno hacia el otro mediante el vector de aceleración a = F/m, reordenado a partir de la segunda ley de Newton
        self.accelerate((force / self.mass, theta - (math.pi / 2)))
        other.accelerate((force / other.mass, theta + (math.pi / 2)))