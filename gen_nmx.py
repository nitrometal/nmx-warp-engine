import json
import requests

def fetch_universal_wireguard_servers():
    url = "https://githubusercontent.com/anywlan/wireguard-finder/main/public_nodes.json"
    try:
        response = requests.get(url, timeout=20)
        if response.status_code != 200:
            return None
            
        raw_data = response.json()
        servers_list = []
        
        target_countries = ['us', 'ca', 'nl', 'pl', 'ro', 'ch', 'sg']
        
        for item in raw_data:
            country = str(item.get("country", item.get("Country", ""))).lower().strip()
            if country not in target_countries:
                continue
                
            endpoint = item.get("endpoint") or item.get("Endpoint")
            peer = item.get("public_key") or item.get("peer") or item.get("PublicKey") or item.get("public")
            priv = item.get("private_key") or item.get("priv") or item.get("PrivateKey") or item.get("private")
            
            if not endpoint or not peer or not priv:
                continue
                
            server_obj = {
                "country": country,
                "endpoint": str(endpoint).strip(),
                "peer": str(peer).strip(),
                "priv": str(priv).strip()
            }
            
            if server_obj not in servers_list:
                servers_list.append(server_obj)
                
        return servers_list if len(servers_list) > 0 else None
    except Exception:
        return None

def main():
    servers = fetch_universal_wireguard_servers()
    
    if not servers:
        servers = [
            {
                "country": "us",
                "endpoint": "149.102.242.94:51820",
                "peer": "fjmcron5ORLeZigl+fJ00PJGgR/2brhc/HjC5fHSGg4=",
                "priv": "OI3m2ltSE/bdxGRMvHgO8oN0rpwCR5Wx4nl2XJugTXg="
            }
        ]

    output_filename = "nmx.net.universal.json"
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(servers, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
