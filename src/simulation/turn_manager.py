# turn_manager.py
from typing import List
from src.models.drone import Drone, DroneState
from src.simulation.simulator import Simulator
from src.routing.strategies.bfs import BFS
from src.models.zone import CapacityError

class TurnManager:
    """
    Gère les tours de simulation :
    - Recalcule le chemin si drone bloqué ou zone pleine
    - Fait avancer tous les drones
    """

    def __init__(self, drones: List[Drone], simulator: Simulator, bfs: BFS):
        self.drones = drones
        self.simulator = simulator
        self.bfs = bfs

    def run_turn(self):
        for drone in self.drones:
            # Si drone bloqué ou sans path, on tente de recalculer un chemin
            if drone.state in [DroneState.WAITING, DroneState.IDLE] or not drone.path:
                if hasattr(drone, 'goal') and drone.goal and drone.current_zone:
                    new_path = self.bfs.find_route(drone.current_zone, drone.goal)
                    if new_path:
                        drone.path = new_path
                        drone.path_index = 0
                        drone.state = DroneState.MOVING
                    else:
                        drone.state = DroneState.WAITING

            # Vérifier si le drone peut avancer vers la prochaine zone
            if drone.state == DroneState.MOVING and drone.next_zone:
                try:
                    # Tente d'occuper la prochaine zone
                    drone.next_zone.occupy(drone.drone_id)
                    # Libère la zone précédente
                    if drone.current_zone:
                        drone.current_zone.vacate(drone.drone_id)
                    drone.advance()
                except CapacityError:
                    # Zone pleine, reste en WAITING et recalculera au prochain tour
                    drone.state = DroneState.WAITING

        # Avance tous les drones d'un pas dans le simulateur
        self.simulator.tick()