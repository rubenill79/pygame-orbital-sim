from simulation import Simulation
"""
Clase padre para los sistemas prediseñados / Hereda de Simulation
"""
class Preset(Simulation):
    def __init__(
        self, 
        dimensions = (800, 800), 
        scale = -1, 
        entity_scale = 5, 
        sim_rate = 3,
        start_date = None,
        fullscreen = False
    ):
        super().__init__(dimensions, scale, entity_scale, sim_rate, start_date, fullscreen)

    def add_entities(self, observer_id):

        for i, id_ in enumerate(self.entity_data.keys()):
            mass = self.entity_data[id_]['m']
            colour = self.entity_data[id_]['c']
            try:
                diameter = self.entity_data[id_]['d']
                # Metodo que accede a la api Horizons y descarga los datos
                self.add_horizons_entity(
                    colour = colour,
                    entity_id = id_,
                    observer_id = observer_id,
                    mass = mass,
                    diameter = diameter         
                )
            except KeyError:
                # No hace falta que todas tengan diametro ya que hay uno prediseñado para satélites
                self.add_horizons_entity(
                    colour = colour,
                    entity_id = id_,
                    observer_id = observer_id,
                    mass = mass,
                )

            print('Entidad {} de {} añadida con éxito'.format(i + 1, len(self.entity_data)))
"""
Clases hijas para cada sistema prediseñado
"""
class EarthMoon(Preset):
    def __init__(self, 
        dimensions = (800, 800), 
        scale = -1, 
        entity_scale = 1, 
        sim_rate = 1,
        start_date = None,
        fullscreen = False
    ):
        super().__init__(dimensions, scale, entity_scale, sim_rate, start_date, fullscreen)

        self.entity_data = {
            '3': {
                'm': 6e24,
                'd': 8.5e-5,
                'c': (0, 0, 255)
            },
            '301': { 
                'm': 7.342e22,
                'd': 2.3e-5,
                'c': (192, 192, 192)
            },
            '-125544': {
                'm': 4.15e2,
                'c': (192, 192, 192)
            }
        }
        self.add_entities('3')

class InnerSolarSystem(Preset):
    def __init__(self, 
        dimensions = (800, 800), 
        scale = -1, 
        entity_scale = 5, 
        sim_rate = 3,
        start_date = None,
        fullscreen = False
    ):
        super().__init__(dimensions, scale, entity_scale, sim_rate, start_date, fullscreen)

        self.entity_data = {
            'sun': {
                'm': 1.99e30,
                'd': 9.29e-3,
                'c': (243, 145, 50)
            },
            '1': {
                'm': 3.30e23,
                'd': 3.26e-5,
                'c': (169, 169, 169)
            },
            '2': {
                'm': 4.9e24,
                'd': 8.1e-5,
                'c': (255, 165, 0) 
            },
            '3': {
                'm': 6e24,
                'd': 8.5e-5,
                'c': (0, 0, 255)
            },
            '4': {
                'm': 6.4e23,
                'd': 4.5e-5,
                'c': (255, 69, 0)
            }
        }

        self.add_entities('sun')

class SolarSystem(Preset):
   def __init__(self, 
        dimensions = (800, 800), 
        scale = -1, 
        entity_scale = 5, 
        sim_rate = 3,
        start_date = None,
        fullscreen = False
    ):
        super().__init__(dimensions, scale, entity_scale, sim_rate, start_date, fullscreen)

        self.entity_data = {
            'sun': {
                'm': 1.99e30,
                'd': 9.29e-3,
                'c': (243, 145, 50)
            },
            '1': {
                'm': 3.30e23,
                'd': 3.26e-5,
                'c': (169, 169, 169)
            },
            '2': {
                'm': 4.9e24,
                'd': 8.1e-5,
                'c': (255, 165, 0) 
            },
            '3': {
                'm': 6e24,
                'd': 8.5e-5,
                'c': (0, 0, 255)
            },
            '4': {
                'm': 6.4e23,
                'd': 4.5e-5,
                'c': (255, 69, 0)
            },
            '5': {
                'm': 1.9e27,
                'd': 9.56e-4,
                'c': (255, 224, 147)
            },
            '6': {
                'm': 5.7e26,
                'd': 8.05e-4,
                'c': (210, 180, 140)
            },
            '7': {
                'm': 8.7e25,
                'd': 3.4e-4,
                'c': (173, 216, 230) 
            },
            '8': {
                'm': 1e26,
                'd': 3.31e-4,
                'c': (0, 0, 128)
            }, 
            '9': {
                'm': 1.46e22,
                'd': 1.58e-5,
                'c': (142, 109, 97)
            }
        }
        self.add_entities('sun')

class EnhancedSolarSystem(Preset):
   def __init__(self, 
        dimensions = (800, 800), 
        scale = -1, 
        entity_scale = 5, 
        sim_rate = 3,
        start_date = None,
        fullscreen = False
    ):
        super().__init__(dimensions, scale, entity_scale, sim_rate, start_date, fullscreen)

        self.entity_data = {
            'sun': {
                'm': 1.99e30,
                'd': 9.29e-3,
                'c': (243, 145, 50)
            },
            '1': {
                'm': 3.30e23,
                'd': 3.26e-5,
                'c': (169, 169, 169)
            },
            '2': {
                'm': 4.9e24,
                'd': 8.1e-5,
                'c': (255, 165, 0) 
            },
            '3': {
                'm': 6e24,
                'd': 8.5e-5,
                'c': (0, 0, 255)
            },
            '4': {
                'm': 6.4e23,
                'd': 4.5e-5,
                'c': (255, 69, 0)
            },
            '5': {
                'm': 1.9e27,
                'd': 9.56e-4,
                'c': (255, 224, 147)
            },
            '6': {
                'm': 5.7e26,
                'd': 8.05e-4,
                'c': (210, 180, 140)
            },
            '7': {
                'm': 8.7e25,
                'd': 3.4e-4,
                'c': (173, 216, 230) 
            },
            '8': {
                'm': 1e26,
                'd': 3.31e-4,
                'c': (0, 0, 128)
            }, 
            '9': {
                'm': 1.46e22,
                'd': 1.58e-5,
                'c': (142, 109, 97)
            },
            '-31': {
                'm': 7.22e2,
                'c': (142, 109, 97)
            },
            '-32': {
                'm': 8.15e2,
                'c': (142, 109, 97)
            },
            '-96': {
                'm': 6.85e2,
                'c': (142, 109, 97)
            },
            '-227': {
                'm': 1.039e3,
                'c': (142, 109, 97)
            },
            '-143205': {
                'm': 1.3e3,
                'c': (142, 109, 97)
            },
            '-23': {
                'm': 2.58e2,
                'c': (142, 109, 97)
            },
            '-24': {
                'm': 2.58e2,
                'c': (142, 109, 97)
            },
            '20065803': {
                'm': 5.4e11,
                'c': (142, 109, 97)
            },
            '2000001': {
                'm': 9.43e20,
                'd': 9.46e-3,
                'c': (142, 109, 97)
            }
        }
        self.add_entities('sun')