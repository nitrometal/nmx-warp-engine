import json
import requests

def fetch_universal_wireguard_servers():
    url = "https://githubusercontent.com"
    try:
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            return None
            
        raw_data = response.json()
        servers_list = []
        
        target_countries = ['us', 'ca', 'nl', 'pl', 'ro', 'ch', 'sg']
        
        for item in raw_data:
            country = item.get("country", "").lower()
            if country not in target_countries:
                continue
                
            endpoint = item.get("endpoint")
            peer = item.get("public_key") or item.get("peer")
            priv = item.get("private_key") or item.get("priv")
            
            if not endpoint or not peer or not priv:
                continue
                
            server_obj = {
                "country": country,
                "endpoint": endpoint,
                "peer": peer,
                "priv": priv
            }
            
            if server_obj not in servers_list:
                servers_list.append(server_obj)
                
        return servers_list
    except Exception:
        return None

def main():
    servers = fetch_universal_wireguard_servers()
    if not servers:
        return

    output_filename = "nmx.net.universal.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(servers, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
