from typing import List, Dict, Optional
from collections import deque
from src.models.graph import Graph
from src.models.zone import Zone, ZoneType
from src.models.drone import Drone


class BFS:
    """
    BFS pour planifier le chemin des drones vers la destination
    """

    def __init__(self, graph: Graph):
        self.graph = graph
        self.prev: Dict[Zone, Optional[Zone]] = {}

    def find_route(self, start: Zone, goal: Zone) -> Optional[List[Zone]]:
        """
        Trouve un chemin du start vers goal.
        Retourne une liste de Zone ou None si aucun chemin.
        """
        queue = deque()
        visited = set()

        queue.append(start)
        visited.add(start)
        self.prev = {start: None}

        while queue:
            current = queue.popleft()

            if current == goal:
                # Reconstituer le chemin
                route = []
                node = goal
                while node:
                    route.append(node)
                    node = self.prev[node]
                route.reverse()
                return route

            for neighbor_name in self.graph.connections[current.name]:
                neighbor = self.graph.get_zone(neighbor_name)
                if neighbor and neighbor not in visited and self.can_visit(neighbor):
                    visited.add(neighbor)
                    queue.append(neighbor)
                    self.prev[neighbor] = current

        return None

    def can_visit(self, zone: Zone) -> bool:
        """
        Vérifie si une zone peut être visitée par BFS pour un drone
        """
        if zone.z_type == ZoneType.BLOCKED:
            return False
        if not zone.has_capacity():  # contrainte capacité
            return False
        return True