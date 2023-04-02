#!/bin/bash
rm -rf ../.env
rm -rf .env
docker-compose down
docker-compose rm -f
