import string
from customtkinter import *

class TrussSolver(CTk):
    def __init__(self):
        super().__init__()
        self.title("Truss Solver")
        self.geometry("500x500")
        self.start_button = CTkButton(self, text="START", command=self.truss_grid)
        self.start_button.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.click_count = 0
        self.joints_properties = {}  # Store node positions and labels

    def truss_grid(self):
        self.start_button.destroy()
        self.canvas = CTkCanvas(self, bg="white", width=500, height=300)
        # self.canvas.create_rectangle(0, 0, 500, 500, fill="white")
        for i in range(1, 26):
            self.canvas.create_line(0, i*20, 500, i*20)  # horizontal lines
            self.canvas.create_line(i*20, 0, i*20, 300)   # vertical lines
        self.canvas.place(relx=0.5, rely=0.3, anchor=CENTER)
        self.canvas.bind("<Button-1>", self.start_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)
        self.canvas.bind("<Button-2>", self.delete_node)
        self.canvas.bind("<Button-3>", self.add_node)

    def add_node(self, event):
        LETTERS = [each for each in string.ascii_uppercase]
        if 0 <= event.x <= 500 and 0 <= event.y <= 500:
            label = LETTERS[self.click_count]
            position_drawn = event.x, event.y
            if self.click_count == 0: position_properties = 0, 0
            else: position_properties = (position_drawn[0] - self.joints_properties[LETTERS[0]][0])//5, ((300-position_drawn[1]) - self.joints_properties[LETTERS[0]][1])//5
            self.canvas.create_oval(position_drawn[0]-5, position_drawn[1]-5, position_drawn[0]+5, position_drawn[1]+5, fill="blue", tags=label, width=1)
            self.canvas.create_text(position_drawn[0]+10, position_drawn[1]+10, text=label, tags=label)
            self.joints_properties[label] = position_properties
            print(position_properties)
            self.click_count += 1

    def delete_node(self, event):
        if 0 <= event.x <= 500 and 0 <= event.y <= 500:
            closest_items = self.canvas.find_closest(event.x, event.y)
            for item in closest_items:
                if self.canvas.type(item) == 'oval':
                    label = self.canvas.gettags(item)[0]
                    self.canvas.delete(label)
                    self.click_count -= 1

    def start_line(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def end_line(self, event):
        self.end_x = event.x
        self.end_y = event.y
        self.canvas.create_line(self.start_x, self.start_y, self.end_x, self.end_y, fill="red", width=3)

TrussSolver().mainloop()
