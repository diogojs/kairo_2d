from abc import ABCMeta, abstractmethod
from typing import Dict, Optional

from pygame import Surface, Vector2


class Entity(metaclass=ABCMeta):
    _current_id = 0

    def __init__(self, position: Optional[Vector2] = None):
        if position is None:
            position = Vector2(0, 0)
        elif type(position) == type(tuple()):
            position = Vector2(position[0], position[1])

        self.id = Entity.current_id()
        self.position = position
        self.components: Dict[int, Entity] = dict()

    @classmethod
    def current_id(cls):
        cls._current_id += 1
        return cls._current_id

    @property
    def x(self):
        return self.position.x

    @x.setter
    def x(self, value):
        if value < 0:
            value = 0
        self.position = Vector2(value, self.y)

    @property
    def y(self):
        return self.position.y

    @y.setter
    def y(self, value):
        if value < 0:
            value = 0
        self.position = Vector2(self.x, value)

    def add_component(self, component):
        self.components[component.id] = component

    def remove_component(self, id_or_component):
        if isinstance(id_or_component, int):
            self.components.pop(id_or_component)
        elif isinstance(id_or_component, Entity):
            self.components.pop(id_or_component.id)
        else:
            raise TypeError("Trying to remove component of invalid type.")

    @abstractmethod
    def update(self):
        raise NotImplementedError

    @abstractmethod
    def render(self, surf: Surface):
        raise NotImplementedError
