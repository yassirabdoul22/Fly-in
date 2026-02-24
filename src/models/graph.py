from typing import Dict, List, Optional
from .zone import Zone,ZoneType
from .drone import Drone

class Graph:
    def __init__(self):
        self.zones: Dict[str, Zone] = {}
        self.connections: Dict[str, List[str]] = {}

    def add_zone(self, zone: Zone):
        self.zones[zone.name] = zone
        if zone.name not in self.connections:
            self.connections[zone.name] = []

    def add_connection(self, zone1_name: str, zone2_name: str):
        if zone1_name not in self.zones or zone2_name not in self.zones:
            raise ValueError("Zone must be created before creating a connection")

        self.connections[zone1_name].append(zone2_name)
        self.connections[zone2_name].append(zone1_name)

    def get_zone(self, name: str) -> Optional[Zone]:
        return self.zones.get(name)

    def can_move(self, drone: Drone, next_zone_name: str) -> bool:
        zone = self.get_zone(next_zone_name)
        if not zone:
            return False
        if zone.z_type == ZoneType.BLOCKED:
            return False
        if not zone.has_capacity():
            return False
        return True
