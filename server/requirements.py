#!/bin/python3

#######################
# Install dependencies
#######################
import pip
import os

pip.main(["install", "-r", "requirements.txt"])

#######################
# Generate protos
#######################
import grpc_tools.protoc as protoc

out_folder = "out"
proto_folder = "protos"
protos = ["simulation", "compiler"]

if not os.path.exists(out_folder):
    os.mkdir(out_folder)


def build_proto(proto_name: str):
    protoc.main([f"-I{proto_folder}.", "--python_out=.", "--grpc_python_out=.", f"{proto_folder}/{proto_name}.proto"])

    newlines = []
    with open(f"{proto_folder}/{proto_name}_pb2_grpc.py", 'r') as file:
        for line in file.readlines():
            if f"from {proto_folder} import {proto_name}_pb2" in line:
                newlines.append(f"import out.{proto_name}_pb2 as {proto_folder}_dot_{proto_name}__pb2")
                continue
            newlines.append(line)

    with open(f"{proto_folder}/{proto_name}_pb2_grpc.py", 'w') as file:
        file.writelines(newlines)

    os.replace(f"{proto_folder}/{proto_name}_pb2_grpc.py", f"{out_folder}/{proto_name}_pb2_grpc.py")
    os.replace(f"{proto_folder}/{proto_name}_pb2.py", f"{out_folder}/{proto_name}_pb2.py")


for proto in protos:
    build_proto(proto)
