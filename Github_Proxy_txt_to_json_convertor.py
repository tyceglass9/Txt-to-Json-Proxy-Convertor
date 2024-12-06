import json
import os
import requests
from datetime import datetime

def convert_proxies_to_json(proxy_file):
    proxies = []

    # Open txt file and read each line
    with open(proxy_file, 'r') as file:
        for line in file.readlines():
            # Strip any leading/trailing whitespace
            proxy = line.strip()

            # Check if line is not empty
            if line:
                # Split the IP and port by colon
                proxy_parts = line.split(':')
                ip = proxy_parts[0]
                port = proxy_parts[1]

                # Add to the list as a dictionary
                proxies.append(proxy)

    return proxies

def save_proxies_to_json(proxies, json_file):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(json_file), exist_ok=True)
    print(f"\033[97mDirectory exists: {os.path.dirname(json_file)}")  # Confirm directory creation

    # Save proxies to a JSON file
    try:
        with open(json_file, 'w') as json_out:
            json.dump(proxies, json_out, indent=4) #Write a JSON file with indentation
            print(f"\033[97mProxies have been successfully saved to {json_file}")
    except Exception as e:
        print(f"\033[91mAn error occured: {e}\033[91m")

def check_proxy_validity(proxy):
    try:
        api_url = f"https://api.proxyscrape.com/?request=checkproxy&proxy={proxy}&key=YourAPIKeyHere"

        # Send request to the ProxyScape's API
        response = requests.get(api_url)

        # Check if the response status code indicates success
        if response.status_code == 200:
            if response.text.strip() == "online":
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(f"Error checking proxy {proxy}: {e}")
    return False

def main():
    # Predefined paths
    output_folder = "Results" # Output folder in the 'Results' subfolder
    # Add date and time to output filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    json_file = os.path.join(output_folder, f"proxies_{timestamp}.json")  # JSON output file

    # Check where the script is running
    print("\033[97mCurrent working directory:", os.getcwd())

    # Ask user to specify the txt file
    proxy_file = input("\033[97mWhat is the path of your txt file?")

    # Remove quotes if present
    proxy_file = proxy_file.strip('"')

    # Initialize a list to store valid proxies
    valid_proxies = []

    # Check if the file exists and is a valid file
    try:
        proxies = convert_proxies_to_json(proxy_file)
        
        # Check validity of proxies before saving to JSON
        
        for proxy in proxies:
            print(f"\033[97mChecking proxy: {proxy}")

            if check_proxy_validity(proxy):
                # Print the proxy in green if valid
                print(f"\033[92mValid proxy: {proxy}\033[97m")
                valid_proxies.append({"proxy": proxy})
            else:
                # Print the proxy in red if invalid
                print(f"\033[91mInvalid proxy: {proxy}\033[97m")

        save_proxies_to_json(valid_proxies, json_file)
        print(f"\033[97mProxies from {proxy_file} have been successfully converted to proxies.json.")
    except Exception as e:
        print(f"\033[91mAn error occured: {e}\033[91m")

if __name__ == '__main__':
    main()