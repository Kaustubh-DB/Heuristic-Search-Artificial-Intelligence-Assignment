#!/usr/local/bin/python3
#
# choose_team.py : Choose a team of maximum skill under a fixed budget
#
# Code by: [Kaustubh Bhalerao(kbhaler), Suyash Poredi(sporedi), Dipali Tolia(dtolia)]
#
# Based on skeleton code by D. Crandall, September 2019
#
import sys
from collections import deque


def load_people(filename):
    people = {}
    with open(filename, "r") as file:
        for line in file:
            l = line.split()
            people[l[0]] = [float(i) for i in l[1:]]
    return people


# Class for storing data for each person/robot
class Person:
    def __init__(self, index, name, efficiency_skill, cost):
        self.index = index
        self.name = name
        self.efficiency_skill = efficiency_skill
        self.cost = cost

    def __iter__(self):
        yield self.index
        yield self.name
        yield self.efficiency_skill
        yield self.cost

    def tostring(self):
        print("Index =", self.index )
        print("name =", self.name)
        print("efficiency_skill =", self.efficiency_skill)
        print("cost =", self.cost)

class PersonState:
    def __init__(self, level_index,name, efficiency_skill, cost, people):
        self.level_index = level_index
        self.name = name
        self.efficiency_skill = efficiency_skill
        self.cost = cost
        self.peoples = people

    def __iter__(self):
        yield self.level_index
        yield self.name
        yield self.efficiency_skill
        yield self.cost
        yield self.peoples

    def tostring(self):
        print("Index =", self.level_index )
        print("name =", self.name)
        print("efficiency_skill =", self.efficiency_skill)
        print("cost =", self.cost)
        print("peoples =", self.peoples)

# This function gives solution using Knapsack Branch and Bound 
def approx_solve_branchandbound(people, budget):

    for (person, (skill, cost)) in people.items():
        name_list.append(person)
        cost_list.append(cost)
        efficiency.append(skill)

    item_count = len(cost_list)

    capacity = budget

    items = []

    for i in range(1, item_count + 1):
        name_value = name_list.__getitem__(i - 1)
        cost_value = float(cost_list.__getitem__(i - 1))
        skill_value = float(efficiency.__getitem__(i - 1))

        item = Person(i-1, name_value, skill_value, cost_value)

        #items.append(Item(i - 1, name_value, float(skill_value), float(cost_value)))
        items.append(item)
        # print(items)

    # sorting Item on basis of cost per efficiency skill.
    items = sorted(items, key=lambda x: x.cost / x.efficiency_skill)

    node = PersonState(-1, '', 0, 0, [])

    v = node
    Q = deque([])
    Q.append(v)

    maxValue = 0
    choosen_team = []
    while (len(Q) != 0):
        # Dequeue a node
        v = Q[0]
        # print(Q)
        Q.popleft()

        u = PersonState(None, None, None, None, [])

        u.level_index = v.level_index + 1
        u.name = items[u.level_index].name
        u.cost = v.cost + items[u.level_index].cost
        u.efficiency_skill = v.efficiency_skill + items[u.level_index].efficiency_skill
        u.peoples = list(v.peoples)
        u.peoples.append(items[u.level_index].index)

        if (u.cost <= capacity and u.efficiency_skill > maxValue):
            maxValue = u.efficiency_skill
            choosen_team = u.peoples

        bound_u = calculate_bound(u, capacity, item_count, items)
        if (bound_u > maxValue):
            Q.append(u)

        u = PersonState(None, None, None, None, [])
        u.level_index = v.level_index + 1
        u.cost = v.cost
        u.efficiency_skill = v.efficiency_skill
        u.peoples = list(v.peoples)

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
        result = u.efficiency_skill
        j = u.level_index + 1
        totalweight = u.cost

        while (j < item_count and totalweight + items[j].cost <= capacity):
            totalweight = totalweight + items[j].cost
            result = result + items[j].efficiency_skill
            j = j + 1

        k = j
        if (k <= item_count - 1):
            result = result + (capacity - totalweight) * items[k].efficiency_skill / items[k].cost

        return result

# This function implements a greedy solution to the problem:
#  It adds people in decreasing order of "skill per dollar,"
#  until the budget is exhausted.
#  But this search technique may not give an optimal solution for every case

def approx_solve(people, budget):

    solution=()
    for (person, (skill, cost)) in sorted(people.items(), key=lambda x: x[1][0]/x[1][1],reverse=True):
        if budget - cost > 0:
            solution += ( ( person, 1), )
            budget -= cost
        else:
            continue

    print("Found a group with %d people costing %f with total skill %f" % \
          (len(solution), sum(people[p][1] * f for p, f in solution), sum(people[p][0] * f for p, f in solution)))

    for s in solution:
        print("%s %f" % s)


if __name__ == "__main__":

    if (len(sys.argv) != 3):
        raise Exception('Error: expected 2 command line arguments')

    budget = float(sys.argv[2])
    people = load_people(sys.argv[1])
    no_items = len(people)
    cost_list = []
    efficiency = []
    name_list = []

    approx_solve_branchandbound(people, budget)
    # approx_solve(people,budget)
