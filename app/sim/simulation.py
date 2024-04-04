import pygame
import pygame.gfxdraw
import math
import datetime
from astroquery.jplhorizons import Horizons
from astropy.time import Time

from .environment import OrbitalSystem

class Simulation():
    def __init__(self, app, sim_rate, scale = 1,  entity_scale = 1):    
        # dimensions: (ancho, alto) de la ventana en píxeles
        # scale: relación de ampliación entre AU y los píxeles mostrados (valor predeterminado -1: calculado automáticamente por self.set_scale())
        # entity_scale: ampliación adicional de las entidades para fines de visibilidad
        # sim_rate: cuántos días pasan en la simulación por cada segundo en la vida real (el valor predeterminado es 1 día por segundo)
        # dx, dy: desplazamiento en px como resultado del movimiento de la cámara
        # offsetx, offsety: constantes al centro (0,0) en la ventana
        self.check_resolution(app)

        self.default_scale = scale
        self.scale = scale
        self.entity_scale = entity_scale
        self.sim_rate = sim_rate
        self.sim_speed = datetime.datetime.today()

        self.date = datetime.datetime.today()

        # inicializar el objeto del sistema orbital
        self.orbital_system = OrbitalSystem()

        self.physics_delta_t = 0
        self.start_time_update = 0
        self.current_time_update = 0
        self.show_labels = True
        
        self.paused = True
        self.ended = False
        
        self.left_click = False
        self.camera_center = False
        self.hovered = False
        self.overpass_mouse_hover = False
        self.focus_camera_index = -1
        self.focus_camera_last_index = -1
        self.focus_1_index = -1
        self.focus_2_index = -1
        self.focus_1_last_index = -1
        self.focus_2_last_index = -1
    """ 
    Acciones de la cámara
    """
    def scroll(self, dx = 0, dy = 0):
        # cambiar el desplazamiento para desplazarse/desplazarse por la pantalla
        relative_scale = self.scale / self.default_scale
        self.dx += dx / relative_scale
        self.dy += dy / relative_scale
    def zoom(self, zoom):
        # ajustar el nivel de zoom y el desplazamiento del zoom
        self.scale *= zoom
    def reset_zoom(self):
        # reset de todas las variables de la cámara a por defecto
        self.scale = self.default_scale
        self.dx = 0
        self.dy = 0
    def change_sim_rate(self, speed_ratio):
        self.sim_rate *= speed_ratio
    def check_resolution(self, app):
        self.width = app.current_resolution[0]
        if not app.fullscreen and app.current_resolution == app.resolution_fullscreen:
            self.height = app.current_resolution[1]*0.96
        else: self.height = app.current_resolution[1]
        self.dx = 0
        self.dy = 0
        self.offsetx = self.width / 2
        self.offsety = self.height / 2
    """
    Añadir las entidades a la simulación
    """
    def add_horizons_entity(self, colour, entity_id, observer_id, mass, diameter = 6.69e-9):
        # entity_id, observer_id: las ids numéricas asignadas por JPL SSD Horizons
        x, y, speed, angle, e, a, arg_periapsis, name = self.get_horizons_positioning(entity_id, observer_id)

        self.orbital_system.add_entity(
            colour,
            position = (x, y), 
            speed = speed, 
            angle = angle, 
            mass = mass, 
            diameter = diameter,
            e = e,
            a = a,
            arg_periapsis = arg_periapsis,
            name = name,
        ) 
    def get_horizons_positioning(self, entity_id, observer_id):
        obj = Horizons(
                id = entity_id, 
                location = '@{}'.format(observer_id),
                epochs = Time(self.date).jd,
                id_type='id'
            )
        
        if not entity_id == observer_id:
            vectors = obj.vectors()
            elements = obj.elements()

            # obtener el eje excéntrico (e) y semieje mayor (a) 
            e = elements['e'].data[0]
            a = elements['a'].data[0]
            arg_periapsis = elements['w'].data[0]
            name = elements['targetname'].data[0].replace('Barycenter ', '').replace('(','').replace(')','')

            # obtener la posicion y velocidad de los componentes del JPL SSD 
            x, y = vectors['x'], vectors['y']
            vx, vy = vectors['vx'], vectors['vy']
            speed = math.hypot(vx, vy)

            # calcular el ángulo de velocidad encontrando la tangente a la órbita
            # Específico de pygame: refleja horizontalmente el ángulo debido al eje y invertido
            angle = math.pi - ((2 * math.pi) - math.atan2(y, x))

            return x, y, speed, angle, e, a, arg_periapsis, name
        else:
            # caso especial para el cuerpo central del sistema (e.g. sun)
            # obj.elements() no funciona cuando entity_id y observer_id son iguales
            name = obj.vectors()['targetname'].data[0].replace('Barycenter ', '').replace('(','').replace(')','')
            return 0, 0, 0, 0, 0, 0, 0, name
    """
    Funciones de la simulación
    """
    def update(self, app, delta_t):
        if app.show_advanced_data:self.start_time_update = pygame.time.get_ticks() # Debug   
        self.orbital_system.update(delta_t)
        self.update_date(delta_t)
        if app.show_advanced_data: self.current_time_update = pygame.time.get_ticks() # Debug   
    def update_date(self, delta_t):
        # calcular el número de días que han pasado en la simulación desde el último frame
        # sumarlo al display del dia y igualarlo a la variable de tiempo de simulación
        try:
            self.sim_speed = datetime.timedelta(days = 1 / ( (1000 / self.sim_rate) / delta_t ))
            self.date += self.sim_speed
        except OverflowError:
            # Año 9999 se acaba el date
            self.paused = True
            self.ended = True
    """
    Método Start
    """
    def start(self):
        # pasar sim_rate a cada entidad en la simulación;
        for entity in self.orbital_system.entities: entity.sim_rate = self.sim_rate

        self.font = pygame.font.Font('data/fonts/m5x7.otf', 32)
        self.mouse_start_pos = (self.width/2,self.height/2)
    """
    Método Dibujar
    """
    def calculate_orbit_points(self, a, e, periapsis_degrees, num_points=360):
        points = []

        for i in range(num_points):
            theta = 2 * math.pi * i / num_points
            r = a * (1 - e**2) / (1 + e * math.cos(theta + periapsis_degrees))
            # Calculate rotated coordinates
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            
            relative_scale = self.scale / self.default_scale
            # Convert to screen coordinates
            screen_x = relative_scale * ((self.scale * x) + self.dx) + self.offsetx
            screen_y = relative_scale * ((self.scale * -y) + self.dy) + self.offsety
            points.append((screen_x, screen_y))
            
        return points
    
    def draw(self, app, clock):
            if app.show_advanced_data: start_time_draw = pygame.time.get_ticks() # Debug
            # limpiar pantalla
            app.screen.fill(self.orbital_system.bg)
            # dibujar planetas
            entity_draw = []
            entity_orbit_draw = []
            entity_labels = []
            selected_entities = []
            mouse_current_pos = pygame.mouse.get_pos()
            # reset del hover
            self.hovered = False
            for i, entity in enumerate(self.orbital_system.entities):
                entity.sim_rate = self.sim_rate
                # calcular x, y teniendo en cuenta el zoom y la escala relativa debido a la cámara
                relative_scale = self.scale / self.default_scale
                x = relative_scale * ((self.scale * entity.x) + self.dx) + self.offsetx
                y = relative_scale * ((self.scale * -entity.y) + self.dy) + self.offsety # reflected across y-axis to compensate for pygame's reversed axes
                r = abs(int((entity.diameter * 150) * self.scale * self.entity_scale / 2 )) #*150 to pass it form UA to Km
                # solo dibujar lo que se va a ver en pantalla o si la camara esta centrada o es una de las entidades apuntadas o la central
                if (x < self.width and y < self.height) or (self.focus_camera_index == i or self.focus_1_index == i or self.focus_2_index == i or i == 0):
                    # hacer que los planetas se vean mejor desde largas distancias
                    if r == 0: r = 1
                    elif r <= 1 and self.scale > 300: r = 2
                    hitbox = 40
                    if r > 40: hitbox = r * 1.2
                    entity_draw.append((entity.colour, (x, y), r,0))
       
                    # solo dibujar las etiquetas si hay hover del raton
                    self.can_hover = ((mouse_current_pos[0] - hitbox < x 
                        and x < mouse_current_pos[0] + hitbox) and (mouse_current_pos[1] - hitbox < y 
                        and y < mouse_current_pos[1] + hitbox))
                    if not app.paused and ((self.focus_camera_index == i or self.focus_1_index == i) or (self.overpass_mouse_hover and self.focus_2_index == i) or (not self.hovered and self.can_hover and app.enable_mouse_hover)):
                        if self.focus_camera_index == i and (self.focus_1_index == i or self.focus_2_index == i): selected_entities.append(entity)
                        elif self.focus_camera_index == i and (self.focus_1_index != i or self.focus_2_index != i): pass
                        else: selected_entities.append(entity)
                        if not self.hovered and self.can_hover and app.enable_mouse_hover: 
                            self.hovered = True
                            self.overpass_mouse_hover = False
                            self.focus_2_index = i
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        if self.left_click and self.can_hover:
                            self.left_click = False
                            self.focus = True
                            self.focus_camera_index = i
                            self.focus_1_index = i
                        if self.focus_camera_index == i and self.focus:
                            # Centrar la cámara en el planeta
                            new_offsetx = self.offsetx - x
                            new_offsety = self.offsety - y
                            self.scroll(dx=new_offsetx, dy=new_offsety)
                        if self.focus_camera_index is not self.focus_camera_last_index:
                            self.focus_camera_last_index = self.focus_camera_index
                            app.play_menu_element[4].update_externaly_changed_entities_camera_center_objects(entity.name)
                        if self.focus_1_index is not self.focus_1_last_index:
                            self.focus_1_last_index = self.focus_1_index
                            app.play_menu_element[4].update_externaly_changed_entities_focus_1_objects(entity.name)
                        if self.focus_2_index is not self.focus_2_last_index:
                            self.focus_2_last_index = self.focus_2_index
                            app.play_menu_element[4].update_externaly_changed_entities_focus_2_objects(entity.name)
                        
                        entity_draw.append(((180, 180, 180), (x, y), r*1.2,1))
                        if i != 0:
                            entity_orbit_draw.append((self.calculate_orbit_points(entity.a, entity.e, entity.arg_periapsis)))
                            
                            """
                            rx = relative_scale * ((self.scale * (entity.a * (1-entity.e))))
                            ry = relative_scale * ((self.scale * (entity.a * math.sqrt(1 - entity.e**2))))
                            print(rx,ry)
                            entity_orbit_draw.append((rx, ry, (180, 180, 180)))
                            """
                        if i == 0:
                            if r < 2: r = 2
                            name_label = self.font.render(F"{entity.name}", True, (180, 180, 180))
                            diameter_label = self.font.render(F"{app.diameter_text}: {entity.diameter} UA", True, (180, 180, 180))
                            mass_label = self.font.render(F"{app.mass_text}: {entity.mass} kg", True, (180, 180, 180))
                            density_label = self.font.render(F"{app.density_text}: {entity.density} kg/UA", True, (180, 180, 180))
                            # append data to array
                            entity_labels.append((name_label, (x + 3 + r, y + 3 + r)))
                            entity_labels.append((diameter_label, (x + 3 + r, y + 3 + r + 30)))
                            entity_labels.append((mass_label, (x + 3 + r, y + 3 + r + 50)))
                            entity_labels.append((density_label, (x + 3 + r, y + 3 + r + 70)))
                        else:
                            # Distancia de sol a entidad con el teorema de pitágoras
                            name_label = self.font.render(F"{entity.name} | {math.hypot(entity.x, entity.y):.5f} UA", True, (180, 180, 180))
                            position_label = self.font.render(F"{app.position_text}: ({entity.x},{entity.y}) UA", True, (180, 180, 180))
                            if entity.diameter == 6.69e-9: diameter_label = self.font.render(F"{app.diameter_text}: {app.small_diameter_text}", True, (180, 180, 180))
                            else: diameter_label = self.font.render(F"{app.diameter_text}: {entity.diameter} UA", True, (180, 180, 180))
                            mass_label = self.font.render(F"{app.mass_text}: {entity.mass} kg", True, (180, 180, 180))
                            density_label = self.font.render(F"{app.density_text}: {entity.density} kg/UA", True, (180, 180, 180))
                            e_label = self.font.render(F"{app.eccentricity_text}: {entity.e}", True, (180, 180, 180))
                            a_label = self.font.render(F"{app.major_axis_text}: {entity.a} UA", True, (180, 180, 180))
                            speed_label = self.font.render(F"{app.velocity_text}: {entity.speed} UA {app.per_day_text}", True, (180, 180, 180))
                            angle_label = self.font.render(F"{app.angle_text}: {entity.angle} rad", True, (180, 180, 180))
                            # append data to array
                            entity_labels.append((name_label, (x + 3 + r, y + 3 + r)))
                            entity_labels.append((position_label, (x + 3 + r, y + 3 + r + 30)))
                            entity_labels.append((diameter_label, (x + 3 + r, y + 3 + r + 50)))
                            entity_labels.append((mass_label, (x + 3 + r, y + 3 + r + 70)))
                            entity_labels.append((density_label, (x + 3 + r, y + 3 + r + 90)))
                            entity_labels.append((e_label, (x + 3 + r, y + 3 + r + 110)))
                            entity_labels.append((a_label, (x + 3 + r, y + 3 + r + 130)))
                            entity_labels.append((speed_label, (x + 3 + r, y + 3 + r + 150)))
                            entity_labels.append((angle_label, (x + 3 + r, y + 3 + r + 170)))  
                        
            if not app.paused and not self.hovered and app.button_hovered is False: pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if self.left_click:
                self.left_click = False
                self.camera_center = False
                self.hovered = False
                self.overpass_mouse_hover = False
                self.focus_camera_index = -1
                self.focus_camera_last_index = -1
                self.focus_1_index = -1
                self.focus_2_index = -1
                self.focus_1_last_index = -1
                self.focus_2_last_index = -1
                app.play_menu_element[4].update_externaly_changed_entities_camera_center_objects("pygame-gui.None")
                app.play_menu_element[4].update_externaly_changed_entities_focus_1_objects("pygame-gui.None")
                app.play_menu_element[4].update_externaly_changed_entities_focus_2_objects("pygame-gui.None")
            
            if len(selected_entities) == 2:
                x1, y1 = selected_entities[0].x, selected_entities[0].y
                x2, y2 = selected_entities[1].x, selected_entities[1].y
                
                x1_screen = relative_scale * ((self.scale * x1) + self.dx) + self.offsetx
                y1_screen = relative_scale * ((self.scale * -y1) + self.dy) + self.offsety
                x2_screen = relative_scale * ((self.scale * x2) + self.dx) + self.offsetx
                y2_screen = relative_scale * ((self.scale * -y2) + self.dy) + self.offsety
                # Distancia euclidiana
                distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
                angle = math.degrees(math.atan2((y2 - y1), (x2 - x1)))
                if 90 <= angle <= 180: angle -= 180
                elif -180 <= angle <= -90: angle += 180
                
                distance_text = self.font.render(f"{distance:.5f} UA", True, (180, 180, 180))
                distance_text_rotated = pygame.transform.rotate(distance_text, angle)
                app.screen.blit(distance_text_rotated, (((x1_screen + x2_screen) //2 - distance_text.get_width()/2), (y1_screen + y2_screen) //2 - distance_text.get_height()/2))
                
                pygame.draw.line(app.screen, (180, 180, 180), (x1_screen, y1_screen), (x2_screen, y2_screen), 1)
            
            for entity in entity_draw:
                colour, position, radius, width = entity
                pygame.draw.circle(app.screen, colour, (position), radius, width)
            for orbit_points in entity_orbit_draw:
                pygame.draw.lines(app.screen, (180, 180, 180), True, orbit_points, 1)
            """
                rx, ry, colour = orbit
                target_rect = pygame.Rect([0, 0, self.width, self.height])
                shape_surf = pygame.Surface(target_rect.size, pygame.SRCALPHA)
                pygame.gfxdraw.ellipse(shape_surf, self.center_x, self.center_y, int(rx), int(ry), colour)
                rotated_surf = pygame.transform.rotate(shape_surf, 45)
                app.screen.blit(rotated_surf, rotated_surf.get_rect(center = [self.center_x, self.center_y]))
                pygame.gfxdraw.ellipse(app.screen, self.center_x, self.center_y, int(rx), int(ry), colour)
            """
            if self.show_labels:
                for label in entity_labels:
                    text, position = label
                    app.screen.blit(text, position)
                
            
            # fecha
            date_display = self.font.render(self.date.strftime("%d %b %Y %H:%M"), 1, (255,255,255))
            app.screen.blit(date_display, (20, 20))
            # velocidad de simulación
            if not self.paused:
                try:
                    sim_hours = (self.sim_speed.seconds*50) // 3600
                    sim_minutes = ((self.sim_speed.seconds*50) /60) % 60
                    sim_rate_display = self.font.render(F"{app.simulating_text}: {sim_hours} {app.hours_text} {app.and_text} {sim_minutes:.5f} {app.minutes_text} {app.per_second_text}" , 1, (255,255,255))                  
                    app.screen.blit(sim_rate_display, (20, 40))
                    sim_rate_hint_display = self.font.render(F"{app.high_speed_text}" , 1, (255,255,255))                  
                    app.screen.blit(sim_rate_hint_display, (20, 60))
                except (AttributeError): pass      
            else:
                paused_display = self.font.render(app.simulation_paused_text, 1, (0,102,204))
                app.screen.blit(paused_display, (self.width / 2 - paused_display.get_width()/2, 100))
            if self.ended:
                error_display = self.font.render(F"{app.sim_error_text}", 1, (0,102,204))
                app.screen.blit(error_display, (self.width / 2 - error_display.get_width()/2, 120))
            if app.show_advanced_data: current_time_draw = pygame.time.get_ticks() # Debug   
            # ups
            if app.show_advanced_data and not app.paused:
                physics_update_display = self.font.render(F"{app.physics_update_text}: {50}", 1, (255,255,255))
                app.screen.blit(physics_update_display, (20, self.height - 60 ))
                # tiempos de refresco
                draw_display = self.font.render(F"Tiempo de renderizado: {current_time_draw-start_time_draw}ms", 1, (255,255,255))
                app.screen.blit(draw_display, (20, self.height - 80))
                if not app.simulation.paused:
                    update_display = self.font.render(F"Tiempo de físicas: {self.current_time_update-self.start_time_update}ms", 1, (255,255,255))
                    app.screen.blit(update_display, (20, self.height - 100 ))
            # fps
            if app.show_FPS:
                fps_display = self.font.render(F"FPS: {clock.get_fps():.2f}", 1, (255,255,255))
                app.screen.blit(fps_display, (20, self.height - 40 ))
            