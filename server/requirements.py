#!/bin/python3

#######################
# Install dependencies
#######################
import pip
import os

out_folder = "out"
pip.main(["install", "-r", "requirements.txt"])

#######################
# Generate protos
#######################
import grpc_tools.protoc as protoc

if not os.path.exists(out_folder):
    os.mkdir(out_folder)

protoc.main(["-Iprotos.", "--python_out=.", "--grpc_python_out=.", "protos/simulation.proto"])

newlines = []
with open("protos/simulation_pb2_grpc.py", 'r') as file:
    for line in file.readlines():
        if "from protos import simulation_pb2" in line:
            newlines.append("import out.simulation_pb2 as protos_dot_simulation__pb2")
            continue
        newlines.append(line)


with open("protos/simulation_pb2_grpc.py", 'w') as file:
    file.writelines(newlines)

os.replace("protos/simulation_pb2_grpc.py", f"{out_folder}/simulation_pb2_grpc.py")
os.replace("protos/simulation_pb2.py", f"{out_folder}/simulation_pb2.py")
