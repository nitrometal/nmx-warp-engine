#!/bin/bash

JSON_FILE="nmx.net.universal.json"

SERVER_PRIV=$(docker run --rm alpine sh -c "apk add --no-cache wireguard-tools && wg genkey")
CLIENT_PRIV=$(docker run --rm alpine sh -c "apk add --no-cache wireguard-tools && wg genkey")
CLIENT_PUB=$(echo "$CLIENT_PRIV" | docker run --rm -i alpine sh -c "apk add --no-cache wireguard-tools && wg pubkey")
SERVER_PUB=$(echo "$SERVER_PRIV" | docker run --rm -i alpine sh -c "apk add --no-cache wireguard-tools && wg pubkey")

docker run -d \
  --name=amneziawg-server \
  --cap-add=NET_ADMIN \
  --device=/dev/net/tun \
  -e SERVER_PRIVATE_KEY="$SERVER_PRIV" \
  -e CLIENT_PUBLIC_KEY="$CLIENT_PUB" \
  -p 16666:16666/udp \
  --restart always \
  ghcr.io/amnezia-vpn/amneziawg-go-docker:latest

touch $JSON_FILE

cat <<EOF > .devcontainer/new_peer.tmp
  {
    "country": "us",
    "endpoint": "PENDING_HOST:16666",
    "peer": "${SERVER_PUB}",
    "priv": "${CLIENT_PRIV}"
  }
EOF

echo "===> OKAY"
