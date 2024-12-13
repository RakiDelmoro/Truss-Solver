import math
import operator
import numpy as np
from customtkinter import *
import matplotlib.pyplot as plt
from statistics import mean
from collections import Counter
import PIL.Image as Image
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class TrussSolver(CTk):
    def __init__(self):
        super().__init__()
        self.title("Truss Me!")
        self.geometry("400x300")
        self.description_container = CTkFrame(self, width=400, height=300, fg_color='black')
        self.description_container.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.text_1 = CTkLabel(self.description_container, text="Truss Me! ", font=("Arial", 20, "bold"), fg_color='black', text_color='white')
        self.text_1.place(relx=0.5, rely=0.1, anchor=CENTER)
        self.line_1 = CTkLabel(self.description_container, text="___________________________________________________", font=("Arial", 10), fg_color='black', text_color='deep sky blue')
        self.line_1.place(relx=0.5, rely=0.2, anchor=CENTER)
        self.text_2 = CTkLabel(self.description_container, text='A truss calculator using the method of joints solves for internal forces by analyzing equilibrium at each joint of the structure.', font=("Arial", 20), fg_color='black', text_color='white', wraplength=400)
        self.text_2.place(relx=0.5, rely=0.4, anchor=CENTER)
        self.line_2 = CTkLabel(self.description_container, text="___________________________________________________", font=("Arial", 10), fg_color='black', text_color='deep sky blue')
        self.line_2.place(relx=0.5, rely=0.6, anchor=CENTER)
        self.text_3 = CTkLabel(self.description_container, text='Jhanniah M. Pineda', font=("Arial", 20), fg_color='black', text_color='white', wraplength=400)
        self.text_3.place(relx=0.5, rely=0.7, anchor=CENTER)
        self.text_4 = CTkLabel(self.description_container, text='Stubcode:742', font=("Arial", 20), fg_color='black', text_color='white', wraplength=400)
        self.text_4.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.start_button = CTkButton(self, text="START", fg_color="deep sky blue", bg_color='deep sky blue', text_color='black', font=('Arial', 15, 'bold'), width=100, command=lambda: [self.start_button.destroy(), self.description_container.destroy(), self.truss_main_frame()])
        self.start_button.place(relx=0.5, rely=0.95, anchor=S)
        self.pair_elements = []
        self.joint_data = {}

    def restart(self):
        self.start_button.destroy()
        self.description_container.destroy()
        self.truss_main_frame()
        self.scrollable_table._parent_frame.destroy()
        self.data_table.destroy()
        self.pair_elements = []
        self.joint_data = {}

    def exit(self):
        self.quit()

    def truss_main_frame(self):
        self.geometry('500x500')
        self.bg_image = CTkImage(light_image=Image.open("Truss-Solver/background.jpg"), size=(500, 500))
        self.bg_label = CTkLabel(self, image=self.bg_image)
        self.bg_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.truss_elements()

        self.restart_button = CTkButton(self, text="RESTART", fg_color='black', width=50, font=('Arial', 15, 'bold'), command=self.restart)
        self.restart_button.place(relx=0.9, rely=0.98, anchor=S)
        self.exit_button = CTkButton(self, text="EXIT", fg_color='black', width=50, font=('Arial', 15, 'bold'), command=self.exit)
        self.exit_button.place(relx=0.065, rely=0.98, anchor=S)

    def truss_elements(self):
        # Create a scrollable frame
        self.elements_table_container = CTkScrollableFrame(self, width=200, height=300, fg_color='black', bg_color='black')
        self.elements_table_container.place(relx=0.5, rely=0.45, anchor=CENTER)
        # Create the internal frame for the data table
        self.elements_table = CTkFrame(self.elements_table_container, width=480)
        self.elements_table.pack(fill="both", expand=True)
        # Headers with row number column
        headers = ["#", "START", "END"]
        for col, header in enumerate(headers):
            header_label = CTkLabel(self.elements_table, text=header, font=("Arial", 15, "bold"))
            header_label.grid(row=0, column=col, padx=5, pady=5)
        self.table_elements = []
        for i in range(50):
            row_entries = []
            # Add row number label
            row_number_label = CTkLabel(self.elements_table, text=str(i+1))
            row_number_label.grid(row=i+1, column=0, padx=5, pady=5)
            for j in range(len(headers)-1):
                entry = CTkEntry(self.elements_table, width=60)
                entry.grid(row=i+1, column=j+1, padx=5, pady=5)
                row_entries.append(entry)    
            self.table_elements.append(row_entries)
        self.apply_elements = CTkButton(self, text="APPLY", font=("Arial", 15, "bold"), text_color='white', fg_color='black', command=self.check_joint_entry)
        self.apply_elements.place(relx=0.459, rely=0.95, anchor=CENTER)

    def check_joint_entry(self):
        input_elements = []
        for input_entries in self.table_elements:
            for entry in input_entries:
                if entry.get() == "": continue
                input_elements.extend(entry.get())
        if len(input_elements) == 0:
            messagebox.showerror("No input", "Error: Please specify joint start and end.")
            return
        for element in input_elements:
            if element.isdigit():
                messagebox.showerror("Input Error", "Error: Please enter only alphabetical values for joint labels.")
                return
        self.apply_elements.destroy()
        self.gather_pair_truss_elements()
        self.truss_data_table()

    def truss_data_table(self):
        self.apply_elements.destroy()
        self.elements_table.destroy()
        self.elements_table_container._parent_frame.destroy()
        self.number_of_joints = len(set([item for pair in self.pair_elements for item in pair]))
        self.scrollable_table = CTkScrollableFrame(self, width=385, height=300, fg_color='black', bg_color='black')
        self.scrollable_table.place(relx=0.5, rely=0.45, anchor=CENTER)
        self.data_table = CTkFrame(self.scrollable_table)
        self.data_table.pack(fill="both", expand=True)
        headers = ["Joint", "X", "Y", "RX", "RY", "FX", "FY"]
        for col, header in enumerate(headers):
            header_label = CTkLabel(self.data_table, text=header, font=("Arial", 15, "bold"))
            header_label.grid(row=0, column=col, padx=10, pady=10)
        self.table_entries = []
        for i in range(self.number_of_joints):
            row_entries = []
            for j in range(len(headers)):
                entry = CTkEntry(self.data_table, width=45)
                entry.grid(row=i+1, column=j, padx=5, pady=5)
                row_entries.append(entry)
            self.table_entries.append(row_entries)
        self.apply_button = CTkButton(self, text="APPLY", fg_color='black', font=('Arial', 15, 'bold'), command=self.check_joint_properties)
        self.apply_button.place(relx=0.459, rely=0.95, anchor=CENTER)

    def check_joint_properties(self):
        for input_entries in self.table_entries:
            row_data = []
            for entry in input_entries:
                value = entry.get()
                row_data.append(value)
            if not row_data[0].isalpha() or any(not value.lstrip('-').isdigit() for value in row_data[1:]):
                messagebox.showerror("Input Error", "Error: The Joint value must be letters and the rest must be numerical.")
                return    
        self.apply_button.destroy()
        self.gather_table_data()
        self.truss_solve_button()

    def truss_solve_button(self):
        solve_button = CTkButton(self, text="SOLVE", fg_color="black", text_color='white', font=('Arial', 15, 'bold'), width=100, command=lambda: [solve_button.destroy(), self.plot_truss_and_solve()])
        solve_button.place(relx=0.459, rely=0.95, anchor=CENTER)

    def gather_pair_truss_elements(self):
        for row_entries in self.table_elements:
            row_data = []
            for entry in row_entries:
                if entry.get() == "": continue
                row_data.append(entry.get())
            if len(row_data) == 0: continue
            self.pair_elements.append(row_data[0] + row_data[1])

    def gather_table_data(self):
        for row_entries in self.table_entries:
            row_data = []
            for entry in row_entries:
                row_data.append(entry.get())
                if entry.get() == "": continue
            if row_data[0] == "": continue
            self.joint_data[row_data[0]] = row_data[1:]

    def solve_truss(self):
        try:
            # str values : X, Y, RX, RY, FX, FY
            x_axis = [int(values[0]) for values in self.joint_data.values()]
            y_axis = [int(values[1]) for values in self.joint_data.values()]
            x_reactions = [int(values[2]) for values in self.joint_data.values()]
            y_reactions = [int(values[3]) for values in self.joint_data.values()]
            force_x = [-int(values[4]) for values in self.joint_data.values()]
            force_y = [int(values[5]) for values in self.joint_data.values()]

            x_values = [-int(values[4]) for values in self.joint_data.values()]
            y_values = [-int(values[5]) for values in self.joint_data.values()]

            x_index = [i for i, x in enumerate(x_reactions) if x == 1]
            y_index = [i for i, y in enumerate(y_reactions) if y == 1]
            if (len(x_index)) == 1: xy_eq = [1, 0, 0], [0, 1, 1]
            else: xy_eq = [1, 1, 0], [0, 0, 1]

            momentum_equation = []
            for i in x_index:
                momentum_equation.append(-x_reactions[i]*y_axis[i])
            for j in y_index:
                momentum_equation.append(y_reactions[j]*x_axis[j])
            moment_f_x = [f*y for f, y in zip(force_x, y_axis)]
            moment_f_y = [-f*x for f, x in zip(force_y, x_axis)]

            left_equation = np.array([xy_eq[0], xy_eq[1], momentum_equation]) # Left side of the equation system
            right_equation = np.array([sum(x_values), sum(y_values), sum(moment_f_y) + sum(moment_f_x)]) # Right side of the equation system
            reaction = np.linalg.solve(left_equation, right_equation).tolist() # Reaction solutions R1, R2 and R3
            for i, val_x in enumerate(x_reactions):
                if val_x == 1:
                    x_reactions[i] = round(reaction[0], 2)
                    reaction.pop(0)
            for j, val_y in enumerate(y_reactions):
                if val_y == 1:
                    y_reactions[j] = round(reaction[0], 2)
                    reaction.pop(0)
            
            for i, keys in enumerate(self.joint_data.keys()):
                self.joint_data[keys][2] = x_reactions[i]
                self.joint_data[keys][3] = y_reactions[i]

            values_to_store = [None]*len(self.pair_elements)
            start_joint = [s for s, _ in self.pair_elements]
            end_joint = [e for _, e in self.pair_elements]
            letters = Counter(start_joint + end_joint)
            sorted_letters = sorted(letters.items(), key=operator.itemgetter(1))
            sorted_letters = [list(ele) for ele in sorted_letters]
            while (None in values_to_store):
                joint = sorted_letters[0][0]
                e_forces = []
                for i in range(len(self.pair_elements)):
                    if (joint in self.pair_elements[i]) and values_to_store[i] == None:
                        e_forces.append(self.pair_elements[i])
                if len(e_forces) == 2:
                    angles = []
                    for point in e_forces:
                        start_joint = point[0]
                        end_joint = point[1]
                        distance_y = float(self.joint_data[point.replace(joint, '')][1]) - float(self.joint_data[joint][1])
                        distance_x = float(self.joint_data[point.replace(joint, '')][0]) - float(self.joint_data[joint][0])
                        if distance_x < 0: angles.append(math.atan(distance_y/distance_x) + math.pi)
                        elif distance_x > 0: angles.append(math.atan(distance_y/distance_x))
                        else:
                            if distance_y > 0: angles.append(math.pi/2)
                            else: angles.append(-math.pi/2)
                        # Reduce number of unknowns by joint
                        for i in range(len(sorted_letters)):
                            if point.replace(joint, '') == sorted_letters[i][0]:
                                sorted_letters[i][1] -= 1
                    # Left side of force equilibrium equations
                    left_x = [math.cos(angles[0]), math.cos(angles[1])]
                    left_y = [math.sin(angles[0]), math.sin(angles[1])]
                    # Right side of force equilibrium equations
                    right_x = -(float(self.joint_data[joint][2]) + float(self.joint_data[joint][4]))
                    right_y = -(float(self.joint_data[joint][3]) + float(self.joint_data[joint][5]))
                    a = np.array([left_x, left_y]) # Left side of the equation system
                    b = np.array([right_x, right_y]) # Right side of the equation system
                    R = np.linalg.solve(a, b).tolist() # Solution of forces
                    result = R.copy()
                    elements_forces = [tuple(x) for x in list(zip(e_forces, R))]
                    for i in e_forces:
                        for j, values in enumerate(self.pair_elements):
                            if i == values:
                                values_to_store[j] = round(result[0], 2)
                                result.pop(0)
                else:
                    angles = []
                    distance_y = float(self.joint_data[e_forces[0].replace(joint, '')][1]) - float(self.joint_data[joint][1])
                    distance_x = float(self.joint_data[e_forces[0].replace(joint, '')][0]) - float(self.joint_data[joint][0])
                    if distance_x < 0: angles.append(math.atan(distance_y/distance_x) + math.pi)
                    elif distance_x > 0: angles.append(math.atan(distance_y/distance_x))
                    else:
                        if distance_y > 0: angles.append(math.pi/2)
                        else: angles.append(-math.pi/2)
                    for i in range(len(sorted_letters)):
                        if e_forces[0].replace(joint, '') == sorted_letters[i][0]: sorted_letters[i][1] -= 1
                    if angles[0] == 0:
                        a = np.array([[math.cos(angles[0])]]) # Left side of the equation system
                        b = np.array([-(float(self.joint_data[joint][2]) + float(self.joint_data[joint][4]))]) # Right side of the equation system
                        result = np.linalg.solve(a, b)[0] # Reaction solutions R1, R2 and R3
                    else:
                        a = np.array([[math.sin(angles[0])]]) # Left side of the equation system
                        b = np.array([-(float(self.joint_data[joint][3]) + float(self.joint_data[joint][5]))]) # Right side of the equation system
                        R = np.linalg.solve(a, b)[0] # Reaction solutions R1, R2 and R3
                        result = R
                        elements_forces = (e_forces[0], R)
                    for j, values in enumerate(self.pair_elements):
                        if e_forces[0] == values:
                            values_to_store[j] = round(result, 2)
                # TODO: Debug
                for idx, keys in enumerate(self.joint_data.keys()):
                    if type(self.joint_data[keys][4]) == str and type(self.joint_data[keys][5]) == str:
                        force_x[idx] = float(self.joint_data[keys][4])
                        force_y[idx] = float(self.joint_data[keys][5])
                    else:
                        force_x[idx] = self.joint_data[keys][4]
                        force_y[idx] = self.joint_data[keys][5]

                for point in e_forces:
                    if len(e_forces) == 2:
                        for i, j in enumerate(elements_forces):
                            if point == j[0]:
                                for idx, joint_letter in enumerate(list(self.joint_data.keys())):
                                    if point.replace(joint,"") == joint_letter:
                                        force_x[idx] = force_x[idx]-(R[i]*math.cos(angles[i]))
                                        force_y[idx] = force_y[idx]-(R[i]*math.sin(angles[i]))
                    else:
                        for idx, joint_letter in enumerate(list(self.joint_data.keys())):
                            if point.replace(joint,"") == joint_letter:
                                force_x[idx] = force_x[idx]-(result*math.cos(angles[0]))
                                force_y[idx] = force_y[idx]-(result*math.sin(angles[0]))

                for idx, keys in enumerate(self.joint_data.keys()):
                    self.joint_data[keys][4] = force_x[idx]
                    self.joint_data[keys][5] = force_y[idx]
                sorted_letters.pop(0)
                sorted_letters = sorted(sorted_letters, key=operator.itemgetter(1))
        except:
            messagebox.showerror("Truss infrastructure", "Invalid truss infrastructure create again.")
            self.restart()
        return values_to_store

    def plot_truss_and_solve(self):
        solve_value = self.solve_truss()
        for i, (start_joint, end_joint) in enumerate(self.pair_elements):
            x_coordinates = int(self.joint_data[start_joint][0]), int(self.joint_data[end_joint][0])
            y_coordinates = int(self.joint_data[start_joint][1]), int(self.joint_data[end_joint][1])
            plt.plot(x_coordinates, y_coordinates, "ro-")
            force_text = str(round(solve_value[i], 2))
            plt.text(mean(x_coordinates), mean(y_coordinates), force_text, fontsize=10, color="g")
            plt.text(x_coordinates[0], y_coordinates[0], start_joint, fontsize=12, color = "b", fontweight="bold")
            plt.text(x_coordinates[1], y_coordinates[1], end_joint, fontsize=12, color = "b", fontweight="bold")
        plt.show()

TrussSolver().mainloop()
