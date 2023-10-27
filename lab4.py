import threading
import time
import tkinter
import random


NUM_PHILOSOPHERS = 5


class View:
    def __init__(self, root):
        self.root = root
        self.root.title('Dining philosophers', )
        self.root.geometry('500x350')
        self.root.resizable(False, False)

        self.canvas = tkinter.Canvas(self.root, width=500, height=350, bg='light grey')
        self.canvas.pack()

        self.label1 = tkinter.Label(self.root, text='Enter work time:', bg='light grey')
        self.label1.place(x=10, y=10)

        self.work_time = tkinter.Entry(self.root, width=10)
        self.work_time.place(x=10, y=30)

        self.label2 = tkinter.Label(self.root, text='Enter status time:', bg='light grey')
        self.label2.place(x=10, y=55)

        self.status_time = tkinter.Entry(self.root, width=10)
        self.status_time.place(x=10, y=75)

        self.start_button = tkinter.Button(self.root, text='Start', command=self.start)
        self.start_button.place(x=10, y=100)

        self.philosopher_label1 = tkinter.Label(self.root, text=f'Philosopher 1 - {0}', bg='light grey')
        self.philosopher_label1.place(x=10, y=140)

        self.philosopher_label2 = tkinter.Label(self.root, text=f'Philosopher 2 - {0}', bg='light grey')
        self.philosopher_label2.place(x=10, y=160)

        self.philosopher_label3 = tkinter.Label(self.root, text=f'Philosopher 3 - {0}', bg='light grey')
        self.philosopher_label3.place(x=10, y=180)

        self.philosopher_label4 = tkinter.Label(self.root, text=f'Philosopher 4 - {0}', bg='light grey')
        self.philosopher_label4.place(x=10, y=200)

        self.philosopher_label5 = tkinter.Label(self.root, text=f'Philosopher 5 - {0}', bg='light grey')
        self.philosopher_label5.place(x=10, y=220)

        self.status1 = self.canvas.create_oval(10, 260, 30, 280, fill='red')

        self.label3 = tkinter.Label(self.root, text='- thinking', bg='light grey')
        self.label3.place(x=35, y=259)

        self.status2 = self.canvas.create_oval(10, 290, 30, 310, fill='orange')

        self.label4 = tkinter.Label(self.root, text='- hungry', bg='light grey')
        self.label4.place(x=35, y=289)

        self.status3 = self.canvas.create_oval(10, 320, 30, 340, fill='green')

        self.label5 = tkinter.Label(self.root, text='- eating', bg='light grey')
        self.label5.place(x=35, y=319)

        self.circle1 = self.canvas.create_oval(250, 27, 350, 127, fill='white')
        self.circle2 = self.canvas.create_oval(345, 96, 445, 196, fill='white')
        self.circle3 = self.canvas.create_oval(308, 207, 408, 307, fill='white')
        self.circle4 = self.canvas.create_oval(191, 207, 291, 307, fill='white')
        self.circle5 = self.canvas.create_oval(154, 96, 254, 196, fill='white')

        self.root.mainloop()

    def update(self, name, status, count):
        if name == 1:
            self.canvas.itemconfig(self.circle1, fill=status)
            self.philosopher_label1.config(text=f'Philosopher 1 - {count}')
        elif name == 2:
            self.canvas.itemconfig(self.circle2, fill=status)
            self.philosopher_label2.config(text=f'Philosopher 2 - {count}')
        elif name == 3:
            self.canvas.itemconfig(self.circle3, fill=status)
            self.philosopher_label3.config(text=f'Philosopher 3 - {count}')
        elif name == 4:
            self.canvas.itemconfig(self.circle4, fill=status)
            self.philosopher_label4.config(text=f'Philosopher 4 - {count}')
        elif name == 5:
            self.canvas.itemconfig(self.circle5, fill=status)
            self.philosopher_label5.config(text=f'Philosopher 5 - {count}')

    def get_work_time(self):
        return int(self.work_time.get())

    def get_status_time(self):
        return int(self.status_time.get())

    def start(self):
        forks = [threading.Semaphore(1) for _ in range(NUM_PHILOSOPHERS)]
        philosophers = []

        for i in range(NUM_PHILOSOPHERS):
            right_fork = forks[i]
            left_fork = forks[(i + 1) % NUM_PHILOSOPHERS]
            philosopher = Philosopher(i + 1, right_fork, left_fork, self, 0)
            philosophers.append(philosopher)

        for philosopher in philosophers:
            philosopher_thread = threading.Thread(target=philosopher.dine)
            philosopher_thread.start()


class Philosopher:
    def __init__(self, name, right_fork, left_fork, view, count):
        self.name = name
        self.right_fork = right_fork
        self.left_fork = left_fork
        self.view = view
        self.count = count

    def eat(self):
        self.count += 1
        self.view.update(self.name, 'green', self.count)
        time.sleep(self.view.get_status_time())

    def think(self):
        self.view.update(self.name, 'red', self.count)
        time.sleep(self.view.get_status_time())

    def dine(self):
        start = time.time()
        while True:
            if time.time() - start >= self.view.get_work_time():
                break
            self.think()
            self.hungry()
        self.view.update(self.name, 'white', self.count)

    def hungry(self):
        self.view.update(self.name, 'orange', self.count)
        fork1, fork2 = self.left_fork, self.right_fork
        while True:
            fork1.acquire()
            locked = fork2.acquire(False)
            if locked:
                break
            fork1.release()
        self.eat()
        fork2.release()
        fork1.release()


def main():
    view = View(tkinter.Tk())
