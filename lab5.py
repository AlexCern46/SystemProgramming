import random
from time import sleep
import tkinter as tk
import threading


flag = False


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("610x265")

        self.label1 = tk.Label(self.root, text="Enter the number of tasks", font=("Arial", 12))
        self.label1.place(x=10, y=10)

        self.task_count = tk.Entry(self.root, font=("Arial", 12))
        self.task_count.place(x=10, y=40)

        self.label2 = tk.Label(self.root, text="Enter the number of tickets", font=("Arial", 12))
        self.label2.place(x=10, y=70)

        self.tickets_count = tk.Entry(self.root, font=("Arial", 12))
        self.tickets_count.place(x=10, y=100)

        self.label3 = tk.Label(self.root, text="Enter the time quantum", font=("Arial", 12))
        self.label3.place(x=10, y=130)

        self.quantum = tk.Entry(self.root, font=("Arial", 12))
        self.quantum.place(x=10, y=160)

        self.start_button = tk.Button(self.root, text="Start", font=("Arial", 12), command=self.start_simulation)
        self.start_button.place(x=10, y=190, width=190)

        self.stop_button = tk.Button(self.root, text="Stop", font=("Arial", 12), command=self.stop_simulation)
        self.stop_button.place(x=10, y=225, width=190)

        self.label4 = tk.Label(self.root, text="STN", font=("Arial", 12))
        self.label4.place(x=210, y=10)

        self.listbox1 = tk.Listbox(self.root, width=10, height=10)
        self.listbox1.place(x=210, y=40, width=190, height=205)

        self.label5 = tk.Label(self.root, text="Tasks", font=("Arial", 12))
        self.label5.place(x=410, y=10)

        self.listbox2 = tk.Listbox(self.root, width=10, height=10)
        self.listbox2.place(x=410, y=40, width=190, height=205)

        self.root.mainloop()

    def start_simulation(self):
        global flag
        flag = True

        sjn = STN(int(self.task_count.get()), int(self.quantum.get()), self)
        lottery = Lottery(int(self.task_count.get()), int(self.quantum.get()), int(self.tickets_count.get()), self)

        thread1 = threading.Thread(target=sjn.start_task)
        thread2 = threading.Thread(target=lottery.start_task)

        thread1.start()
        thread2.start()


    def stop_simulation(self):
        global flag
        flag = False

    def update_listbox1(self, tasks, previous_exec_times):
        self.listbox1.delete(0, tk.END)
        for task in range(len(tasks)):
            s = f"Task {tasks[task].id}; time {tasks[task].time}; previous time {previous_exec_times[task]}"
            self.listbox1.insert(tk.END, s)

    def update_listbox2(self, tasks, tickets):
        self.listbox2.delete(0, tk.END)
        for task in tasks:
            count = 0
            for ticket in tickets:
                if ticket.task_id == task.id:
                    count += 1
            s = f"Task {task.id}; time {task.time}; tickets {count}"
            self.listbox2.insert(tk.END, s)


class Task:
    def __init__(self, id, time):
        self.id = id
        self.time = time

    def __str__(self):
        return f"Task {self.id}; time {self.time}"


class STN:
    def __init__(self, num_tasks, quantum, view):
        self.tasks = [Task(i, random.randint(3, 10)) for i in range(num_tasks)]
        self.quantum = quantum
        self.alpha = 0.5
        self.previous_exec_times = [task.time for task in self.tasks]
        self.view = view
        view.update_listbox1(self.tasks, self.previous_exec_times)

    def start_task(self):
        while flag and len(self.tasks) > 0:
            shortest_time = 15
            shortest_task = None
            i = None
            for time in range(len(self.previous_exec_times)):
                if self.previous_exec_times[time] < shortest_time:
                    i = time
                    shortest_time = self.previous_exec_times[time]
                    shortest_task = self.tasks[time]
            self.view.label4.config(text=f"Task {shortest_task.id} in progress")
            sleep(self.quantum)
            shortest_task.time -= self.quantum
            if shortest_task.time <= 0:
                del self.tasks[i]
                del self.previous_exec_times[i]
            else:
                self.update_previous_exec_time(i, shortest_time)
            self.view.update_listbox1(self.tasks, self.previous_exec_times)
        self.view.label4.config(text="No tasks")

    def update_previous_exec_time(self, task_id, time):
        self.previous_exec_times[task_id] = self.alpha * time + (1 - self.alpha) * (self.previous_exec_times[task_id] - self.quantum)


class Ticket:
    def __init__(self, id, task_id):
        self.id = id
        self.task_id = task_id


class Lottery:
    def __init__(self, num_tasks, quantum, num_tickets, view):
        self.tasks = [Task(i, random.randint(1, 10)) for i in range(num_tasks)]
        self.quantum = quantum
        self.tickets = [Ticket(i, random.choice(self.tasks).id) for i in range(num_tickets)]
        self.view = view
        view.update_listbox2(self.tasks, self.tickets)

    def start_task(self):
        while flag and len(self.tasks) > 0:
            if len(self.tickets) == 0:
                self.view.label5.config(text="No tickets")
                break
            else:
                ticket = random.choice(self.tickets)
                i = None
                for task in range(len(self.tasks)):
                    if self.tasks[task].id == ticket.task_id:
                        i = task
                        break
                task = self.tasks[i]
                self.view.label5.config(text=f"Task {task.id} in progress")
                sleep(self.quantum)
                task.time -= self.quantum
                if task.time <= 0:
                    del self.tasks[i]
                    self.update_tickets(ticket.task_id)
                self.view.update_listbox2(self.tasks, self.tickets)
        self.view.label5.config(text="No tasks")

    def update_tickets(self, task_id):
        while task_id in [ticket.task_id for ticket in self.tickets]:
            for ticket in self.tickets:
                if ticket.task_id == task_id:
                    self.tickets.remove(ticket)


def main():
    view = View()
