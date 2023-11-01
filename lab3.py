import tkinter as tk
import threading
import time


running = False


def square(a):
    return a**2


def factor(a):
    if a == 1:
        return 1
    else:
        return a * factor(a - 1)


def get_ascii(symbol):
    return ord(symbol)


def get_symbol(symbol):
    return dir(ord(symbol) + 2)


def get_sound(a):
    return 'beep' * a


def num_to_x(string):
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    new_str = ''
    for i in string:
        if i in nums:
            new_str += 'x'
        else:
            new_str += i
    return new_str


def critical_region(process_id):
    if process_id == 0:
        time.sleep(2)
    else:
        time.sleep(2)


def noncritical_region(process_id):
    if process_id == 0:
        time.sleep(1)
    else:
        time.sleep(1)


class View:
    def __init__(self, process):
        self.root = tk.Tk()
        self.root.title(process.title)

        self.turn = 0
        self.process0_in_critical = False
        self.process1_in_critical = False

        self.process = process

        self.label_process0 = tk.Label(self.root, text="Process 0: Not in critical region")
        self.label_process1 = tk.Label(self.root, text="Process 1: Not in critical region")

        self.start_button = tk.Button(self.root, text="Start Simulation", command=self.start_simulation)
        self.stop_button = tk.Button(self.root, text="Stop Simulation", command=self.stop_simulation)

        self.label_process0.pack()
        self.label_process1.pack()
        self.start_button.pack()
        self.stop_button.pack()

    def start_simulation(self):
        global running
        running = True
        self.process.process0_thread.start()
        self.process.process1_thread.start()

    def stop_simulation(self):
        global running
        running = False

    def update_labels(self):
        self.label_process0.config(
            text=f"Process 0: {'In critical region' if self.process0_in_critical else 'Not in critical region'}")
        self.label_process1.config(
            text=f"Process 1: {'In critical region' if self.process1_in_critical else 'Not in critical region'}")

    def run(self):
        self.root.mainloop()


class StrictAlternation:
    def __init__(self):
        self.title = "Strict Alternation Algorithm Simulation"

        self.process0_thread = threading.Thread(target=self.process0)
        self.process1_thread = threading.Thread(target=self.process1)

        self.view = View(self)
        self.view.run()

    def process0(self):
        while running:
            while self.view.turn != 0:
                pass
            self.view.process0_in_critical = True
            self.view.update_labels()
            critical_region(0)
            self.view.turn = 1
            self.view.process0_in_critical = False
            self.view.update_labels()
            noncritical_region(0)

    def process1(self):
        while running:
            while self.view.turn != 1:
                pass
            self.view.process1_in_critical = True
            self.view.update_labels()
            critical_region(1)
            self.view.turn = 0
            self.view.process1_in_critical = False
            self.view.update_labels()
            noncritical_region(1)


class Peterson:
    def __init__(self):
        self.N = 2
        self.title = "Peterson Algorithm Simulation"

        self.turn = 0
        self.interested = [False for _ in range(self.N)]

        self.process0_thread = threading.Thread(target=self.process, args=(0,))
        self.process1_thread = threading.Thread(target=self.process, args=(1,))

        self.view = View(self)
        self.view.run()

    def process(self, process_id):
        while True:
            self.enter_region(process_id)
            if process_id == 0:
                self.view.process0_in_critical = True
            else:
                self.view.process1_in_critical = True
            self.view.update_labels()
            critical_region(process_id)
            self.leave_region(process_id)
            if process_id == 0:
                self.view.process0_in_critical = False
            else:
                self.view.process1_in_critical = False
            self.view.update_labels()
            noncritical_region(process_id)

    def enter_region(self, process):
        other = 1 - process
        self.interested[process] = True
        self.turn = process
        while self.turn == process and self.interested[other]:
            pass

    def leave_region(self, process):
        self.interested[process] = False


def main():
    # simulator = StrictAlternation()
    simulator = Peterson()
