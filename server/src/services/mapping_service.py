from src.clients.abstract_swarm_client import AbstractSwarmClient


class MappingService:

    def __init__(self, swarm_client: AbstractSwarmClient):
        swarm_client.add_callback("mapping", self._add)

    def _add(self, uri, data):
        # TODO Ajouter le point à l'ensemble
        # Il faudrait surrement faire une genre de carte ou on ajoute des points
        ...

    def flush(self):
        # TODO
        ...
