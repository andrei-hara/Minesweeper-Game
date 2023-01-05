from tkinter import Button, Label
import random
import settings
import ctypes
import sys

class Cell:
    #global variables
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None

    def __init__(self,x, y, is_mine=False):
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened = False
        self.is_flagged = False
        self.x = x
        self.y = y

        #Append the object to the Cell.all list
        Cell.all.append(self)
    
    def create_btn_object(self, location):
        btn = Button(
            location,
            width=14,
            height=3,
        )
        btn.bind('<Button-1>', self.left_click_actions) # assigning the left click action by refference to function
        btn.bind('<Button-3>', self.right_click_actions)
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
            width=12,
            height=4,
            font=("", 30)
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()     
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell in self.surrounded_cells:
                    cell.show_cell()
                    # configuring the background to default if the cell is flagged
                    cell.cell_btn_object.configure(bg='SystemButtonFace')
            self.show_cell()
            # same background configure 
            self.cell_btn_object.configure(bg='SystemButtonFace')
            # If mines count is 0
            if Cell.cell_count == settings.MINES_COUNT:
                ctypes.windll.user32.MessageBoxW(0, "You've won the game!", "Congratulations!", 0)

        # Cancel the left and right click actions for the cell if it is opened
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def show_mine(self):
        # self.cell_btn_object.configure(bg='red')
        ctypes.windll.user32.MessageBoxW(0, 'You clicked on a mine!', 'Game Over!', 0)
        sys.exit()

    def get_cell_by_axis(self, x, y):
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property #read-only function
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None] # overriding the list to eliminate the none values    
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

    def show_cell(self):
        if not self.is_opened:
            # Show the surrounded mines
            self.cell_btn_object.configure(text = f"{self.surrounded_cells_mines_length}")
            # Replace the text of cell count label
            if Cell.cell_count_label_object:
                Cell.cell_count -= 1
                Cell.cell_count_label_object.configure(text=f"Cells Left:{Cell.cell_count}")
            # Mark the cell as opened
        self.is_opened = True

    def right_click_actions(self, event):
        if not self.is_flagged:
            self.cell_btn_object.configure(bg='yellow')
            self.is_flagged = True
        else:
            self.cell_btn_object.configure(bg='SystemButtonFace')
            self.is_flagged = False

    # static method for usage outside the class instantiation
    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all,
            settings.MINES_COUNT
        )
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    # overriding the representation of cells
    def __repr__(self):
        return f"Cell({self.x}, {self.y})"


