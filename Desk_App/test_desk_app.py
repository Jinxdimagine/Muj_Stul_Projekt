import unittest
from DeskGUI import DeskGUI

class DummyDsHandler:
    def __init__(self):
        self.calls = []

    def check_reservation(self, data):
        # Povolíme všechny rezervace
        return True

    def add_reservation(self, data, status):
        self.calls.append((data, status))


class DummyWebSocket:
    def __init__(self):
        self.sent = []

    def send_sync(self, data):
        self.sent.append(data)

    def stop(self):
        pass


class TestDeskGUI(unittest.TestCase):
    def setUp(self):
        # Mock WebSocket a DsHandler
        self.ws = DummyWebSocket()
        self.dshandler = DummyDsHandler()
        self.gui = DeskGUI(self.ws, self.dshandler)

    def test_add_reservation(self):
        data = {"name": "Alice", "surname": "Smith", "people": 4, "date":"2025-12-08", "time":"19:00"}
        self.gui.add_reservation(data)
        # Přidání do listboxu je asynchronní (root.after), proto zavoláme update
        self.gui.root.update()
        self.assertIn(data, self.gui.list)
        self.assertEqual(self.gui.listbox.size(), 1)

    def test_approve_reservation(self):
        data = {"name": "Bob", "surname": "Jones", "people": 2, "date":"2025-12-08", "time":"18:00"}
        self.gui.add_reservation(data)
        self.gui.root.update()

        # Simulujeme výběr první položky
        self.gui.listbox.selection_set(0)
        self.gui.approve()

        # Data by měla být odstraněna z listu a listboxu
        self.assertNotIn(data, self.gui.list)
        self.assertEqual(self.gui.listbox.size(), 0)

        # DsHandler měl být zavolán s "approved"
        self.assertIn((data, "approved"), self.dshandler.calls)

        # WebSocket měl odeslat zprávu
        self.assertEqual(len(self.ws.sent), 1)
        self.assertEqual(self.ws.sent[0]["status"], "approved")

    def test_deny_reservation(self):
        data = {"name": "Carol", "surname": "White", "people": 3, "date":"2025-12-08", "time":"20:00"}
        self.gui.add_reservation(data)
        self.gui.root.update()

        # Simulace výběru
        self.gui.listbox.selection_set(0)
        self.gui.deny()

        self.assertNotIn(data, self.gui.list)
        self.assertEqual(self.gui.listbox.size(), 0)
        self.assertIn((data, "denied"), self.dshandler.calls)
        self.assertEqual(len(self.ws.sent), 1)
        self.assertEqual(self.ws.sent[0]["status"], "denied")


if __name__ == "__main__":
    unittest.main()
