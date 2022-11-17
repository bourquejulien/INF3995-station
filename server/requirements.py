#!/usr/bin/env python
import os
import shutil

#######################
# Install dependencies
#######################
import pip

pip.main(["install", "-r", "requirements.txt"])

#######################
# Generate protos - Fix for protox implementation
#######################
import grpc_tools.protoc as protoc

out_folder = "out"
proto_folder = "protos"
protos = ["simulation", "compiler"]

if not os.path.exists(out_folder):
    os.mkdir(out_folder)


def build_proto(proto_name: str):
    protoc.main([f"-I{proto_folder}.", "--python_out=.", "--grpc_python_out=.",
                 os.path.join(proto_folder, f"{proto_name}.proto")])

    pb_file = f"{proto_name}_pb2.py"
    pb_grpc_file = f"{proto_name}_pb2_grpc.py"

    with open(os.path.join(proto_folder, pb_grpc_file), "r") as rf:
        with open(os.path.join(out_folder, pb_grpc_file), "w") as wf:
            while line := rf.readline():
                if f"from {proto_folder} import {proto_name}_pb2" in line:
                    line = f"import out.{proto_name}_pb2 as {proto_folder}_dot_{proto_name}__pb2"
                wf.write(line)

    shutil.move(os.path.join(proto_folder, pb_file), os.path.join(out_folder, pb_file))
    os.remove(os.path.join(proto_folder, pb_grpc_file))


for proto in protos:
    build_proto(proto)
