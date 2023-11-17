import random
import tkinter as tk


class View:
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("610x265")

        self.label1 = tk.Label(self.root, text="Enter the number of tasks", font=("Arial", 12))
        self.label1.place(x=10, y=10)

        self.entry1 = tk.Entry(self.root, font=("Arial", 12))
        self.entry1.place(x=10, y=40)

        self.label2 = tk.Label(self.root, text="Enter the number of tickets", font=("Arial", 12))
        self.label2.place(x=10, y=70)

        self.entry2 = tk.Entry(self.root, font=("Arial", 12))
        self.entry2.place(x=10, y=100)

        self.label3 = tk.Label(self.root, text="Enter the time quantum", font=("Arial", 12))
        self.label3.place(x=10, y=130)

        self.entry3 = tk.Entry(self.root, font=("Arial", 12))
        self.entry3.place(x=10, y=160)

        self.start_button = tk.Button(self.root, text="Start Simulation", font=("Arial", 12), command=self.start_simulation)
        self.start_button.place(x=10, y=190, width=190)

        self.stop_button = tk.Button(self.root, text="Stop Simulation", font=("Arial", 12), command=self.stop_simulation)
        self.stop_button.place(x=10, y=225, width=190)

        self.listbox1 = tk.Listbox(self.root, width=10, height=10)
        self.listbox1.place(x=210, y=10, width=190, height=245)

        self.listbox2 = tk.Listbox(self.root, width=10, height=10)
        self.listbox2.place(x=410, y=10, width=190, height=245)

        self.root.mainloop()

    def start_simulation(self):
        pass

    def stop_simulation(self):
        pass


#   6. «Выбор следующим самого короткого процесса»
# Обычно интерактивные процессы следуют схеме, при которой ожидается ввод команды, затем она выполняется, ожидается
# ввод следующей команды, затем выполняется эта команда, и т. д. Если выполнение каждой команды рассматривать как
# отдельное «задание», то можно минимизировать общее время отклика, запустив первой выполнение самой короткой команды.
# При реализации необходимо предусмотреть следующие функции:
#      выбор количества заданий в очереди (от 2 до 10);
#      запуск и остановка процесса выполнения;
#      выбор размера кванта времени выполнения;
#      назначение времени выполнения для каждого задания в случайном порядке;
#      расчёт самого короткого времени выполнения исходя из последнего времени выполнения заданий;


class Task:
    def __init__(self, id, time):
        self.id = id
        self.time = time


class SJN:
    def __init__(self, num_tasks):
        self.tasks = []
        for i in range(num_tasks):
            self.tasks.append(Task(i, random.randint(1, 100)))

    def schedule(self):
        self.tasks.sort(key=lambda x: x.time)
        for task in self.tasks:
            print(f"Task {task.id} is scheduled for {task.time} units")

    def shortest_job(self):
        return min(self.tasks, key=lambda x: x.time).id


#   8. Лотерейное планирование
# Основная идея состоит в раздаче процессам лотерейных билетов на доступ к различным системным ресурсам, в том числе
# и к процессорному времени.
# При реализации необходимо предусмотреть следующие функции:
#      выбор количества заданий в очереди (от 2 до 10);
#      запуск и остановка процесса выполнения;
#      выбор размера кванта времени выполнения;
#      назначение времени выполнения для каждого задания;
#      выбор количества лотерейных билетов для каждого задания;


def main():
    num_tasks = int(input("Enter the number of tasks: "))
    sjn = SJN(num_tasks)
    sjn.schedule()
    print(f"The shortest job is: {sjn.shortest_job()}")
