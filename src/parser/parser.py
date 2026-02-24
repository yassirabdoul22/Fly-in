# src/parser/parser.py
from typing import List, Optional
from src.models.graph import Graph
from src.models.zone import Zone, ZoneType
from .lexer import Token


class ParsedConfig:
    """Holds all data produced by the parser."""

    def __init__(
        self,
        graph: Graph,
        start_zone: Zone,
        goal_zone: Zone,
        nb_drones: int,
    ) -> None:
        """
        Initialize ParsedConfig.

        Args:
            graph: The zone/connection graph.
            start_zone: The starting zone.
            goal_zone: The goal zone.
            nb_drones: Number of drones to simulate.
        """
        self.graph = graph
        self.start_zone = start_zone
        self.goal_zone = goal_zone
        self.nb_drones = nb_drones


class Parser:
    """Parse a list of Tokens into a ParsedConfig."""

    def __init__(self, tokens: List[Token]) -> None:
        """
        Initialize the Parser.

        Args:
            tokens: Token list produced by the Lexer.
        """
        self.tokens = tokens
        self.graph = Graph()
        self.start_zone: Optional[Zone] = None
        self.goal_zone: Optional[Zone] = None
        self.nb_drones: int = 0

    def parse(self) -> ParsedConfig:
        """
        Parse all tokens and return a ParsedConfig.

        Returns:
            A fully populated ParsedConfig instance.

        Raises:
            ValueError: When mandatory fields are missing or invalid.
        """
        for token in self.tokens:
            if token.type == "nb_drones":
                self.nb_drones = token.value

            elif token.type in ("hub", "start_hub", "end_hub"):
                zone_type = ZoneType.NORMAL
                if "zone" in token.metadata:
                    zt = token.metadata["zone"]
                    if zt == "blocked":
                        zone_type = ZoneType.BLOCKED
                    elif zt == "restricted":
                        zone_type = ZoneType.RESTRICTED
                    elif zt == "priority":
                        zone_type = ZoneType.PRIORITY

                zone = Zone(
                    name=token.value,
                    x=token.x,
                    y=token.y,
                    z_type=zone_type,
                    capacity=int(token.metadata.get("max_drones", 1)),
                    color=token.metadata.get("color"),
                )
                self.graph.add_zone(zone)

                if token.type == "start_hub":
                    self.start_zone = zone
                elif token.type == "end_hub":
                    self.goal_zone = zone

            elif token.type == "connection":
                zone1, zone2 = token.value
                self.graph.add_connection(zone1, zone2)

        if self.nb_drones <= 0:
            raise ValueError("nb_drones must be > 0")
        if not self.start_zone or not self.goal_zone:
            raise ValueError("start_hub and end_hub must be defined")

        return ParsedConfig(
            graph=self.graph,
            start_zone=self.start_zone,
            goal_zone=self.goal_zone,
            nb_drones=self.nb_drones,
        )