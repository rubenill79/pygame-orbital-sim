import os
import ctypes
import sys
import pygame
import math
import datetime
from astroquery.jplhorizons import Horizons
from astropy.time import Time

from .environment import OrbitalSystem

class Simulation():
    def __init__(
        self,
        app,
        scale = -1, 
        entity_scale = 10, 
        sim_rate = 2,
        start_date = None,
    ):    
        # dimensions: (ancho, alto) de la ventana en píxeles
        # scale: relación de ampliación entre AU y los píxeles mostrados (valor predeterminado -1: calculado automáticamente por self.set_scale())
        # entity_scale: ampliación adicional de las entidades para fines de visibilidad
        # sim_rate: cuántos días pasan en la simulación por cada segundo en la vida real (el valor predeterminado es 1 día por segundo)
        # dx, dy: desplazamiento en px como resultado de la panorámica con las teclas de flecha
        # offsetx, offsety: constantes al centro (0,0) en la ventana
        self.width =app.current_resolution[0]
        self.height = app.current_resolution[1]
        self.dx = 0
        self.dy = 0
        self.offsetx = self.width / 2
        self.offsety = self.height / 2

        self.default_scale = scale
        self.scale = scale
        self.entity_scale = entity_scale
        self.sim_rate = sim_rate
        self.sim_speed = datetime.datetime.today()

        if start_date:
            self.date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        else:
            self.date = datetime.datetime.today()

        # inicializar el objeto del sistema orbital
        self.orbital_system = OrbitalSystem()

        self.physics_delta_t = 0
        self.start_time_update = 0
        self.current_time_update = 0
        self.show_labels = True
        self.hovered = False
        self.paused = True
        self.ended = False
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
    def set_scale(self, max_a):
        # calcular y establecer automáticamente la escala en función del semieje mayor más grande en la matriz de entidades;
        # no hace nada si la escala se configura manualmente
        if self.scale < 0:
            new_scale = min(self.width, self.height) / (2 * max_a) 
            self.scale = new_scale
            self.default_scale = new_scale
    def change_sim_rate(self, speed_ratio):
        self.sim_rate *= speed_ratio
    """
    Añadir las entidades a la simulación
    """
    def add_custom_entity(
        self,
        position,
        mass,
        speed = 0,
        angle = 0,
        diameter = 1e-5,
        e = 0,
        a = None,
        name = ''
    ):  
        # posición: tuple (x, y) que describe la distancia en AU desde el centro del sistema (0, 0)
        # velocidad: magnitud de la velocidad inicial medida en AU/día
        # ángulo: ángulo de la velocidad inicial dado en radianes
        # masa: medida en kg
        # diámetro: medido en AU
        # (si corresponde) e: excentricidad de la órbita de la entidad en el rango de 0-1
        # (si corresponde) a: semieje mayor de la órbita de la entidad medido en AU
        # name: cadena de texto que se mostrará junto a la entidad cuando las etiquetas estén activadas
        if not a:
            x, y = position
            a = math.hypot(x, y)

        self.orbital_system.add_entity(
            position = position, 
            speed = speed, 
            angle = angle, 
            mass = mass, 
            diameter = diameter,
            e = e,
            a = a
        )
    def add_horizons_entity(self, colour, entity_id, observer_id, mass, diameter = 0.5e-5):
        # entity_id, observer_id: las ids numéricas asignadas por JPL SSD Horizons
        x, y, speed, angle, e, a, name = self.get_horizons_positioning(entity_id, observer_id)

        self.orbital_system.add_entity(
            colour,
            position = (x, y), 
            speed = speed, 
            angle = angle, 
            mass = mass, 
            diameter = diameter,
            e = e,
            a = a,
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
            name = elements['targetname'].data[0].replace('Barycenter ', '').replace('(','').replace(')','')

            # obtener la posicion y velocidad de los componentes del JPL SSD 
            x, y = vectors['x'], vectors['y']
            vx, vy = vectors['vx'], vectors['vy']
            speed = math.hypot(vx, vy)

            # calcular el ángulo de velocidad encontrando la tangente a la órbita
            # Específico de pygame: refleja horizontalmente el ángulo debido al eje y invertido
            angle = math.pi - ((2 * math.pi) - math.atan2(y, x))

            return x, y, speed, angle, e, a, name
        else:
            # caso especial para el cuerpo central del sistema (e.g. sun)
            # obj.elements() no funciona cuando entity_id y observer_id son iguales
            name = obj.vectors()['targetname'].data[0].replace('Barycenter ', '').replace('(','').replace(')','')
            return 0, 0, 0, 0, 0, 0, name
    """
    Funciones de la simulación
    """
    def update(self, delta_t):
        self.orbital_system.update(delta_t)
        self.update_date(delta_t)
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
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # teclas individuales
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_SPACE and not self.ended: self.paused = not self.paused
            if event.key == pygame.K_q: self.zoom(1.2)
            if event.key == pygame.K_e: self.zoom(0.8)
            if event.key == pygame.K_r: self.reset_zoom()
            if event.key == pygame.K_PERIOD: self.change_sim_rate(1.2)
            if event.key == pygame.K_COMMA: self.change_sim_rate(0.8)
            if event.key == pygame.K_l: self.show_labels = not self.show_labels
        # zoom con el mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: self.mouse_start_pos = pygame.mouse.get_pos()
            if event.button == 4: self.zoom(1.2)
            if event.button == 5: self.zoom(0.8)
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        # movimiento cámara
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                mouse_current_pos = pygame.mouse.get_pos()
                mouse_offset_x = mouse_current_pos[0] - self.mouse_start_pos[0]
                mouse_offset_y = mouse_current_pos[1] - self.mouse_start_pos[1]
                self.scroll(dx = mouse_offset_x / 100, dy = mouse_offset_y / 100)
        # movimiento cámara
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]: self.scroll(dx = 10)
        if keys[pygame.K_d]: self.scroll(dx = -10)
        if keys[pygame.K_w]: self.scroll(dy = 10)
        if keys[pygame.K_s]: self.scroll(dy = -10)
        if keys[pygame.K_f]: self.toggle_fullscreen()
        
        return True
    """
    Método Main
    """
    def start(self, app):
        """ 
        Constructor 
        """
        
        if app.fullscreen:
            display_info = pygame.display.Info()
            self.width = display_info.current_w
            self.height = display_info.current_h
            self.offsetx = self.width / 2
            self.offsety = self.height / 2

        # pasar sim_rate a cada entidad en la simulación;
        # también calcula el semieje mayor más grande y calcula la escala si corresponde
        semimajor_axes = []
        for entity in self.orbital_system.entities:
            entity.sim_rate = self.sim_rate
            semimajor_axes.append(entity.a)
        self.set_scale(max(semimajor_axes))

        font = pygame.font.Font('data/fonts/m5x7.otf', 32)
        
        clock = pygame.time.Clock()
        self.mouse_start_pos = (self.width/2,self.height/2)
        """
        # Hacer que la ventana se ponga por encima de las demás
        ctypes.windll.user32.SetForegroundWindow(pygame.display.get_wm_info()["window"])
        """
        """
        Bucle pygame
        """
        running = True
        while running:
            delta_t = clock.tick(500)
            
            # manejador de eventos
            for event in pygame.event.get(): running = self.handle_event(event)
            # actualizacion de físicas
            if not self.paused:
                self.physics_delta_t += delta_t
                # actualizar 50 veces por segundo
                if self.physics_delta_t >= 20:
                    #self.start_time_update = pygame.time.get_ticks() # Debug
                    self.update(self.physics_delta_t)
                    self.physics_delta_t = 0
                    #self.current_time_update = pygame.time.get_ticks() # Debug
            
            #start_time_draw = pygame.time.get_ticks() # Debug
            # limpiar pantalla
            app.screen.fill(self.orbital_system.bg)
            # dibujar planetas
            entity_labels = []
            # reset del hover
            self.hovered = False
            for i, entity in enumerate(self.orbital_system.entities):
                entity.sim_rate = self.sim_rate
                # calcular x, y teniendo en cuenta el zoom y la escala relativa debido a la cámara
                relative_scale = self.scale / self.default_scale
                x = relative_scale * ((self.scale * entity.x) + self.dx) + self.offsetx
                y = relative_scale * ((self.scale * -entity.y) + self.dy) + self.offsety # reflected across y-axis to compensate for pygame's reversed axes
                r = abs(int(entity.diameter * self.scale * self.entity_scale / 2 ))
                # solo dibujar lo que se va a ver en pantalla
                if x < self.width and y < self.height:
                    # hacer que los planetas se vean mejor desde largas distancias
                    if r == 0: r = 1
                    elif r <= 1 and self.scale > 300: r = 2
                    hitbox = 40
                    if r > 50: hitbox = r * 1.2
                    pygame.draw.circle(app.screen, entity.colour, (x, y), r)
       
                    # solo dibujar las etiquetas si hay hover del raton
                    mouse_current_pos = pygame.mouse.get_pos()
                    if not self.hovered and (mouse_current_pos[0] - hitbox < x and x < mouse_current_pos[0] + hitbox) and (mouse_current_pos[1] - hitbox < y and y < mouse_current_pos[1] + hitbox):
                        self.hovered = True
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        if i == 0:
                            if r < 2: r = 2
                            name_label = font.render(F"{entity.name}", True, (180, 180, 180))
                            diameter_label = font.render(F"Diámetro: {entity.diameter} UA", True, (180, 180, 180))
                            mass_label = font.render(F"Masa: {entity.mass} kg", True, (180, 180, 180))
                            density_label = font.render(F"Densidad: {entity.density} kg/UA", True, (180, 180, 180))
                            # append data to array
                            entity_labels.append((name_label, (x + 3 + r, y + 3 + r)))
                            entity_labels.append((diameter_label, (x + 3 + r, y + 3 + r + 30)))
                            entity_labels.append((mass_label, (x + 3 + r, y + 3 + r + 50)))
                            entity_labels.append((density_label, (x + 3 + r, y + 3 + r + 70)))
                        else:
                            # Distancia de sol a entidad con el teorema de pitágoras
                            name_label = font.render(F"{entity.name} | {math.hypot(entity.x, entity.y):.5f} UA", True, (180, 180, 180))
                            position_label = font.render(F"Posición: ({entity.x},{entity.y}) UA", True, (180, 180, 180))
                            diameter_label = font.render(F"Diámetro: {entity.diameter} UA", True, (180, 180, 180))
                            mass_label = font.render(F"Masa: {entity.mass} kg", True, (180, 180, 180))
                            density_label = font.render(F"Densidad: {entity.density} kg/UA", True, (180, 180, 180))
                            e_label = font.render(F"Excentricidad de la órbita: {entity.e}", True, (180, 180, 180))
                            a_label = font.render(F"Semieje mayor: {entity.a} UA", True, (180, 180, 180))
                            speed_label = font.render(F"Velocidad: {entity.speed} UA/día", True, (180, 180, 180))
                            angle_label = font.render(F"Ángulo de rotación: {entity.angle} rad", True, (180, 180, 180))
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
                        
                        # circle underline
                        pygame.draw.circle(app.screen, (180, 180, 180), (x, y), r*1.2,1)    
            
            if self.show_labels:
                for label in entity_labels:
                    text, position = label
                    app.screen.blit(text, position)
            
            # fecha
            date_display = font.render(self.date.strftime("%d %b %Y %H:%M"), 1, (255,255,255))
            app.screen.blit(date_display, (20, 20))
            # velocidad de simulación
            if not self.paused:
                try:
                    sim_hours = (self.sim_speed.seconds*50) // 3600
                    sim_minutes = ((self.sim_speed.seconds*50) /60) % 60
                    sim_rate_display = font.render(F"Simulando a: {sim_hours} horas y {sim_minutes:.5f} minutos / segundo" , 1, (255,255,255))                  
                    app.screen.blit(sim_rate_display, (20, 40))
                    sim_rate_hint_display = font.render(F"Una velocidad alta provocará fallos en la simulación" , 1, (255,255,255))                  
                    app.screen.blit(sim_rate_hint_display, (20, 60))
                except (AttributeError): pass      
            else:
                paused_display = font.render("SIMULACIÓN PAUSADA", 1, (0,102,204))
                app.screen.blit(paused_display, (self.width / 2 - paused_display.get_width()/2, 100))
            if self.ended:
                error_display = font.render("ERROR: NO SE PUEDE REANUDAR LA SIMULACIÓN", 1, (0,102,204))
                app.screen.blit(error_display, (self.width / 2 - error_display.get_width()/2, 120))
            #current_time_draw = pygame.time.get_ticks() # Debug   
            # tiempos de refresco
            # draw_display = font.render(F"Tiempo de renderizado: {current_time_draw-start_time_draw}ms", 1, (255,255,255))
            # app.screen.blit(draw_display, (20, self.height - 80))
            # update_display = font.render(F"Tiempo de físicas: {self.current_time_update-self.start_time_update}ms", 1, (255,255,255))
            # app.screen.blit(update_display, (20, self.height - 100 ))
            # fps
            fps_display = font.render(F"FPS: {clock.get_fps():.2f}", 1, (255,255,255))
            app.screen.blit(fps_display, (20, self.height - 60 ))
            # ups
            fps_display = font.render(F"Actualizaciones de físicas / segundo: {50}", 1, (255,255,255))
            app.screen.blit(fps_display, (20, self.height - 40 ))
            pygame.display.flip()