import random
import tkinter


def power_of_two(number):
    power = 0
    while number > 1:
        number /= 2
        power += 1
    return power


class PageTableEntry:
    def __init__(self, virtual_page_num, present_bit, physical_page_num):
        self.virtual_page_num = virtual_page_num
        self.present_bit = present_bit
        self.physical_page_num = physical_page_num

    def __repr__(self):
        return f"Virtual page num: {self.virtual_page_num}, present bit: {self.present_bit}, physical page num: {self.physical_page_num}"


class MemoryManager:
    def __init__(self, page_size_kb, memory_size_kb):
        self.page_size = page_size_kb * 1024
        self.memory_size = memory_size_kb * 1024
        self.num_virtual_pages = 2**16 // self.page_size
        self.num_physical_pages = self.memory_size // self.page_size

        self.page_table = [PageTableEntry(i, 0, -1) for i in range(self.num_virtual_pages)]
        self.physical_memory = [-1] * self.num_physical_pages

    def allocate_memory(self, virtual_address):
        num_bits = power_of_two(self.num_virtual_pages)
        virtual_page_num = int(virtual_address[:num_bits], 2)

        if not self.page_table[virtual_page_num].present_bit:
            self._handle_page_fault(virtual_page_num)

        physical_page_num = self.page_table[virtual_page_num].physical_page_num
        physical_address = str(bin(physical_page_num)[2:].zfill(power_of_two(self.num_physical_pages))) + virtual_address[num_bits:]

        return physical_address

    def _handle_page_fault(self, virtual_page_num):
        if -1 in self.physical_memory:
            free_page_index = self.physical_memory.index(-1)
        else:
            free_page_index = random.randint(0, self.num_physical_pages - 1)

        for page in self.page_table:
            if page.physical_page_num == free_page_index:
                page.present_bit = 0
                page.physical_page_num = -1

        self.page_table[virtual_page_num].present_bit = 1
        self.page_table[virtual_page_num].physical_page_num = free_page_index
        self.physical_memory[free_page_index] = virtual_page_num


manager = MemoryManager(4, 32)


def start(page_size_kb, memory_size_kb, virtual_memory, physical_memory):
    virtual_memory.delete(0, tkinter.END)
    physical_memory.delete(0, tkinter.END)

    page_size_kb = int(page_size_kb.get())
    memory_size_kb = int(memory_size_kb.get())

    global manager
    manager = MemoryManager(page_size_kb, memory_size_kb)

    # Отображение виртуальной памяти
    for i in range(manager.num_virtual_pages):
        s = f"{i}: {i * page_size_kb} - {i * page_size_kb + page_size_kb} K"
        virtual_memory.insert(tkinter.END, s)

    # Отображение физической памяти
    for i in range(manager.num_physical_pages):
        s = f"{i}: {i * page_size_kb} - {i * page_size_kb + page_size_kb} K"
        physical_memory.insert(tkinter.END, s)


def allocate(virtual_address, page_table, answer):
    physical_address = manager.allocate_memory(str(virtual_address))
    answer.config(text=f"Answer: Virtual Address: {virtual_address} -> Physical Address: {physical_address}")

    with open("page_table.txt", "w") as file:
        file.write("Virtual page num    Present bit    Physical page num\n")
        for i in range(len(manager.page_table)):
            physical_page_num = manager.page_table[i].physical_page_num
            if physical_page_num == -1:
                physical_page_num = "None"
            file.write("{:<16}    {:<11}    {:<18}\n".format(i, manager.page_table[i].present_bit, physical_page_num))


    page_table.delete(0, tkinter.END)
    for i in manager.page_table:
        page_table.insert(tkinter.END, i)


def main():
    root = tkinter.Tk()
    root.title("Page Table")
    root.geometry("600x380")

    label = tkinter.Label(root, text=f"Enter page size (Kb):")
    label.place(x=10, y=10)

    page_size_kb = tkinter.Entry(root, width=10)
    page_size_kb.place(x=125, y=10)

    label = tkinter.Label(root, text=f"Enter memory size (Kb):")
    label.place(x=200, y=10)

    memory_size_kb = tkinter.Entry(root, width=10)
    memory_size_kb.place(x=335, y=10)

    button1 = tkinter.Button(root, text="Start", command=lambda: start(page_size_kb, memory_size_kb, virtual_memory, physical_memory))
    button1.place(x=410, y=10)

    label = tkinter.Label(root, text="Enter virtual address:")
    label.place(x=10, y=40)

    virtual_address = tkinter.Entry(root, width=10)
    virtual_address.place(x=125, y=40, width=100)

    button2 = tkinter.Button(root, text="Allocate", command=lambda: allocate(virtual_address.get(), page_table, answer))
    button2.place(x=230, y=40)

    label = tkinter.Label(root, text="Virtual memory")
    label.place(x=10, y=70)

    virtual_memory = tkinter.Listbox(root, width=15, height=15)
    virtual_memory.place(x=10, y=90, height=260)

    label = tkinter.Label(root, text="Physical memory")
    label.place(x=125, y=70)

    physical_memory = tkinter.Listbox(root, width=15, height=15)
    physical_memory.place(x=125, y=90, height=260)

    label = tkinter.Label(root, text="Page table")
    label.place(x=240, y=70)

    page_table = tkinter.Listbox(root, width=15, height=15)
    page_table.place(x=240, y=90, width=330, height=260)

    answer = tkinter.Label(root, text=f"Answer:")
    answer.place(x=10, y=350)

    root.mainloop()
