from WebSocketClient import WebSocketClient
from UI.main_window import DeskGUI
from dshandler import DsHandler
def main():
    dshandler=DsHandler()
    # Create WebSocket client
    ws_client = WebSocketClient("ws://localhost:3031")

    # Create GUI and pass WebSocket client
    gui = DeskGUI(ws_client)
    
    def handle_ws_message(data):
        if "name" in data and "people" in data:
            gui.add_reservation(data)
        else:
            print("Ignored non-reservation message:", data)
    # Pass GUI callback to WebSocket so new reservations are added
    ws_client.on_message = handle_ws_message
    # Start WebSocket in background
    ws_client.start()

    # Start GUI loop (blocking)
    gui.run()

if __name__ == "__main__":
   main()
