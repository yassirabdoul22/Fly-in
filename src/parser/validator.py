class Validator:
    def __init__(self, parsed_config: ParsedConfig):
        self.config = parsed_config

    def validate(self) -> None:
        """
        Lancer toutes les validations.
        Raise ValueError ou custom exceptions si quelque chose ne va pas.
        """
        self._check_basic()
        self._check_connections()
        self._check_blocked_zones()
        self._check_reachability()
        self._check_capacities()


    def _check_basic(self):
        if self.config.nb_drones <= 0:
            raise ValueError("nb_drones must be > 0")
        if not self.config.start_zone:
            raise ValueError("start_zone not defined")
        if not self.config.goal_zone:
            raise ValueError("goal_zone not defined")

    def _check_connections(self):
        for zone_name, neighbors in self.config.graph.adjacency.items():
            if zone_name not in self.config.graph.zones:
                raise ValueError(f"Zone {zone_name} in connections does not exist")
            for neighbor in neighbors:
                if neighbor not in self.config.graph.zones:
                    raise ValueError(f"Neighbor {neighbor} does not exist")

    def _check_blocked_zones(self):
        for zone_name, zone in self.config.graph.zones.items():
            if zone.z_type == ZoneType.BLOCKED:
                if self.config.graph.adjacency.get(zone_name):
                    raise ValueError(f"Blocked zone {zone_name} should have no outgoing connections")

    def _check_reachability(self):
        if not self._is_reachable(self.config.start_zone.name, self.config.goal_zone.name):
            raise ValueError("Goal unreachable from start")

    def _check_capacities(self):
        for (u, v), capacity in self.config.graph.capacities.items():
            if capacity < 1 or capacity > self.config.nb_drones:
                raise ValueError(f"Invalid capacity {capacity} for link {u}->{v}")

    # BFS simple pour vérifier accessibilité
    def _is_reachable(self, start, goal):
        visited = set()
        queue = [start]
        while queue:
            current = queue.pop(0)
            if current == goal:
                return True
            visited.add(current)
            for neighbor in self.config.graph.adjacency.get(current, []):
                if neighbor not in visited:
                    queue.append(neighbor)
        return False
