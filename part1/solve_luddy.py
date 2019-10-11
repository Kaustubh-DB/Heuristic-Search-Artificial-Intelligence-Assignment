#!/usr/local/bin/python3
# solve_luddy.py : Sliding tile puzzle solver
#
# Code by: [Kaustubh Bhalerao(kbhaler), Suyash Poredi(sporedi), Dipali Tolia(dtolia)]
#
# Based on skeleton code by D. Crandall, September 2019
#
from queue import PriorityQueue
import queue as Q
import sys
import time
import os
import heapq
from heapq import heapify, heappush, heappop

MOVES = {"R": (0, -1), "L": (0, 1), "D": (-1, 0), "U": (1, 0)}

LUDDY_MOVES = {"A": (2, 1), "B": (2, -1), "C": (-2, 1), "D": (-2, -1), "E": (1, 2), "F": (1, -2), "G": (-1, 2),"H": (-1, -2)}

#LUDDY_MOVES = {"A": (-2, -1), "B": (-2, 1), "C": (2, -1), "D": (2, 1), "E": (-1, -2), "F": (-1, 2), "G": (1, -2), "H": (1, 2)}

def rowcol2ind(row, col):
    return row * 4 + col


def ind2rowcol(ind):
    return int(ind / 4), ind % 4


def valid_index(row, col):
    return 0 <= row <= 3 and 0 <= col <= 3


def swap_ind(list, ind1, ind2):
    return list[0:ind1] + (list[ind2],) + list[ind1 + 1:ind2] + (list[ind1],) + list[ind2 + 1:]


def swap_tiles(state, row1, col1, row2, col2):
    return swap_ind(state, *(sorted((rowcol2ind(row1, col1), rowcol2ind(row2, col2)))))


def printable_board(row):
    return ['%3d %3d %3d %3d' % (row[j:(j + 4)]) for j in range(0, 16, 4)]


# Finding the number of unorganized tiles on the board
def unorganized_tiles(state):
    count_tiles = 0
    for i in range(15):
        if state[i] != (i + 1):
            count_tiles += 1
    if state[15] != 0:
                count_tiles += 1
    return count_tiles


# Checks the board if it is solvable or not
def issolvable(state):
    inversion = 0

    for i in range(len(state)):
        for j in range(i, len(state)):
            if (state[i] > state[j]) and state[i] != 0 and state[j] != 0:
                inversion += 1
    (empty_row, empty_col) = ind2rowcol(state.index(0))

    if empty_row % 2 == 0 and inversion % 2 == 1:
        return True
    if empty_row % 2 == 1 and inversion % 2 == 0:
        return True

    return False


# Finding the possible successor states
def successors(state):
    # Finding the coordinates of '0'
    (empty_row, empty_col) = ind2rowcol(state.index(0))
    if sys.argv[2] == 'luddy':

        return [(swap_tiles(state, empty_row, empty_col, empty_row + i, empty_col + j), c) \
                for (c, (i, j)) in LUDDY_MOVES.items() if valid_index(empty_row + i, empty_col + j)]

    elif sys.argv[2] == 'original':
        return [(swap_tiles(state, empty_row, empty_col, empty_row + i, empty_col + j), c) \
                for (c, (i, j)) in MOVES.items() if valid_index(empty_row + i, empty_col + j)]
    else:
        return [(swap_tiles(state, empty_row, empty_col, (empty_row + i) % 4, (empty_col + j) % 4), c) for (c, (i, j))
                in MOVES.items()]

#Fvalue is calculated based on number of misplaced tiles and length of move
def f_cost(succ, move):
    h_cost = unorganized_tiles(succ)
    length_move = len(move)
    f = h_cost + length_move
    return f


# checking if we have reached goal state or not
def is_goal(state):
    return sorted(state[:-1]) == list(state[:-1]) and state[-1] == 0


# Solve method - using A* Search, Defining heuristic and F value
def solve(initial_board):
    fringe = [(0, initial_board, "")]
    closed = set()

    q = Q.PriorityQueue()
    g_cost = 0
    h_cost = unorganized_tiles(initial_board)
    f = h_cost + 0
    q.put((f, initial_board, "",0))

    while not q.empty():
        (f, state, route_so_far,g) = q.get()
        g=g+1

        if is_goal(state):
            return route_so_far

        for (succ, move) in successors(state):
            if succ not in closed:
                closed.add(succ)
                f_value = f_cost(succ, move)
                q.put((f_value + g, succ, route_so_far + move, g))


    return False


# testing cases
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise (Exception("Error: expected 2 arguments"))

    start_state = []

    with open(sys.argv[1], 'r') as file:
        for line in file:
            start_state += [int(i) for i in line.split()]

    '''
    if(sys.argv[2] != "original"):
        raise(Exception("Error: only 'original' puzzle currently supported -- you need to implement the other two!"))
    '''
    if len(start_state) != 16:
        raise (Exception("Error: couldn't parse start state file"))

    start_state = tuple(start_state)

    print("Start state: \n" + "\n".join(printable_board(start_state)))

    if issolvable(start_state):

        print("Solving...")

        route = solve(tuple(start_state))

        print("Solution found in " + str(len(route)) + " moves:" + "\n" + route)

    else:
        print("Inf")
