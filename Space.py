from Pedestrians import *
import config as cfg
import numpy as np
from PIL import Image
import random


class Cell:

    def __init__(self, state, position_x, position_y, pedestrian=None, isExit=False):
        self.state = state  # 3 : obstacle, 0 : free, 1 : pedestrian
        self.isExit = isExit
        self.pedestrian = pedestrian
        self.position_x = position_x
        self.position_y = position_y
        self.sff_value = np.inf
        self.dff_value = 0

    def putPed(self, pedestrian):
        self.state = 1
        self.pedestrian = pedestrian

    def isOccupied(self):
        return self.state != 0

    def hasPedestrian(self):
        return self.state == 1

    def removePedestrian(self):
        if self.hasPedestrian():
            self.state = 0
            self.pedestrian = None

    def addPedestrian(self, pedestrian):
        self.state = 1
        self.pedestrian = pedestrian

    def isObstacle(self):
        return self.state == 3


class Space:

    def __init__(self, width, height, nbPeds, imageName=None):
        np.random.seed(0)
        random.seed(0)
        self.grid = [[Cell(0, i, j) for i in range(width)] for j in range(height)]
        self.exits = []
        self.nbPeds = nbPeds
        self.nbCellObstacles = 0
        self.dff = np.array((width, height))
        if imageName:
            self.initObstacles(imageName)
        self.initPedestrians()
        self.checkNbPeds()
        self.init_sff()

    def initObstacles(self, imageName):
        im = Image.open(imageName)
        imArray = np.array(im.convert("L"))
        with np.nditer(imArray, op_flags=['readwrite']) as it:
            for x in it:
                if x == 0:
                    x[...] = 3
                elif x == 255:
                    x[...] = 0
                elif x > 0:
                    x[...] = 2
        for row_cell_image, row_cell_grid in zip(imArray, self.grid):
            for cell_image, cell_grid in zip(row_cell_image, row_cell_grid):
                if cell_image != 2:
                    cell_grid.state = cell_image
                    if cell_image == 3:
                        self.nbCellObstacles += 1
                else:
                    cell_grid.state = 0
                    cell_grid.isExit = True
                    cell_grid.sff_value = 0
                    self.exits.append(cell_grid)

    def init_sff(self):
        cells_to_visit = {}
        for exit in self.exits:
            cells_to_visit[exit] = exit.sff_value

        while len(cells_to_visit) != 0:
            cell = cells_to_visit.popitem()[0]
            if cell.isObstacle():
                continue
            neighbors = self.getNeighborsCells(cell)
            for neighbor in neighbors:
                if neighbor.isObstacle():
                    continue
                if cell.sff_value + 1 < neighbor.sff_value:
                    neighbor.sff_value = cell.sff_value + 1
                    cells_to_visit[neighbor] = neighbor.sff_value

    def checkNbPeds(self):
        nbMax = self.grid.__len__() * self.grid[0].__len__() - self.nbCellObstacles
        if self.nbPeds > nbMax:
            print("Too many pedestrians for this room, only {} can fit".format(nbMax))
            self.nbPeds = nbMax

    def initPedestrians(self):
        nbPedsPut = 0
        while nbPedsPut < self.nbPeds:
            i = np.random.randint(0, len(self.grid))
            j = np.random.randint(0, len(self.grid[0]))
            if not (self.grid[i][j].isOccupied()):
                self.grid[i][j].putPed(Pedestrians(j, i))
                nbPedsPut += 1

        for row in self.grid:
            for cell in row:
                if cell.hasPedestrian():
                    cell.pedestrian.neighbors = {key: 0 for key in self.getNeighborsCells(cell)}

    def getNeighborsCells(self, cell):
        if cfg.neighborhood == "Moore":
            N = []
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if i == 0 and j == 0:
                        continue
                    elif self.checkInBounds(cell.position_y + i, cell.position_x + j):
                        n = self.grid[cell.position_y + i][cell.position_x + j]
                        N.append(n)
            return N
        elif cfg.neighborhood == "Neumann":
            N = []
            if self.checkInBounds(cell.position_y + 1, cell.position_x):
                n = self.grid[cell.position_y + 1][cell.position_x]
                N.append(n)
            if self.checkInBounds(cell.position_y - 1, cell.position_x):
                n = self.grid[cell.position_y - 1][cell.position_x]
                N.append(n)
            if self.checkInBounds(cell.position_y, cell.position_x + 1):
                n = self.grid[cell.position_y][cell.position_x + 1]
                N.append(n)
            if self.checkInBounds(cell.position_y, cell.position_x - 1):
                n = self.grid[cell.position_y][cell.position_x - 1]
                N.append(n)
            return N
        else:
            raise NotImplementedError("Only Moore neighborhood is implemented")

    def checkInBounds(self, x, y):
        return 0 <= x < len(self.grid) and 0 <= y < len(self.grid[0])

    def updateDFF(self):
        for row in self.grid:
            for cell in row:
                if cell.hasPedestrian():
                    cell.dff_value = min(cfg.max_dff_value, cell.dff_value + cfg.delta_DFF)
                if np.random.rand() < cfg.decay_rate_DFF:
                    cell.dff_value = max(0, cell.dff_value - cfg.delta_decay_DFF)
                elif np.random.rand() < cfg.diffusion_rate_DFF and cell.dff_value > 0:
                    cell.dff_value = max(0, cell.dff_value - cfg.delta_diffusion_DFF)
                    neighbor = random.choice(self.getNeighborsCells(cell))
                    if neighbor.isObstacle:
                        continue
                    neighbor.dff_value = min(cfg.max_dff_value, neighbor.dff_value + cfg.delta_DFF)


    def move_ped(self, old_cell, new_cell):
        new_cell.addPedestrian(old_cell.pedestrian)
        old_cell.removePedestrian()
        new_cell.pedestrian.move()

    def sequential_update(self):
        # TODO : shuffle grid_cell
        conflicts = {}

        for row in self.grid:
            for cell in row:
                if not (cell.hasPedestrian()):
                    continue
                if cell.isExit and cell.hasPedestrian():
                    cell.removePedestrian()
                    self.nbPeds -= 1
                    continue

                sum_proba_neighbors = 0
                cell.pedestrian.neighbors = {}
                for neighbor in self.getNeighborsCells(cell):
                    proba = np.exp(cfg.kappaS * (cell.sff_value - neighbor.sff_value)) * np.exp(
                        cfg.kappaD * (neighbor.dff_value - cell.dff_value)) * (1 - neighbor.isOccupied())
                    cell.pedestrian.neighbors[neighbor] = proba
                    sum_proba_neighbors += proba

                if sum_proba_neighbors == 0:  # ped cannot move
                    continue

                for neighbor in cell.pedestrian.neighbors.keys():
                    cell.pedestrian.neighbors[neighbor] /= sum_proba_neighbors

                r = np.random.rand()
                # TODO : shuffle neighbors ?
                for i, neighbor in enumerate(cell.pedestrian.neighbors.keys()):
                    r -= cell.pedestrian.neighbors[neighbor]
                    if r <= 0:
                        cell.pedestrian.future_x = neighbor.position_x
                        cell.pedestrian.future_y = neighbor.position_y
                        try:
                            conflicts[neighbor].append(cell.pedestrian)
                        except KeyError:
                            conflicts[neighbor] = [cell.pedestrian]
                        break
        return conflicts

    def solveConflicts(self, conflicts):
        for desired_cell, pedestrians in conflicts.items():
            if len(pedestrians) > 1:
                probas = np.zeros(len(pedestrians))
                for i, ped in enumerate(pedestrians):
                    probas[i] = ped.neighbors[desired_cell]
                probas = probas / sum(probas)
                winner = pedestrians[np.argmax(probas)]
                self.move_ped(self.grid[winner.y][winner.x], self.grid[winner.future_y][winner.future_x])
            else:
                self.move_ped(self.grid[pedestrians[0].y][pedestrians[0].x], self.grid[pedestrians[0].future_y][pedestrians[0].future_x])
