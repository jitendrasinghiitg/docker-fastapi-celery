#!/usr/bin/env bash
sudo docker-compose -f docker-compose.yml up --scale worker=2 --build
