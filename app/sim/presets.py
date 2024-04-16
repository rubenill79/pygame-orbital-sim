from .simulation import Simulation
import threading
import time
"""
Clase padre para los sistemas prediseñados / Hereda de Simulation
"""
class Preset(Simulation):
    def __init__(self, app, sim_rate):
        super().__init__(app, sim_rate)
            
    def add_entity_thread(self, i, entity_data, observer_id, id_, mass, colour, diameter=None):
        # Método que accede a la API Horizons y descarga los datos
        if diameter is not None:
            self.add_horizons_entity(
                colour=colour,
                entity_id=id_,
                observer_id=observer_id,
                mass=mass,
                diameter=diameter
            )
        else:
            self.add_horizons_entity(
                colour=colour,
                entity_id=id_,
                observer_id=observer_id,
                mass=mass
            )
        print('Entidad {} de {} añadida con éxito'.format(i + 1, len(entity_data)))

    def add_entities(self, observer_id):
        threads = []
        for i, id_ in enumerate(self.entity_data.keys()):
            mass = self.entity_data[id_]['m']
            if i == 0:
                self.orbital_system.central_mass = mass
            try:
                colour = self.entity_data[id_]['c']
            except KeyError:
                # No hace falta que todas tengan color ya que hay uno prediseñado para satélites y objetos diminutos
                colour = (255, 255, 255)
        
            try:
                diameter = self.entity_data[id_]['d']
                thread = threading.Thread(target=self.add_entity_thread, args=(i, self.entity_data, observer_id, id_, mass, colour, diameter))
            except KeyError:
                # No hace falta que todas tengan diámetro ya que hay uno prediseñado para satélites
                thread = threading.Thread(target=self.add_entity_thread, args=(i, self.entity_data, observer_id, id_, mass, colour))
        
            threads.append(thread)
            thread.start()
            time.sleep(0.4)
        # Espera a que todos los hilos terminen
        for thread in threads:
            thread.join()

        print('Todas las entidades añadidas con éxito')

class CustomPreset(Preset):
    def __init__(self, app, prest_json):
        sim_rate = prest_json["global"]["min_sim_rate"]
        super().__init__(app, sim_rate)
        
        self.entity_data = prest_json["entity_data"]
        # El observer_id lo obtenemos de esta manera
        self.add_entities(list(self.entity_data.keys())[0])
