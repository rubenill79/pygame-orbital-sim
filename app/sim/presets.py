from .simulation import Simulation
"""
Clase padre para los sistemas prediseñados / Hereda de Simulation
"""
class Preset(Simulation):
    def __init__(self, app, sim_rate):
        super().__init__(app, sim_rate)

    def add_entities(self, observer_id):

        for i, id_ in enumerate(self.entity_data.keys()):
            mass = self.entity_data[id_]['m']
            try:
                colour = self.entity_data[id_]['c']
            except KeyError:
                # No hace falta que todas tengan color ya que hay uno prediseñado para satélites y objetos diminutos
                colour = (255, 255, 255)
            
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

class CustomPreset(Preset):
    def __init__(self, app, prest_json):
        sim_rate = prest_json["global"]["min_sim_rate"]
        super().__init__(app, sim_rate)
        
        self.entity_data = prest_json["entity_data"]
        # El observer_id lo obtenemos de esta manera
        self.add_entities(list(self.entity_data.keys())[0])
