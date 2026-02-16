from dataclasses import dataclass, field
from typing import Optional, List, TYPE_CHECKING
from enum import Enum, auto
from src.models.zone import Zone


class DroneState(Enum):
    IDLE = auto()
    MOVING = auto()
    IN_TRANSIT = auto()
    WAITING = auto()
    ARRIVED = auto()


@dataclass
class Drone:
    
    drone_id: int 
    state: DroneState = DroneState.IDLE
    path: List['Zone'] = field(default_factory=list) 
    transit_target: Optional['Zone'] = None
    transit_remaining: int = 0

    @property 
    def current_zone(self) -> Optional['Zone']:
        if self.path_index < len(self.path): 
            return self.path[self.path_index]
        return None
    
    @property
    def next_zone(self) -> Optional['Zone']:
        if self.path_index + 1 < len(self.path): 
            return self.path[self.path_index + 1]
        return None
    
    def is_at_destination(self, goal: 'Zone') -> bool:
        return self.state == DroneState.ARRIVED or (
            self.current_zone == goal and self.path_index > 0
        )
    
    def advance(self) -> None:
        if self.next_zone:
            self.path_index += 1
            self.state = DroneState.MOVING
        else:
            self.state = DroneState.ARRIVED 
    
    def start_transit_to_restricted(self, target: 'Zone') -> None:
        self.transit_target = target
        self.transit_remaining = 1
        self.state = DroneState.IN_TRANSIT

    def update_transit(self) -> bool:
        if self.state != DroneState.IN_TRANSIT:
            return False
        self.transit_remaining -= 1
        if self.transit_remaining <= 0 and self.transit_target:
            self.path_index += 1
            self.state = DroneState.MOVING
            return True
        return False