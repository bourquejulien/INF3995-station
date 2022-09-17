from os import environ as env

config = {
    "argos_url": {
        "host": env.get("SIMULATION_ADDR") if env.get("SIMULATION_ADDR") is not None else "localhost",
        "port": 9854
    }
}
