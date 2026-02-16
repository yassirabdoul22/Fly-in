from typing import List, Optional
from src.models.graph import Graph
from src.models.zone import Zone, ZoneType
from .lexer import Token


class ParsedConfig:
    def __init__(self, graph: Graph, start_zone: Zone,
                 goal_zone: Zone, nb_drones: int):
        self.graph = graph
        self.start_zone = start_zone
        self.goal_zone = goal_zone
        self.nb_drones = nb_drones


class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.graph = Graph()
        self.start_zone: Optional[Zone] = None
        self.goal_zone: Optional[Zone] = None
        self.nb_drones: int = 0

    def parse(self) -> ParsedConfig:
        for token in self.tokens:

            if token.type == "nb_drones":
                self.nb_drones = token.value

            elif token.type in ("hub", "start_hub", "end_hub"):

                zone_type = ZoneType.NORMAL

                if "zone" in token.metadata:
                    if token.metadata["zone"] == "blocked":
                        zone_type = ZoneType.BLOCKED
                    elif token.metadata["zone"] == "restricted":
                        zone_type = ZoneType.RESTRICTED
                    elif token.metadata["zone"] == "priority":
                        zone_type = ZoneType.PRIORITY

                zone = Zone(
                    name=token.value,
                    x=token.x,
                    y=token.y,
                    z_type=zone_type
                )

                if "color" in token.metadata:
                    zone.color = token.metadata["color"]

                self.graph.add_zone(zone)

                if token.type == "start_hub":
                    self.start_zone = zone
                elif token.type == "end_hub":
                    self.goal_zone = zone

            elif token.type == "connection":
                zone1, zone2 = token.value
                self.graph.add_connection(zone1, zone2)

        # ---------------- VALIDATION ----------------
        if self.nb_drones <= 0:
            raise ValueError("nb_drones must be defined and > 0")

        if not self.start_zone:
            raise ValueError("start_hub not defined")

        if not self.goal_zone:
            raise ValueError("end_hub not defined")

        return ParsedConfig(
            graph=self.graph,
            start_zone=self.start_zone,
            goal_zone=self.goal_zone,
            nb_drones=self.nb_drones
        )
