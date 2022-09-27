
class CommandService:
    
    def __init__(self):
        self.isSimulation = False

    def init_mission(self, request_data):
        self.isSimulation = request_data["isSimulation"]
        response = {
            "status": "success",
        }
        return response
    
    def identify(self, request_data):
        # command
        response = {
            "status": "success",
        }
        return response