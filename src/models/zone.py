from __future__ import annotations
from dataclasses import dataclass field
from typing import Optional , Set
from enum import Enum , auto

class ZoneType(Enum):
    NORMAL = auto()
    BLOCKED = auto()
    RESTRICTED = auto()
    PRIORITY = auto()

@dataclass
class Zone:
    """
        Represente une zone du graphe avec ses proprites et contraintes
    """
    def __init__(self,name: str,x:int, y:int, capacity:int ,z_type:ZoneType):
        self.name:str = name
        self.x:int = x
        self.y:int = y
        self.capacity:int = capacity
        self.z_type:ZoneType = z_type.ZoneType.NORMAL
        self.color:Optional[str] = None
        current_drones :Set[int] = field(default_factory=set , repr=False)
        self.max_drones = 1

    def is_accessible(self)->bool:
        return self.z_type == ZoneType.BLOCKED

    def get_movement_cost(self)->int:
        if self.z_type == ZoneType.BLOCKED:
            return 0
        elif self.z_type == ZoneType.RESTRICTED
            return 2
        return 1

    def has_capacity(self)->bool:
        return len(self.current_drones) < self.max_drones
    
    def occupy(self,drone_id:int)->None:
        if not self.has_capacity():
            raise CapacityError(f"Zone {self.name} pleine")
        self.current_drones.add(drone_id)

    def vacate(self , drone_id:str)->None:
        self.current_drones.discard(drone_id)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self , other:Object):
        if not isinstance(other,Zone):
            return NotImplemented
        return self.name == other.name
        