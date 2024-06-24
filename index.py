from tkinter import messagebox, Tk
import pygame
import sys

# Initialize Pygame
pygame.init()

window_width = 1000
window_height = 1000
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Pathfinding Visualizer")

column = 50
rows = 50

box_width = window_width // column
box_height = window_height // rows
grid = []
queue = []
path = []

class Box:
    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.start = False
        self.wall = False
        self.target = False
        self.queued = False
        self.visited = False
        self.neighbors = []
        self.prior = None

    def draw(self, win, color):
        pygame.draw.rect(win, color, (self.x * box_width, self.y * box_height, box_width - 2, box_height - 2))

    def set_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.x < column - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.y < rows - 1:
            self.neighbors.append(grid[self.x][self.y + 1])

# Create grid
def create_grid():
    global grid
    grid = []
    for i in range(column):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)
    for i in range(column):
        for j in range(rows):
            grid[i][j].set_neighbors()

create_grid()

start_box = grid[0][0]
start_box.start = True
start_box.visited = True
queue = [start_box]

begin_search = False
target_box_set = False
searching = True
target_box = None

def reset_grid():
    global grid, queue, path, start_box, target_box, target_box_set, begin_search, searching
    grid = []
    queue = []
    path = []
    target_box = None
    target_box_set = False
    begin_search = False
    searching = True
    create_grid()
    start_box = grid[0][0]
    start_box.start = True
    start_box.visited = True
    queue = [start_box]

def main():
    global begin_search, target_box_set, searching, target_box

    font = pygame.font.SysFont("comicsans", 40)
    start_button = pygame.Rect(850, 50, 100, 50)
    reset_button = pygame.Rect(850, 150, 100, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if start_button.collidepoint(x, y):
                    if target_box_set:
                        begin_search = True
                elif reset_button.collidepoint(x, y):
                    reset_grid()
                else:
                    i, j = x // box_width, y // box_height
                    if 0 <= i < column and 0 <= j < rows:
                        if event.button == 1:
                            grid[i][j].wall = True
                        if event.button == 3 and not target_box_set:
                            target_box = grid[i][j]
                            target_box.target = True
                            target_box_set = True

        if begin_search:
            if len(queue) > 0 and searching:
                current_box = queue.pop(0)
                current_box.visited = True
                if current_box == target_box:
                    searching = False
                    while current_box.prior != start_box:
                        path.append(current_box.prior)
                        current_box = current_box.prior
                else:
                    for neighbor in current_box.neighbors:
                        if not neighbor.queued and not neighbor.wall:
                            neighbor.queued = True
                            neighbor.prior = current_box
                            queue.append(neighbor)
            else:
                if searching:
                    Tk().wm_withdraw()
                    messagebox.showinfo("No Solution", "There is no solution")
                    searching = False

        window.fill((30, 30, 30))

        for i in range(column):
            for j in range(rows):
                box = grid[i][j]
                if box in path:
                    box.draw(window, (0, 0, 200))
                elif box.start:
                    box.draw(window, (0, 200, 200))
                elif box.wall:
                    box.draw(window, (90, 90, 90))
                elif box.target:
                    box.draw(window, (200, 200, 0))
                elif box.visited:
                    box.draw(window, (0, 200, 0))
                elif box.queued:
                    box.draw(window, (200, 0, 0))
                else:
                    box.draw(window, (50, 50, 50))

        pygame.draw.rect(window, (0, 200, 0), start_button)
        pygame.draw.rect(window, (200, 0, 0), reset_button)
        window.blit(font.render("Start", True, (0, 0, 0)), (860, 60))
        window.blit(font.render("Reset", True, (0, 0, 0)), (860, 160))

        pygame.display.flip()

main()
