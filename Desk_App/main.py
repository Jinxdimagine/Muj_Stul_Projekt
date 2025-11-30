from WebSocketClient import WebSocketClient
from DeskGUI import DeskGUI

def main():
    # Create WebSocket client
    ws_client = WebSocketClient("ws://localhost:3031")

    # Create GUI and pass WebSocket client
    gui = DeskGUI(ws_client)

    # Pass GUI callback to WebSocket so new reservations are added
    ws_client.on_message = lambda data: gui.add_reservation(data)

    # Start WebSocket in background
    ws_client.start()

    # Start GUI loop (blocking)
    gui.run()

if __name__ == "__main__":
   main()
