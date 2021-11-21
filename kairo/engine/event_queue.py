from typing import Dict, Optional
from time import time

from kairo.engine import STD_DELTA


class Event():
    def __init__(self, name: str = ''):
        self.name = name


class EventQueue():
    def __init__(self):
        self.events: Dict[float, Event] = {}
        self.frame_time = time()
        self.tick = 0.25
    
    def add(self, event: Event, *, timestep: Optional[float] = None, frames_ahead: int = 0) -> None:
        if frames_ahead:
            event_time = self.frame_time + frames_ahead * self.tick
        elif timestep:
            if timestep < time():
                raise ValueError("Timestep must be greater than current time")
            event_time = timestep
        else:
            event_time = time()

        if event_time in self.events:
            event_time += STD_DELTA

        self.events[event_time] = event


def test_event_queue():
    queue = EventQueue()
    for i in range(10):
        if 3 < i < 7:
            ev = Event('arroba')
        else:
            ev = Event()
        queue.add(ev)

    assert len(queue.events) == 10

    counter = 0
    for event in queue.events.values():
        if event.name:
            counter += 1
    
    assert counter == 3

