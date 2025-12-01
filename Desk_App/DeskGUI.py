import tkinter as tk

class DeskGUI:
    def __init__(self, ws,dshandler):
        self.root = tk.Tk()
        self.root.title("Muj_Stul-Viet_Fusion")
        self.root.geometry("400x400")
        self.ws = ws
        self.list = []
        self.dshandler = dshandler

        tk.Label(self.root, text="Hello, Desk App!").pack(pady=20)
        tk.Label(self.root, text="Pending Reservations:").pack(pady=10)

        self.listbox = tk.Listbox(self.root, width=40, height=15)
        self.listbox.pack(pady=10)

        # Buttons
        tk.Button(self.root, text="Approve", command=self.approve).pack(side=tk.LEFT, padx=10)
        tk.Button(self.root, text="Deny", command=self.deny).pack(side=tk.RIGHT, padx=10)


        # On close
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_reservation(self, data):
        """
        Adds a reservation to the internal list and updates the Listbox.
        """
        if self.dshandler.check_reservation(data):
            def add():
                if data in self.list:
                    return
                # Ensure all required fields exist
                name = data.get('name', 'Unknown')
                surname = data.get('surname', '')
                people = data.get('people', 'N/A')
                date = data.get('date', 'N/A')
                time = data.get('time', 'N/A')

                # Build display string
                item_text = f"{name} {surname} - {people} people at {date} {time}"

                # Append the full data object to self.list
                self.list.append(data)
                # Add display string to listbox
                self.listbox.insert(tk.END, item_text)

            self.root.after(0, add)



    def approve(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        data_item = self.list[idx]  # Get the actual data dict
        self.listbox.delete(idx)
        self.list.pop(idx)
        self.dshandler.add_reservation(data_item,"approved")
        print("APPROVED:", data_item)
        self.ws.send_sync({"type": "decision", "status": "approved", "item": data_item})


    def deny(self):
        selection = self.listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        data_item = self.list[idx]  # Get the actual data dict
        self.listbox.delete(idx)
        self.list.pop(idx)
        self.dshandler.add_reservation(data_item,"denied")
        print("DENIED:", data_item)
        self.ws.send_sync({"type": "decision", "status": "denied", "item": data_item})

    def on_close(self):
        self.ws.stop()
        self.root.destroy()

    def run(self):
        self.root.mainloop()