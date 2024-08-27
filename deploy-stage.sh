#!/usr/bin/bash

set -e

sudo -v

sudo mkdir -p /var/www/test-debtor-api
sudo mkdir -p /var/www/test-debtor-api/staticfiles

docker build --tag test-debtor-api .

sudo docker compose up

sudo systemctl reload nginx.service

echo "Deploy complete"
