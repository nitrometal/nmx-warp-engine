import json
import requests
import base64

def fetch_free_wireguard_servers():
    url = "https://vpngate.net"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return None
        
        lines = response.text.split('\n')
        servers_list = []
        
        for line in lines:
            if line.startswith('*') or line.startswith('#') or not line.strip():
                continue
                
            parts = line.strip().split(',')
            if len(parts) < 14:
                continue
                
            country = parts[6].lower()
            config_base64 = parts[14]
            
            target_countries = ['us', 'ca', 'nl', 'pl', 'ro', 'ch', 'sg']
            if country not in target_countries:
                continue
                
            try:
                ip = parts[1]
                endpoint = f"{ip}:51820"
                
                server_obj = {
                    "country": country,
                    "endpoint": endpoint,
                    "peer": "APcJxf2UbdHXop3dZT3xBj1286WoIxIFSPBdSqCrVS4=",
                    "priv": "kO0yEGaY/1Za4hUV6nLADliMu8effv6k69/2qUxufF0="
                }
                
                if server_obj not in servers_list:
                    servers_list.append(server_obj)
                    
            except Exception:
                continue
                
        return servers_list
    except Exception:
        return None

def main():
    servers = fetch_free_wireguard_servers()
    if not servers:
        return

    output_filename = "nmx.net.universal.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(servers, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
