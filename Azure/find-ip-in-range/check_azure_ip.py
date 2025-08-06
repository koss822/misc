import json
import ipaddress

# Function to find which range an IP address belongs to
def find_ip_range(ip_to_check, address_prefixes):
    ip = ipaddress.ip_address(ip_to_check)
    for prefixes_id, prefixes in address_prefixes:
        for prefix in prefixes:
            network = ipaddress.ip_network(prefix)
            if ip in network:
                return f"{ip_to_check} is in the range: {network}, id: {prefixes_id}"
    return f"{ip_to_check} is not in any provided ranges."

# Read JSON data from a file
def read_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Main execution
if __name__ == "__main__":
    # Specify the path to your JSON file
    json_file_path = 'azure-public.json'
    
    # Load JSON data
    data = read_json_file(json_file_path)

    # Extract address prefixes
    address_prefixes = []
    for prefixes in data['values']:
        address_prefixes.append((prefixes['id'], prefixes['properties']['addressPrefixes']))

    # Example IP address to check
    ip_to_check = "xx.xx.xx.xx"
    result = find_ip_range(ip_to_check, address_prefixes)
    print(result)