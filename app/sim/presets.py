from .simulation import Simulation
import threading
import time
from requests.exceptions import HTTPError
"""
Clase padre para los sistemas prediseñados / Hereda de Simulation
"""
class Preset(Simulation):
    def __init__(self, app, config_values, entities_number):
        super().__init__(app, config_values, entities_number)
            
    def add_horizons_entity_thread(self, i, total_entities, observer_id, id_, mass, colour, diameter=None):
        # Número máximo de reintentos
        MAX_RETRIES = 5
        success = False
        retries = 0

        while not success and retries < MAX_RETRIES:
            try:
                if diameter is not None:
                    self.add_horizons_entity(
                        colour=colour,
                        entity_id=id_,
                        observer_id=observer_id,
                        mass=mass,
                        index=i,
                        diameter=diameter
                    )
                else:
                    self.add_horizons_entity(
                        colour=colour,
                        entity_id=id_,
                        observer_id=observer_id,
                        index=i,
                        mass=mass
                    )
                # Si no hay error, marca como exitoso
                success = True
                print('Entidad {} de {} añadida con éxito'.format(i + 1, total_entities))

            except HTTPError:
                retries += 1
                print(f"Error HTTP encontrado en entidad: {i + 1}. Intento {retries} de {MAX_RETRIES}")
                time.sleep(1)  # Esperar 1 segundo antes de reintentar

        if not success:
            print("Error: no se pudo añadir la entidad tras varios intentos.")
            
    def add_custom_entity_thread(self, i, total_entities, entity_data_list, name):
        
        position = entity_data_list['pos']
        mass = entity_data_list['m']
        speed = entity_data_list['s']
        angle = entity_data_list['rad']
        e = entity_data_list['e']
        a = entity_data_list['a']
        p = entity_data_list['p']
        arg_periapsis = entity_data_list['per']
        
        if i == 0: self.orbital_system.central_mass = mass
        
        # Diccionario para guardar argumentos opcionales
        optional_args = {}
        # Intenta asignar opcionales, captura si alguna falta
        if 'c' in entity_data_list:
            optional_args['colour'] = entity_data_list['c']
        if 'd' in entity_data_list:
            optional_args['diameter'] = entity_data_list['d']
            
        # Llamar al método con argumentos fijos y opcionales
        self.add_custom_entity(position, mass, speed, angle, e, a, p, arg_periapsis, name, i, **optional_args)
        
        print('Entidad {} de {} añadida con éxito'.format(i + 1, total_entities))


    def add_entities(self, observer_id):
        total_entities = len(self.entity_data)
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
                thread = threading.Thread(target=self.add_horizons_entity_thread, args=(i, total_entities, observer_id, id_, mass, colour, diameter))
            except KeyError:
                # No hace falta que todas tengan diámetro ya que hay uno prediseñado para satélites
                thread = threading.Thread(target=self.add_horizons_entity_thread, args=(i, total_entities, observer_id, id_, mass, colour))
        
            threads.append(thread)
            thread.start()
            time.sleep(0.3)
        # Espera a que todos los hilos terminen
        for thread in threads:
            thread.join()

        print('Todas las entidades añadidas con éxito')
        
    def add_custom_entities(self):
        total_entities = len(self.entity_data)
        threads = []
        for i, name in enumerate(self.entity_data.keys()):
            thread = threading.Thread(target=self.add_custom_entity_thread, args=(i, total_entities, self.entity_data[name], name))
            threads.append(thread)
            thread.start()
        # Espera a que todos los hilos terminen
        for thread in threads:
            thread.join()

        print('Todas las entidades añadidas con éxito')

class CustomPreset(Preset):
    def __init__(self, app, prest_json):
        config_values = [
            prest_json["global"]["start_sim_rate"],
            prest_json["global"]["min_sim_rate"],
            prest_json["global"]["max_sim_rate"],
            prest_json["global"]["start_scale"],
            prest_json["global"]["min_scale"],
            prest_json["global"]["max_scale"]
        ]
        if app.offline_mode: self.entity_data = prest_json["offline_entity_data"]
        else: self.entity_data = prest_json["online_entity_data"]
        super().__init__(app, config_values, len(self.entity_data))
        # El observer_id lo obtenemos de esta manera
        if app.offline_mode: self.add_custom_entities()
        else: self.add_entities(list(self.entity_data.keys())[0])
