import random
from typing import List

import pygame
from pygame import *
import tkinter as tk
from tkinter import *
from tkinter import filedialog as fd, simpledialog
from tkinter import messagebox

from Button import Button
from MenuItem import MenuItem
from constants import *
import matplotlib.backends.backend_agg as agg
import pylab

import re


class GUI:

    def insert_dialog_save(self):
        user_input = simpledialog.askstring(title="Insert name", prompt="Save as .json")
        if user_input is not None:
            check = user_input.split("/")[-1].split(".")

            if check[-1] == "json":
                self.algo.save_to_json(user_input)
            else:
                messagebox.showerror("ERROR", "INVALID INPUT!")

        else:
            messagebox.showerror("ERROR", "INVALID INPUT!")

    def choose_dialog_load(self):
        dialog = fd.askopenfilename()
        if dialog != "":
            print(dialog)
            list_check = dialog.split("/")
            user_input = list_check[len(list_check) - 1].split(".")

            if user_input[-1] == "json":
                self.algo.load_from_json(dialog)

                self.plot()
            else:
                messagebox.showerror("ERROR", "INVALID INPUT!")

    def insert_dialog_load(self):
        root = tk.Tk()
        root.withdraw()
        user_input = simpledialog.askstring(title="Insert", prompt="Insert file name")

        if user_input is not None:
            check = user_input.split(".")
            if check[len(check) - 1] == "json":
                self.algo.load_from_json(user_input)

                self.plot()
            else:
                messagebox.showerror("ERROR", "INVALID INPUT!")

    def ask_add_node(self):
        node_id = simpledialog.askinteger(title="Add Node Input", prompt="Insert Node ID")
        if node_id is None:
            messagebox.showerror("ERROR", "YOU MUST INPUT A VALUE!")
            return

        node_pos_x = simpledialog.askfloat(title="Add Node Input",
                                           prompt="Insert Node X coords\nLeave empty for a null position")

        node_pos_y = simpledialog.askfloat(title="Add Node Input",
                                           prompt="Insert Node Y coords\nLeave empty for a null position")
        if node_pos_x is None or node_pos_y is None:
            self.algo.get_digraph().add_node(node_id)
        else:
            self.algo.get_digraph().add_node(node_id, (node_pos_x, node_pos_y))

        self.plot()

    def ask_remove_node(self):
        node_id = simpledialog.askinteger(title="Remove Node ID", prompt="Insert Node ID!")
        if node_id is None:
            return
        self.algo.get_digraph().remove_node(node_id)

        self.plot()

    def ask_add_edge(self):
        edge_src = simpledialog.askinteger(title="Add Edge Input", prompt="Insert Source Node ID!")
        if edge_src is None:
            return

        if not self.algo.get_digraph().is_exist_node(edge_src):
            messagebox.showerror("ERROR", "NODE " + str(edge_src) + " Doesn't exist!")
            return
        edge_dest = simpledialog.askinteger(title="Add Edge Input", prompt="Insert Destination Node ID!")
        if edge_dest is None:
            return
        if not self.algo.get_digraph().is_exist_node(edge_dest):
            messagebox.showerror("ERROR", "NODE " + str(edge_dest) + " Doesn't exist!")
            return
        edge_weight = simpledialog.askfloat(title="Add Edge Input", prompt="Insert Edge Weight")
        if edge_weight is None:
            return
        self.algo.get_digraph().add_edge(edge_src, edge_dest, edge_weight)

        self.plot()

    def ask_remove_edge(self):
        edge_src = simpledialog.askinteger(title="Remove Edge Input", prompt="Insert Source Node ID!")
        if edge_src is None:
            return

        if not self.algo.get_digraph().is_exist_node(edge_src):
            messagebox.showerror("ERROR", "NODE " + str(edge_src) + " Doesn't exist!")
            return
        edge_dest = simpledialog.askinteger(title="Remove Edge Input", prompt="Insert Destination Node ID!")
        if edge_dest is None:
            return
        if not self.algo.get_digraph().is_exist_node(edge_dest):
            messagebox.showerror("ERROR", "NODE " + str(edge_dest) + " Doesn't exist!")
            return
        self.algo.get_digraph().remove_edge(edge_src, edge_dest)

        self.plot()

    def find_shortest_path(self):
        edge_src = simpledialog.askinteger(title="Shortest Path Input", prompt="Insert Source Node ID!")
        if edge_src is None:
            return

        if not self.algo.get_digraph().is_exist_node(edge_src):
            messagebox.showerror("ERROR", "NODE " + str(edge_src) + " Doesn't exist!")
            return
        edge_dest = simpledialog.askinteger(title="Shortest Path Input", prompt="Insert Destination Node ID!")
        if edge_dest is None:
            return
        if not self.algo.get_digraph().is_exist_node(edge_dest):
            messagebox.showerror("ERROR", "NODE " + str(edge_dest) + " Doesn't exist!")
            return

        answer = self.algo.shortest_path(edge_src, edge_dest)
        if answer == (float('inf'), []):
            messagebox.showinfo("Shortest Path Output",
                                "There is no path from N" + str(edge_src) + " to N" + str(edge_dest))
            return
        st1 = print_nodelist(answer[1])
        messagebox.showinfo("Shortest Path Output", "Path: " + st1 + "\nDistance: " + str(answer[0]))

    def find_tsp(self):
        nodes = simpledialog.askstring(title="TSP INPUT",
                                       prompt="Insert Node List for TSP(separate with comma)\nExample: 1,3,4")
        if nodes is None:
            return
        if re.fullmatch("((\\d+),)+(\\d+)", nodes.strip()) is not None:
            node_list = nodes.split(",")
            city_list = []
            for index in range(len(node_list)):
                if self.algo.get_digraph().is_exist_node(int(node_list[index])):
                    city_list.append(int(node_list[index]))
                    print(int(node_list[index]))
                else:
                    messagebox.showerror("ERROR", "NODE " + node_list[index] + " Doesn't exist!")
                    return
            answer = self.algo.TSP(city_list)
            st1 = print_nodelist(answer[0])
            messagebox.showinfo("TSP OUTPUT", "Path: " + st1 + "\nDistance: " + str(answer[1]))

        else:
            messagebox.showerror("ERROR", "INVALID INPUT!")

    def plot(self):
        graph_size = (screen_size - button_height - padding) / 100
        fig = pylab.figure(figsize=[graph_size, graph_size],
                           dpi=100,
                           )
        ax = fig.gca()
        ax.axis("off")
        nodes = self.algo.get_digraph().get_all_v()
        if self.algo.get_digraph().v_size() == 1:
            ax.plot(self.screen.get_width() / 2, self.screen.get_height() / 2, 'ro')
        for key in nodes:
            if nodes[key].get_pos() is not None:
                x = nodes[key].get_pos()[0]
                y = nodes[key].get_pos()[1]
            else:
                x = random.uniform(self.algo.get_digraph().min_pos[0], self.algo.get_digraph().max_pos[1])
                y = random.uniform(self.algo.get_digraph().min_pos[0], self.algo.get_digraph().max_pos[1])
                nodes[key].set_pos((x, y))

            edges_out = self.algo.get_digraph().all_out_edges_of_node(key)
            for edge_key in edges_out:
                if nodes[edges_out[edge_key].get_dest()].get_pos() is not None:
                    dest_pos = nodes[edges_out[edge_key].get_dest()].get_pos()
                    ax.annotate("", xy=(x, y), xytext=(dest_pos[0], dest_pos[1]), arrowprops=dict(arrowstyle="<-"))
                else:
                    dest_x = random.uniform(self.algo.get_digraph().min_pos[0], self.algo.get_digraph().max_pos[1])
                    dest_y = random.uniform(self.algo.get_digraph().min_pos[0], self.algo.get_digraph().max_pos[1])
                    ax.annotate("", xy=(x, y), xytext=(dest_x, dest_y), arrowprops=dict(arrowstyle="<-"))
                    nodes[edges_out[edge_key].get_dest()].set_pos((dest_x, dest_y))

            ax.text(x, y, str(self.algo.get_digraph().get_node(key).get_id()), color="green", fontsize=12)
            ax.plot(x, y, 'ro')

        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()

        size = canvas.get_width_height()

        surf = pygame.image.fromstring(raw_data, size, "RGB")
        self.surf = surf

    def __init__(self,algo):
        #if algo is None:
        self.algo = algo
        #else:
        #    self.algo = algo
        pygame.init()
        self.clock = pygame.time.Clock()

        self.screen = display.set_mode((screen_size, screen_size), depth=32)

        self.arial_font = font.SysFont('Arial', 15, bold=True)

        self.save_button = Button('Save Graph', (button_width, button_height), x=3,
                                  on_click_func=lambda: self.insert_dialog_save())
        self.save_button.show()

        self.load_button = Button('Load Graph', (button_width, button_height), x=126)
        self.load_button.show()

        self.edit_button = Button('Edit Graph', (button_width, button_height), x=249)
        self.edit_button.show()

        self.algo_button = Button('Algorithms Graph', (button_width, button_height), x=372)
        self.algo_button.show()

        self.buttons = [self.save_button, self.load_button, self.edit_button, self.algo_button]

        middle_screen = screen_size / 2
        self.load_button.set_x(middle_screen - padding / 2 - button_width)
        self.save_button.set_x(self.load_button.get_x() - padding - button_width)

        self.edit_button.set_x(middle_screen + padding / 2)
        self.algo_button.set_x(self.edit_button.get_x() + padding + button_width)

        self.save_menu_item = MenuItem(self.save_button, [])

        self.save_menu_item.define_button_pos()

        self.choose_for_load = Button('Choose file', (button_width, button_height), x=126,
                                      on_click_func=lambda: self.choose_dialog_load())
        self.insert_for_load = Button('File name', (button_width, button_height), x=126,
                                      on_click_func=lambda: self.insert_dialog_load())

        self.load_menu_item = MenuItem(self.load_button, [self.choose_for_load, self.insert_for_load])
        self.load_menu_item.define_button_pos()

        self.remove_edge = Button('Remove edge', (button_width, button_height), x=249,
                                  on_click_func=lambda: self.ask_remove_edge())
        self.add_edge = Button('Add edge', (button_width, button_height), x=249,
                               on_click_func=lambda: self.ask_add_edge())
        self.remove_node = Button('Remove node', (button_width, button_height), x=249,
                                  on_click_func=lambda: self.ask_remove_node())
        self.add_node = Button('Add node', (button_width, button_height), x=249,
                               on_click_func=lambda: self.ask_add_node())

        self.edit_menu_item = MenuItem(self.edit_button,
                                       [self.remove_edge, self.add_edge, self.remove_node, self.add_node])
        self.edit_menu_item.define_button_pos()

        self.shortest_path = Button('Shortest path', (button_width, button_height), x=372,
                                    on_click_func=lambda: self.find_shortest_path())
        self.tsp = Button('TSP', (button_width, button_height), x=372, on_click_func=lambda: self.find_tsp())
        self.center_point = Button('Center point', (button_width, button_height), x=372,
                                   on_click_func=lambda: self.algo.get_digraph().centerPoint())

        self.algo_menu_item = MenuItem(self.algo_button, [self.shortest_path, self.tsp, self.center_point])
        self.algo_menu_item.define_button_pos()

        self.menu_items = [self.save_menu_item, self.load_menu_item, self.edit_menu_item, self.algo_menu_item]
        self.menu_item_bools = [False, False, False, False]

        self.plot()

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    quit()
                    exit(0)
            self.screen.fill(Color(255, 255, 255))
            self.screen.blit(self.surf, (0, 0))
            i = 0
            while i < 4:
                current_button = self.menu_items[i].get_button()
                current_button.render(self.screen)
                if current_button.check_hover() or self.menu_item_bools[i]:
                    self.menu_item_bools[i] = True
                    current_button.set_color(BLACK)
                    current_buttons_list = self.menu_items[i].get_buttons()
                    if current_button is self.save_button:
                        current_button.check()
                    else:
                        for menu_item in current_buttons_list:

                            menu_item.show()
                            menu_item.render(self.screen)
                            if menu_item.check_hover():
                                menu_item.set_color(BLACK)
                                menu_item.check()
                            else:
                                menu_item.set_color(GRAY)
                else:
                    current_button.set_color(GRAY)

                if not self.menu_items[i].check_rect(pygame.mouse.get_pos()):
                    self.menu_item_bools[i] = False
                i = i + 1

            display.update()


def print_nodelist(l: List[int]):
    ret = ""
    for i in range(len(l)):
        if i == len(l) - 1:
            ret += "N" + str(l[i])
        else:
            ret += "N" + str(l[i]) + "->"
    return ret
