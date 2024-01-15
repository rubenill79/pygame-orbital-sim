import math
from astropy.constants import G

def add_vectors(vector1, vector2):
    # vectores son cantidades con magnitud y dirección
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
       
    def __init__(self, colour, position, diameter, mass, e = 0, a = 1, name = ''):
        # posición: tuple (x, y) que describe la distancia en UA desde el centro del sistema (0, 0)
        # diámetro: medido en UA
        # masa: medida en kg
        # velocidad: magnitud de la velocidad inicial medida en UA/día
        # ángulo: ángulo de la velocidad inicial dado en rad
        # (si procede) e: excentricidad de la órbita, 0-1
        # (si procede) a: semieje mayor medido en UA
        self.x, self.y = position
        # convertir a float para optimizar la aplicación en las operaciones
        self.x, self.y = float(self.x), float(self.y)

        self.diameter = diameter
        self.mass = mass
        self.density = self.mass / (4/3 * math.pi * (self.diameter/2)**3)
        self.e = e
        self.a = a
        self.colour = colour
        self.name = name

        self.speed = 0
        self.angle = 0
        
        # G = [AU^3 * kg^-1 * d^-2]
        self.GForce = G.to('AU3 / (kg d2)').value

        # sim_rate: establecido externamente, describe el número de días que pasan en la simulación por cada segundo de la vida real (en tiempo real es 1.2e-5)
        # delta_t: el tiempo en ms entre fotogramas utilizado para mantener constante la tasa de simulación
        self.sim_rate = 1
        self.delta_t = 16
    """
    Cálculos físicos para el movimiento
    """
    def days_per_update(self):
    # devuelve el número de días que pasan en un intervalo dado delta_t
        return 1 / ( (1000 / self.sim_rate) / self.delta_t )
    def move(self):
        dpu = self.days_per_update()
        x, y = math.sin(self.angle) * self.speed * dpu, math.cos(self.angle) * self.speed * dpu
        self.x += x
        self.y -= y # resta debido al sistema de coordenadas de pygame porque 0,0 corresponde a la esquina superior en vez de la inferior
    def accelerate(self, acceleration):
        # ajusta la magnitud de la aceleración para los días pasados por fotograma
        # combina aplica la aceleración al vector velocidad
        acc_mag, acc_angle = acceleration
        acc_mag *= self.days_per_update()
        self.speed, self.angle = add_vectors((self.speed, self.angle), (acc_mag, acc_angle))
    def attract(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        theta = math.atan2(dy, dx)
        distance = math.hypot(dx, dy)

        # Calcular la fuerza de atracción debida a la gravedad utilizando la ley de gravitación universal de Newton:
        # F = G * m1 * m2 / r^2
        force = self.GForce * self.mass * other.mass / (distance ** 2)
     
        # acelerar ambos cuerpos uno hacia el otro mediante el vector de aceleración a = F/m, reordenado a partir de la segunda ley de Newton
        self.accelerate((force / self.mass, theta - (math.pi / 2)))
        other.accelerate((force / other.mass, theta + (math.pi / 2)))