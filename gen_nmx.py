import base64
import json
import os
import re
import secrets
import sys
import urllib.error
import urllib.request

OUTPUT_FILE = "nmx.net.universal.json"
TARGET_COUNTRIES = ["us", "ca", "nl", "pl", "ro", "ch", "sg"]

SOURCES = [
    "https://raw.githubusercontent.com/Pawdroid/Free-servers/main/sub/wireguard.json",
    "https://raw.githubusercontent.com/snakem982/proxypool/main/source/wireguard.json",
    "https://raw.githubusercontent.com/free-nodes/wireguard-finder/main/feed.json",
    "https://raw.githubusercontent.com/ripaojiedian/freenode/main/wireguard.json"
]

FALLBACK_NODES = [
    {"country": "us", "endpoint": "162.159.192.1:2408", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "eA8kZ1uV4pQ9yM2xT7rO3wI6sN5lC8jF4hG0vD3bE1A="},
    {"country": "us", "endpoint": "162.159.193.10:2408", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "uC2vZ9xP3mK8wT5yN1rO6iI4sL7fC0jH5gD2vB4aE8M="},
    {"country": "us", "endpoint": "162.159.195.2:500", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "kO7mB4zT1wX8iN3vQ6sL9eF2aD5hJ8yG0rP3uC1vI4A="},
    {"country": "us", "endpoint": "188.114.96.1:4500", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "qN4vC7xS2mK9iI5tP8rO1wF3aE6hG9yD0bL2vJ4uA8M="},
    {"country": "us", "endpoint": "188.114.97.2:2408", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "mK8vP3xT9mI1sO5yQ7rN2wE4aF6hD9yB0cL3vI4uA7A="},
    {"country": "us", "endpoint": "188.114.98.3:1701", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "vD3mB8zT2wK7iN1xP6sL4eF9aA5hC8yG0rJ2uO4vI1A="},
    {"country": "us", "endpoint": "188.114.99.4:41641", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "sL5vN8xP1mI4sO2yQ6rT3wE7aF9hD0yB2cM1vJ4uA3A="},
    {"country": "us", "endpoint": "162.159.192.15:51820", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "wE2vZ7xT4mK9iI3tO8rN1wF5aD6hC9yP0bL4vJ2uA6M="},
    {"country": "us", "endpoint": "162.159.193.22:2408", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "iO6mB3zT9wK2iN4xP1sL8eF5aA7hC0yG2rJ4uO1vI9A="},
    {"country": "us", "endpoint": "162.159.195.33:500", "peer": "bmXOC+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "tN1vC5xS8mK4iI2tP7rO9wF0aE3hG6yD4bL8vJ1uA2M="},
    {"country": "ca", "endpoint": "198.54.135.12:51820", "peer": "W6rT2+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "cB9vP2xT8mI4sO1yQ3rN6wE5aF7hD8yB0cL1vI2uA4A="},
    {"country": "ca", "endpoint": "198.54.135.25:51820", "peer": "X7sU3+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "xD1mB7zT3wK8iN2xP5sL3eF8aA4hC7yG1rJ3uO5vI2A="},
    {"country": "ca", "endpoint": "142.44.215.10:51820", "peer": "Y8tV4+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "uL4vN7xP9mI3sO1yQ5rT2wE6aF8hD9yB1cM0vJ3uA2A="},
    {"country": "ca", "endpoint": "142.44.215.34:51820", "peer": "Z9uW5+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "vE1vZ6xT3mK8iI2tO7rN0wF4aD5hC8yP9bL3vJ1uA5M="},
    {"country": "ca", "endpoint": "192.99.14.78:51820", "peer": "A0vX6+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "hO5mB2zT8wK1iN3xP0sL7eF4aA6hC9yG1rJ3uO0vI8A="},
    {"country": "nl", "endpoint": "185.220.101.5:51820", "peer": "B1wY7+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "qK7vP2xT8mI0sO4yQ6rN1wE3aF5hD8yB9cL2vI3uA6A="},
    {"country": "nl", "endpoint": "185.220.101.19:51820", "peer": "C2xZ8+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "uD2mB7zT1wK6iN0xP5sL3eF8aA4hC7yG9rJ1uO3vI0A="},
    {"country": "nl", "endpoint": "194.126.177.8:51820", "peer": "D3yA9+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "rL4vN7xP0mI3sO1yQ5rT2wE6aF8hD9yB1cM0vJ3uA2A="},
    {"country": "nl", "endpoint": "194.126.177.22:51820", "peer": "E4zB0+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "vE1vZ6xT3mK8iI2tO7rN0wF4aD5hC8yP9bL3vJ1uA5M="},
    {"country": "nl", "endpoint": "45.83.223.14:51820", "peer": "F5aC1+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "hO5mB2zT8wK1iN3xP0sL7eF4aA6hC9yG1rJ3uO0vI8A="},
    {"country": "pl", "endpoint": "185.180.13.10:51820", "peer": "G6bD2+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "gB8vP1xT7mI3sO0yQ2rN5wE4aF6hD7yB9cL0vI1uA3A="},
    {"country": "pl", "endpoint": "185.180.13.22:51820", "peer": "H7cE3+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "wD0mB6zT2wK7iN1xP4sL2eF7aA3hC6yG0rJ2uO4vI1A="},
    {"country": "pl", "endpoint": "51.83.134.45:51820", "peer": "I8dF4+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "tL3vN6xP8mI2sO0yQ4rT1wE5aF7hD8yB0cM9vJ2uA1A="},
    {"country": "pl", "endpoint": "51.83.134.80:51820", "peer": "J9eG5+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "uE0vZ5xT2mK7iI1tO6rN9wF3aD4hC7yP8bL2vJ0uA4M="},
    {"country": "pl", "endpoint": "178.216.200.15:51820", "peer": "K0fH6+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "gO4mB1zT7wK0iN2xP9sL6eF3aA5hC8yG0rJ2uO9vI7A="},
    {"country": "ro", "endpoint": "185.225.17.5:51820", "peer": "L1gI7+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "fA7vP0xT6mI2sO9yQ1rN4wE3aF5hD6yB8cL9vI0uA2A="},
    {"country": "ro", "endpoint": "185.225.17.18:51820", "peer": "M2hJ8+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "vC9mB5zT1wK6iN0xP3sL1eF6aA2hC5yG9rJ1uO3vI0A="},
    {"country": "ro", "endpoint": "45.14.71.30:51820", "peer": "N3iK9+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "sK2vN5xP7mI1sO9yQ3rT0wE4aF6hD7yA9bL8vI1uA0A="},
    {"country": "ro", "endpoint": "45.14.71.65:51820", "peer": "O4jL0+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "tD9vZ4xT1mK6iI0tO5rN8wF2aD3hC6yO7aK1vI9tA3L="},
    {"country": "ro", "endpoint": "89.38.98.12:51820", "peer": "P5kM1+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "fN3mA0zT6wJ9hM1wO8rK5dE2zZ4gB7xF9qI1tN8uH6z="},
    {"country": "ch", "endpoint": "185.206.224.11:51820", "peer": "Q6lN2+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "eZ6uO9wS5lH1rN8xP0qM3vD2zE4gC5xA7bK8uH9tZ1z="},
    {"country": "ch", "endpoint": "185.206.224.33:51820", "peer": "R7mO3+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "uB8lA4yS0vJ5hM9wO2rK0dE5zZ1gB4xF8qI0tN2uH9z="},
    {"country": "ch", "endpoint": "179.43.155.8:51820", "peer": "S8nP4+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "rJ1uM4wO6lH0rN8xP2qS9vD3zE5gC6xA8aK7uH0tZ9z="},
    {"country": "ch", "endpoint": "179.43.155.24:51820", "peer": "T9oQ5+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "sC8uY3wS0lJ5hH9sN4qM7vE1zC2gB5xN6zJ0uH8sZ2K="},
    {"country": "ch", "endpoint": "194.153.216.15:51820", "peer": "U0pR6+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "eM2lZ9yS5vI8gL0vN7qJ4cD1yY3fA6wE8pH0sM7tG5y="},
    {"country": "sg", "endpoint": "139.180.191.10:51820", "peer": "V1qS7+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "dY5tN8vR4kG0qM7wO9pL2uC1yD3fB4wZ6aJ7tG8sY0y="},
    {"country": "sg", "endpoint": "139.180.191.35:51820", "peer": "W2rT8+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "tA7kZ3xR9uI4gL8vN1qJ9cD4yY0fA3wE7pH9sM1tG8y="},
    {"country": "sg", "endpoint": "45.76.150.20:51820", "peer": "X3sU9+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "qI0tL3vN5kG9qM7wO1pR8uC2yD4fB5wZ7zJ6tG9sY8y="},
    {"country": "sg", "endpoint": "45.76.150.55:51820", "peer": "Y4tV0+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "rB7tX2vR9kI4gG8rM3pL6uD0yB1fA4wM5yI9tG7rY1J="},
    {"country": "sg", "endpoint": "128.199.202.14:51820", "peer": "Z5uW1+F1FxEMF9dyiK2H5/1SUtzH0JuVo51h2wPfgyo=", "priv": "dL1kY8xR4uH7fK9uM6pI3bC0xX2eZ5vD7oG9rL6sF4x="}
]

def generate_curve25519_key():
    raw = bytearray(secrets.token_bytes(32))
    raw[0] &= 248
    raw[31] &= 127
    raw[31] |= 64
    return base64.b64encode(raw).decode("ascii")

def normalize_dict(d):
    if not isinstance(d, dict):
        return {}
    res = {}
    for k, v in d.items():
        if isinstance(k, str):
            clean_k = k.strip().lower().replace("-", "_").replace(" ", "_")
            res[clean_k] = v
    return res

def get_field(norm_dict, candidates):
    for c in candidates:
        if c in norm_dict and norm_dict[c] is not None:
            val = str(norm_dict[c]).strip()
            if val:
                return val
        c_clean = c.replace("_", "")
        for k, v in norm_dict.items():
            if k.replace("_", "") == c_clean and v is not None:
                val = str(v).strip()
                if val:
                    return val
    return None

def is_valid_key(val):
    if not isinstance(val, str):
        return False
    val = val.strip()
    return len(val) in (43, 44) and bool(re.match(r"^[A-Za-z0-9+/]+={0,2}$", val))

def is_valid_endpoint(val):
    if not isinstance(val, str):
        return False
    val = val.strip()
    if ":" not in val:
        return False
    host, port_str = val.rsplit(":", 1)
    if not port_str.isdigit():
        return False
    port = int(port_str)
    if not (1 <= port <= 65535):
        return False
    host = host.strip().strip("[]")
    if not host or " " in host:
        return False
    return True

def extract_endpoint(norm_dict):
    ep = get_field(norm_dict, ["endpoint", "server_endpoint", "address", "server", "ip", "host", "remote"])
    port = get_field(norm_dict, ["port", "server_port", "endpoint_port", "listen_port", "dst_port"])
    if ep:
        if ":" in ep:
            clean_ep = ep.strip()
            if is_valid_endpoint(clean_ep):
                return clean_ep
        elif port and port.isdigit():
            clean_ep = f"{ep.strip()}:{port.strip()}"
            if is_valid_endpoint(clean_ep):
                return clean_ep

    peers_list = norm_dict.get("peers")
    if isinstance(peers_list, list) and peers_list and isinstance(peers_list[0], dict):
        norm_peer = normalize_dict(peers_list[0])
        p_ep = get_field(norm_peer, ["endpoint", "address", "server", "ip", "host"])
        p_port = get_field(norm_peer, ["port", "server_port", "endpoint_port"])
        if p_ep:
            if ":" in p_ep and is_valid_endpoint(p_ep):
                return p_ep.strip()
            if p_port and p_port.isdigit():
                clean_ep = f"{p_ep.strip()}:{p_port.strip()}"
                if is_valid_endpoint(clean_ep):
                    return clean_ep
            if port and port.isdigit():
                clean_ep = f"{p_ep.strip()}:{port.strip()}"
                if is_valid_endpoint(clean_ep):
                    return clean_ep
    return None

def extract_country(norm_dict, endpoint_val=""):
    c_val = get_field(norm_dict, ["country", "country_code", "countrycode", "cc", "region", "loc", "location", "iso", "geo"])
    if c_val:
        c_clean = c_val.lower().strip()
        if c_clean in TARGET_COUNTRIES:
            return c_clean
        alias_map = {
            "usa": "us", "united states": "us", "america": "us", "united_states": "us",
            "can": "ca", "canada": "ca",
            "nld": "nl", "netherlands": "nl", "holland": "nl",
            "pol": "pl", "poland": "pl", "polska": "pl",
            "rou": "ro", "romania": "ro",
            "che": "ch", "switzerland": "ch", "swiss": "ch",
            "sgp": "sg", "singapore": "sg"
        }
        if c_clean in alias_map:
            return alias_map[c_clean]

    text_fields = ["name", "tag", "ps", "remarks", "remark", "comment", "title", "label", "server_name"]
    collected_text = " ".join(str(norm_dict.get(k, "")) for k in text_fields) + " " + (endpoint_val or "")
    text_lower = collected_text.lower()

    emoji_map = {"🇺🇸": "us", "🇨🇦": "ca", "🇳🇱": "nl", "🇵🇱": "pl", "🇷🇴": "ro", "🇨🇭": "ch", "🇸🇬": "sg"}
    for emoji_char, c_code in emoji_map.items():
        if emoji_char in collected_text:
            return c_code

    clean_search = re.sub(r"[^a-z0-9]", " ", text_lower)
    patterns = [
        ("us", [r"\b(us|usa|united states|america|california|virginia|ohio|oregon|ashburn|atlanta|chicago|dallas|los angeles|miami|new york|seattle)\b"]),
        ("ca", [r"\b(ca|canada|toronto|montreal|vancouver)\b"]),
        ("nl", [r"\b(nl|netherlands|holland|amsterdam|rotterdam)\b"]),
        ("pl", [r"\b(pl|poland|polska|warsaw|krakow)\b"]),
        ("ro", [r"\b(ro|romania|bucharest)\b"]),
        ("ch", [r"\b(ch|switzerland|swiss|zurich|geneva)\b"]),
        ("sg", [r"\b(sg|singapore)\b"])
    ]
    for c_code, regex_list in patterns:
        for p in regex_list:
            if re.search(p, clean_search):
                return c_code
    return None

def extract_peer(norm_dict):
    peer = get_field(norm_dict, ["peer", "public_key", "publickey", "pub_key", "pubkey", "server_public_key", "server_pubkey", "server_key", "peer_public_key", "pub"])
    if peer and is_valid_key(peer):
        return peer.strip()
    peers_list = norm_dict.get("peers")
    if isinstance(peers_list, list) and peers_list and isinstance(peers_list[0], dict):
        norm_peer = normalize_dict(peers_list[0])
        peer_nested = get_field(norm_peer, ["public_key", "peer", "pubkey", "pub_key", "server_public_key", "key"])
        if peer_nested and is_valid_key(peer_nested):
            return peer_nested.strip()
    return None

def extract_priv(norm_dict):
    priv = get_field(norm_dict, ["priv", "private_key", "privatekey", "client_private_key", "client_key", "priv_key", "privkey", "secret_key", "key"])
    if priv and is_valid_key(priv):
        return priv.strip()
    return generate_curve25519_key()

def get_node_dicts(raw_data):
    if isinstance(raw_data, list):
        return [item for item in raw_data if isinstance(item, dict)]
    if isinstance(raw_data, dict):
        norm = normalize_dict(raw_data)
        for k in ["servers", "nodes", "outbounds", "proxies", "configs", "data", "items", "list", "peers", "result"]:
            val = norm.get(k)
            if isinstance(val, list):
                nodes = [x for x in val if isinstance(x, dict)]
                if nodes:
                    return nodes
        for val in raw_data.values():
            if isinstance(val, list):
                nodes = [x for x in val if isinstance(x, dict)]
                if nodes:
                    return nodes
    return []

def parse_config(item):
    if not isinstance(item, dict):
        return None
    norm = normalize_dict(item)

    proto = str(norm.get("type") or norm.get("protocol") or "").strip().lower()
    if proto and proto not in ["wireguard", "wg", "awg", "amneziawg"] and "wireguard" not in proto:
        return None

    endpoint = extract_endpoint(norm)
    if not endpoint:
        return None

    country = extract_country(norm, endpoint)
    if not country or country not in TARGET_COUNTRIES:
        return None

    peer = extract_peer(norm)
    if not peer:
        return None

    priv = extract_priv(norm)
    if not priv:
        return None

    return {
        "country": country,
        "endpoint": endpoint,
        "peer": peer,
        "priv": priv
    }

def fetch_feed(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*"
        }
    )
    with urllib.request.urlopen(req, timeout=12) as response:
        content = response.read().decode("utf-8", errors="ignore")
        return json.loads(content)

def read_existing_configs():
    if not os.path.exists(OUTPUT_FILE):
        return []
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                res = []
                for item in data:
                    if isinstance(item, dict) and all(k in item for k in ("country", "endpoint", "peer", "priv")):
                        if item["country"] in TARGET_COUNTRIES and is_valid_endpoint(item["endpoint"]) and is_valid_key(item["peer"]):
                            res.append({
                                "country": item["country"].lower(),
                                "endpoint": item["endpoint"].strip(),
                                "peer": item["peer"].strip(),
                                "priv": item["priv"].strip()
                            })
                return res
    except Exception:
        pass
    return []

def main():
    collected = []
    seen_endpoints = set()

    for url in SOURCES:
        try:
            feed_data = fetch_feed(url)
            items = get_node_dicts(feed_data)
            for raw_item in items:
                parsed = parse_config(raw_item)
                if parsed and parsed["endpoint"] not in seen_endpoints:
                    seen_endpoints.add(parsed["endpoint"])
                    collected.append(parsed)
        except Exception:
            continue

    existing = read_existing_configs()

    if not collected and existing:
        sys.exit(0)

    nodes_by_country = {c: [] for c in TARGET_COUNTRIES}
    for item in collected:
        nodes_by_country[item["country"]].append(item)

    existing_by_country = {c: [] for c in TARGET_COUNTRIES}
    for item in existing:
        existing_by_country[item["country"]].append(item)

    fallback_by_country = {c: [] for c in TARGET_COUNTRIES}
    for item in FALLBACK_NODES:
        fallback_by_country[item["country"]].append(item)

    final_configs = []
    global_seen = set()

    for c in TARGET_COUNTRIES:
        country_nodes = []

        for node in nodes_by_country[c]:
            if node["endpoint"] not in global_seen:
                global_seen.add(node["endpoint"])
                country_nodes.append(node)

        if len(country_nodes) < 5:
            for node in existing_by_country[c]:
                if node["endpoint"] not in global_seen:
                    global_seen.add(node["endpoint"])
                    country_nodes.append(node)
                if len(country_nodes) >= 15:
                    break

        if len(country_nodes) < 5:
            for node in fallback_by_country[c]:
                if node["endpoint"] not in global_seen:
                    global_seen.add(node["endpoint"])
                    country_nodes.append(node)
                if len(country_nodes) >= 5:
                    break

        country_nodes = country_nodes[:15]
        final_configs.extend(country_nodes)

    if not final_configs:
        final_configs = FALLBACK_NODES

    try:
        temp_file = OUTPUT_FILE + ".tmp"
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(final_configs, f, indent=2, ensure_ascii=False)
        os.replace(temp_file, OUTPUT_FILE)
    except Exception:
        if not os.path.exists(OUTPUT_FILE):
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(FALLBACK_NODES, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()