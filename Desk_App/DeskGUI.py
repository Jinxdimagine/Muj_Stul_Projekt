import tkinter as tk


class DeskGUI:
    def __init__(self,ws):
        # Create main window
        self.root = tk.Tk()
        self.root.title("Muj_Stul-Viet_Fusion")
        self.root.geometry("400x400")
        self.ws=ws
        self.list=[]
        # Add a label
        tk.Label(self.root, text="Hello, Desk App!").pack(pady=20)


    def add_reservation(self,data):
        self.list.append(data)

    # Run the Tkinter main loop
    def run(self):
        self.root.mainloop()
