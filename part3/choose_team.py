#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [Kaustubh Bhalerao(kbhaler), Suyash Poredi(sporedi), Dipali Tolia(dtolia)]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
from recordclass import recordclass
from collections import deque


def load_people(filename):
    people = {}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [float(i) for i in l[1:]]
    return people


# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted. It exactly exhausts the budget
#  by adding a fraction of the last person.
#

def approx_solve(people, budget):
    Item = recordclass('Item', 'index name efficiency cost')
    Node = recordclass('Node', 'level name efficiency cost items')
    # lines = input_data.split('\n')
    # print(input_data.items())
    for (person, (skill, cost)) in people.items():
        name_list.append(person)
        cost_list.append(cost)
        efficiency.append(skill)
    # firstLine = lines[0].split()
    item_count = len(cost_list)
    # print(item_count)
    capacity = budget
    # print(capacity)
    items = []

    for i in range(1, item_count + 1):
        # print(cost_list.__getitem__(i-1))
        name_value = name_list.__getitem__(i - 1)
        cost_value = float(cost_list.__getitem__(i - 1))
        skill_value = float(efficiency.__getitem__(i - 1))
        # parts = line.split()
        items.append(Item(i - 1, name_value, float(skill_value), float(cost_value)))
        # print(items)
    # sorting Item on basis of cost per efficiency.
    items = sorted(items, key=lambda Item: Item.cost / Item.efficiency)
    # print("***",items)

    v = Node(level=-1, name=None, efficiency=0, cost=0, items=[])
    Q = deque([])
    Q.append(v)

    maxValue = 0
    choosen_team = []
    while (len(Q) != 0):
        # Dequeue a node
        v = Q[0]
        # print(Q)
        Q.popleft()

        u = Node(level=None, name=None, cost=None, efficiency=None, items=[])

        u.level = v.level + 1
        u.name = items[u.level].name
        u.cost = v.cost + items[u.level].cost
        u.efficiency = v.efficiency + items[u.level].efficiency
        u.items = list(v.items)
        u.items.append(items[u.level].index)
        # print(u)
        if (u.cost <= capacity and u.efficiency > maxValue):
            maxValue = u.efficiency
            choosen_team = u.items

        bound_u = calculate_bound(u, capacity, item_count, items)
        if (bound_u > maxValue):
            Q.append(u)

        u = Node(level=None, name=None, cost=None, efficiency=None, items=[])
        u.level = v.level + 1
        u.cost = v.cost
        u.efficiency = v.efficiency
        u.items = list(v.items)

        bound_u = calculate_bound(u, capacity, item_count, items)

        if (bound_u > maxValue):
            Q.append(u)

    total_cost = 0
    solution = ()

    for i in range(0, len(choosen_team)):
        for j in range(0, len(items)):
            if (items.__getitem__(j).index == choosen_team[i]):
                total_cost += items.__getitem__(j).cost
                solution += ((items.__getitem__(j).name, 1),)

    print("Found a group with %d people costing %f with total skill %f" % (len(choosen_team), total_cost, maxValue))

    for s in solution:
        print("%s %f" % s)

    return solution


# Class to calculate the upper bound for element
def calculate_bound(u, capacity, item_count, items):
    if (u.cost >= capacity):
        return 0
    else:
        result = u.efficiency
        j = u.level + 1
        totalweight = u.cost

        while (j < item_count and totalweight + items[j].cost <= capacity):
            totalweight = totalweight + items[j].cost
            result = result + items[j].efficiency
            j = j + 1

        k = j
        if (k <= item_count - 1):
            result = result + (capacity - totalweight) * items[k].efficiency / items[k].cost

        return result


if __name__ == "__main__":

    if (len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    no_items = len(people)
    cost_list = []
    efficiency = []
    name_list = []

    approx_solve(people, budget)
