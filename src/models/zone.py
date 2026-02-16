from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Set
from enum import Enum, auto


class ZoneType(Enum):
    NORMAL = auto()
    BLOCKED = auto()
    RESTRICTED = auto()
    PRIORITY = auto()


class CapacityError(Exception):
    """Exception levée lorsqu'une zone est pleine."""
    pass


@dataclass
class Zone:
    """
    Représente une zone du graphe avec ses propriétés et contraintes.
    """
    name: str
    x: int
    y: int
    capacity: int = 1
    z_type: ZoneType = ZoneType.NORMAL
    color: Optional[str] = None
    current_drones: Set[int] = field(default_factory=set, repr=False)

    def is_accessible(self) -> bool:
        """Renvoie True si la zone peut être visitée (non bloquée)."""
        return self.z_type != ZoneType.BLOCKED

    def get_movement_cost(self) -> int:
        """Coût de déplacement selon le type de zone."""
        if self.z_type == ZoneType.BLOCKED:
            return 0
        elif self.z_type == ZoneType.RESTRICTED:
            return 2
        elif self.z_type == ZoneType.PRIORITY:
            return 1  # priorité pourrait être utilisée dans l'algorithme de pathfinding
        return 1  # NORMAL

    def has_capacity(self) -> bool:
        """Vérifie si la zone peut accueillir un drone supplémentaire."""
        return len(self.current_drones) < self.capacity

    def occupy(self, drone_id: int) -> None:
        """Marque la zone comme occupée par un drone."""
        if not self.has_capacity():
            raise CapacityError(f"Zone {self.name} pleine")
        self.current_drones.add(drone_id)

    def vacate(self, drone_id: int) -> None:
        """Libère la zone d'un drone."""
        self.current_drones.discard(drone_id)

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Zone):
            return NotImplemented
        return self.name == other.name
