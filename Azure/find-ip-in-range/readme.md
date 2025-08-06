# Azure Public IP Range Lookup

This Python script allows you to identify which Azure public IP address range a given IP address belongs to. It reads Azure's public IP address data from a JSON file and checks if the specified IP address falls within any of the advertised address prefixes.

## Features

- Reads Azure public IP ranges from a JSON file (e.g., `azure-public.json`).
- Checks if a provided IP address is contained within any Azure public IP ranges.
- Outputs the matching IP range and associated ID if found.


## Prerequisites

- Python 3.6 or higher.
- The `azure-public.json` file containing the Azure public IP ranges. (You can download this file from the [official Azure IP ranges service](https://www.microsoft.com/en-us/download/details.aspx?id=56519).)
- No external Python packages are needed beyond the standard library.


## Usage

1. Place your `azure-public.json` file in the same directory as this script or update the `json_file_path` variable with the correct path in the script.
2. Update the IP address to check in the script by modifying this line:

```python
ip_to_check = "xx.xx.xx.xx"
```

Replace `"xx.xx.xx.xx"` with the actual IP address you want to verify.
3. Run the script:

```bash
python check_azure_ip.py
```

4. The script will output whether the IP address belongs to any Azure public IP range, and if so, which range and its associated ID.

## How It Works

- The script loads the JSON data containing Azure public IP address ranges.
- It extracts all address prefixes and their corresponding IDs.
- Given an IP address, the script checks which Azure network (address prefix) it falls into using Python's built-in `ipaddress` module.
- It prints the matching range and ID or states that the IP is not in any Azure public IP range.


## Example Output

```
13.64.39.16 is in the range: 13.64.0.0/16, id: AzureCloud.westus
```

or

```
192.168.1.1 is not in any provided ranges.
```


## Notes

- Ensure the IP address format is valid (IPv4 or IPv6).
- The JSON file must follow the Azure public IP JSON schema, typically containing a `values` list with `id` and `properties.addressPrefixes`.
- You may want to automate updating the `azure-public.json` file regularly to have the latest IP ranges.


## License

This script is provided as-is under the MIT License. Use it freely and modify as needed.

