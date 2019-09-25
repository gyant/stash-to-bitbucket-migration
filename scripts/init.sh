#!/bin/bash

mkdir -p $(pwd)/data/stash

make init-stash

docker-compose up -d