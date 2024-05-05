from .entity import Entity

class OrbitalSystem():
    def __init__(self, entities_number):
        self.entities = []
        self.entities_number = entities_number
        self.bg = "#080f20"

    def add_entity(
        self,
        colour,
        diameter = 8.5e-5,
        mass = 6e24,
        position = (0, 0),
        speed = 0,
        angle = 0,
        e = 0,
        a = 1,
        p = 0,
        arg_periapsis = 0,
        name = '',
        index = 0
    ):
        entity = Entity(colour, position, diameter, mass, self.central_mass, e, a, p, arg_periapsis, name, self.entities_number)
        entity.speed = speed
        entity.angle = angle

        self.entities.insert(index, entity)

    def update(self, delta_t):
        for i, entity in enumerate(self.entities):
            entity.delta_t = delta_t
            entity.move()
            entity.accelerate("", (0, 0))

            for entity2 in self.entities[i + 1:]:
                entity.attract(entity2)