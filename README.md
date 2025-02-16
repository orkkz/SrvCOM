# ServerCOM

ServerCOM is a remote administration tool that consists of a **server**, an **admin panel**, and a **client**. The client connects to the server, allowing the admin to send commands remotely.

## Features
- Remote command execution
- Persistent client setup
- Communication between client and admin panel

## Installation
1. Install the required dependencies:
   ```sh
   python -m pip install -r requirements.txt
   ```
2. Edit `admin.py` and `client.py` to configure the URL of the server running `server.py`.
3. Use `compile.bat` to compile the client into an executable file.
4. Distribute the compiled client to the target machine.

## Usage
- Start the **server** by running:
  ```sh
  python server.py
  ```
- Launch the **admin panel**:
  ```sh
  python admin.py
  ```
- The **client** will connect automatically once executed on the target system.

## Disclaimer
This project is intended for educational and legal purposes only. The authors are not responsible for any misuse of this tool.

