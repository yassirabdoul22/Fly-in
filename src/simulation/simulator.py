from typing import List
from src.models.graph import Graph
from src.models.drone import Drone, DroneState


class Simulator:
    """
    Moteur de simulation pour faire avancer les drones tour par tour.
    """

    def __init__(self, graph: Graph, drones: List[Drone]):
        self.graph = graph
        self.drones = drones

    def tick(self):
        for drone in self.drones:
            if drone.is_at_destination(drone.goal):
                drone.state = DroneState.ARRIVED
                continue

            if drone.state == DroneState.IN_TRANSIT:
                drone.update_transit()
                continue

            next_zone = drone.next_zone

            if next_zone and self.graph.can_move(drone, next_zone.name):
                if drone.current_zone:
                    drone.current_zone.vacate(drone.drone_id)

                next_zone.occupy(drone.drone_id)
                drone.advance()
            else:
                if not drone.is_at_destination(drone.goal):
                    drone.state = DroneState.WAITING