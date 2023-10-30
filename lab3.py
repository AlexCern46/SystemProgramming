import tkinter as tk
import threading
import time


class StrictAlternationSimulator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Strict Alternation Algorithm Simulation")

        self.turn = 0
        self.process0_in_critical = False
        self.process1_in_critical = False

        self.label_process0 = tk.Label(self.root, text="Process 0: Not in critical region")
        self.label_process0.pack()

        self.label_process1 = tk.Label(self.root, text="Process 1: Not in critical region")
        self.label_process1.pack()

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)
        self.stop_button.pack()

        self.process0_thread = threading.Thread(target=self.process0)
        self.process1_thread = threading.Thread(target=self.process1)

        self.running = False

    def start_simulation(self):
        self.running = True
        self.process0_thread.start()
        self.process1_thread.start()

    def stop_simulation(self):
        self.running = False

    def process0(self):
        while self.running:
            while self.turn != 0:
                pass
            self.process0_in_critical = True
            self.update_labels()
            self.critical_region(0)
            self.turn = 1
            self.process0_in_critical = False
            self.update_labels()
            self.noncritical_region(0)

    def process1(self):
        while self.running:
            while self.turn != 1:
                pass
            self.process1_in_critical = True
            self.update_labels()
            self.critical_region(1)
            self.turn = 0
            self.process1_in_critical = False
            self.update_labels()
            self.noncritical_region(1)

    def critical_region(self, process_id):
        if process_id == 0:
            time.sleep(2)
        else:
            time.sleep(2)

    def noncritical_region(self, process_id):
        if process_id == 0:
            time.sleep(1)
        else:
            time.sleep(1)

    def update_labels(self):
        self.label_process0.config(
            text=f"Process 0: {'In critical region' if self.process0_in_critical else 'Not in critical region'}")
        self.label_process1.config(
            text=f"Process 1: {'In critical region' if self.process1_in_critical else 'Not in critical region'}")

    def run(self):
        self.root.mainloop()


def main():
    simulator = StrictAlternationSimulator()
    simulator.run()
