#!/bin/bash

protoc codebots.proto --python_out=. --java_out=java_viewer/src_protobuf

