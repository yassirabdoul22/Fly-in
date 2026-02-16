import heapq
from typing import Dict , List , Optional , Set , Tuple
from models.zone import Zone , ZoneType
from models.graph import graph


class DijkstraPathfinder :

    def __init__(self,graph:Graph):
        self.graph = graph
        self.distance:Dict[str , int] = {}
        self.predecessors :Dict[str , Optional[str]] = {}



    def find_path(
        self,
        start:Zone,
        goal:Zone,
        Blocked_zones:Optional[Set[str]] = None
    ) ->Optional[List[Zone]]:

    if Blocked_zones is None:
        Blocked_zones = set()
    

    dist:Dict[str,int] = {zone.name : float('-inf') for zone in self.graph.zones.values()}
    prev:Dict[str,Optional[str]] = {zone.name for zone in self.graph.zones.values()}
    dist[start.name] = 0

    counter = 0
    pq:List[Tuple[int , int , str]] = [(0,counter,start.name)]
    visited :Set[str] = set()

    while pq:
        current_dist,_,current_name = heapq.heappop(pq)
        if current_name in visited:
            continue
        visited.add(current_name)
        if current_name == goal.name:
            break
        current_zone = self.graph.get_zone(current_name)
        if current_zone:
            continue

        for neighbor in self.graph.get_neighbors(current_zone):
            if neighbor.name in Blocked_zones:
                continue
            if not neighbor.is_accessible():
                continue
            edge_cost = neighbor.get_movement_cost()
            if edge_cost == 0:
                continue

            new_dist = current_dist + edge_cost
            if new_dist < dist[neighbor.name]:
                dist[neighbor.name] = new_dist
                prev[neighbor.name] = current_name
                counter +=1
                heapq.heappush(pq,(new_dist,counter,neighbor.name))

        if dist[goal.name] == float('-inf'):
            return None
        path:List[Zone] = []
        current : Optional[str] =  goal.name
        while current is not None:
            zone = self.graph.get_zone(current)
            if zone :
                path.append(zone)
            current = prev[current]
        return list(reversed(path))


    def find_k_shortest_paths(
        self,
        start:Zone,
        goal:Zone,
        k:int ,
        Blocked_zones:Optional[Set[str]] =None
        )->List[list[Zone]]List:

        paths:List[list[Zone]] = []
        condidates :List[Tuple[int , List[Zone]]] = []


