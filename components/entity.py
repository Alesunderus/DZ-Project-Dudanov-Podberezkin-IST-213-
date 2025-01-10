class Entity:
    def __init__(self, *components, x=0, y=0):
        self.components = []
        for c in components:
            self.add(c, False)
        for c in components:
            g = getattr(c, 'setup', None)
            if callable(g):
                c.setup()
        self.x = x
        self.y = y

    def add(self, component, perform_setup = True):
        self.components.append(component)
        component.entity = self
        if perform_setup:
            g = getattr(component, 'setup', None)
            if callable(g):
                component.setup()

    def delete_self(self):
        from core.area import area
        if self in area.entities:
            area.entities.remove(self)
        for c in self.components:
            g = getattr(c, 'breakdown', None)
            if callable(g):
                c.breakdown()
        self.components.clear()

    def remove(self, kind):
        c = self.get(kind)
        self.remove_component(c)

    def remove_component(self, c):
        if c is not None:
            g = getattr(c, 'breakdown', None)
            if callable(g):
                c.breakdown()
            c.entity = None
            self.components.remove(c)

    def has(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return True
        return False

    def get(self, kind):
        for c in self.components:
            if isinstance(c, kind):
                return c
        return None