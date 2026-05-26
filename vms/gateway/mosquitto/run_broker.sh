#!/bin/bash
sudo ufw allow 1883/tcp
sudo docker run -d \
  --name broker \
  --restart unless-stopped \
  -v $PWD/mosquitto.conf:/mosquitto/config/mosquitto.conf \
  -p 1883:1883 \
  eclipse-mosquitto
echo "Mosquitto брокер запущен на порту 1883"
