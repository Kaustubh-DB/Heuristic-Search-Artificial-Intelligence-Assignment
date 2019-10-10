#!/usr/local/bin/python3

# put your routing program here!
# User_id : dtolia@iu.edu, kbhalerao@iu.edu, sporedi@iu.edu
# =============List of Functions and descriptions==============================
# @author : Deepali Tolia, Kaustubh Bhalerao, Suyash Poredi
# 1. Main function
#   -we take command line arguments in global variables 
#   -call parse_document function
# 2. parse_document
#   -Called in:
#       main
#   -parse road-segments.txt in gv_rd_seg_lst list structure
#   -parse city-gps.txt in gv_cty_gps_lst list structure 
# 3. child_succ
#   -used filter function of list with lambda function to filter and create a 
#    list of child successor
#   -returns child succesors of city B of the current state
#   -checks and returns for City B in the list for both directions
# 4. Using haversine function of Python 
#   -to calculate the GPS distance between two location which will be used in 
#    A* search heuristic
#   -
#   -
# =============================================================================
# ==============List structure and names and purpose===========================
# @author : Deepali Tolia
# Last Changed 27/09/2019
# =============================================================================
import math
import sys
import queue as Q
from haversine import haversine, Unit

# Global variable
gv_strt_cty = ""
gv_end_cty = ""
gv_cst_func = ""
gv_rd_seg_lst = []
gv_cty_gps_lst = []
gv_total_dist = 0


# Parse the text files with data
def parse_document():
    with open("road-segments.txt", "r") as f:
        for line_strip in f.readlines():
            gv_rd_seg_lst.append(line_strip.split())
    with open("city-gps.txt", "r") as f:
        for line_strip in f.readlines():
            gv_cty_gps_lst.append(line_strip.split())

        # all possible next route for reaching goal state


def child_succ(city_B):
    lv_child_lst = list()
    lv_child_lst = (list(filter(lambda child: city_B in child, gv_rd_seg_lst)))
    # print(lv_child_lst)
    return lv_child_lst


# haversine distance for two locations
#Reference https://stackoverflow.com/questions/44743075/calculate-the-distance-between-two-coordinates-with-python
def haversineDistance(origin,destination):
    lat1, lon1 = origin
    lat2, lon2 = destination
    radius = 6371 * 0.62  # miles

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d

def dist_calc(start_cty, end_cty):
    #    lv_strt_cty = list()
    # print(gv_cty_gps_lst)
    lv_strt_cty = list(filter(lambda lv_strt_cty: start_cty in lv_strt_cty, gv_cty_gps_lst))
    lv_end_cty = list(filter(lambda lv_end_cty: end_cty in lv_end_cty, gv_cty_gps_lst))
    if lv_strt_cty and lv_end_cty:
        #        print("in dist calc if")
        #    print(lv_strt_cty)
        start_cty_loc = (float(lv_strt_cty[0][1]), float(lv_strt_cty[0][2]))

        #    print(lv_end_cty)
        end_cty_loc = (float(lv_end_cty[0][1]), float(lv_end_cty[0][2]))
        #    print(start_cty_loc, end_cty_loc)
        # print(lv_strt_cty)
        return haversineDistance(start_cty_loc, end_cty_loc)
    return 0


# A* search
def A_star_srch():
    if gv_strt_cty == gv_end_cty:
        return True
    route_queue = Q.PriorityQueue()
    child_list = child_succ(gv_strt_cty)
    seg = 0
    distance = 0
    hours = 0
    tgg = 0
    for child in child_list:
        if child[1] == gv_strt_cty:
            child[1] = child[0]
            child[0] = gv_strt_cty
        if gv_cst_func == 'distance':
            cost = 0
            # cost = round(dist_calc(child[1], gv_end_cty))
            cost = int(child[2])
            if cost == 0:
                cost = int(child[2])
        if gv_cst_func == 'segments':
            cost = 1
        if gv_cst_func == 'time':
            time = int(child[2]) / int(child[3])
            cost = time
        distance = int(child[2])
        route_queue.put((cost, seg, distance, hours, tgg, child, gv_strt_cty + ' '))
    closed = []

    while not route_queue.empty():
        (cost, seg, distance, hours, tgg, curr_stop, route) = route_queue.get()

        if (curr_stop[0] == gv_end_cty or curr_stop[1] == gv_end_cty):
            print(seg, distance, hours, tgg, route+gv_end_cty)
            return True
            # return seg, distance, hours, tgg, route+gv_end_cty
        child_list = child_succ(curr_stop[1])
        closed.append(curr_stop)
        for next_stop in child_list:
            next_seg = next_distance = next_hours = next_tgg = next_cost = 0
            if next_stop in closed:
                continue
            if next_stop[1] == curr_stop[1]:
                temp_name = next_stop[1]
                next_stop[1] = next_stop[0]
                next_stop[0] = temp_name
            if gv_cst_func == 'distance':
                temp = 0
                temp = round(dist_calc(next_stop[1], gv_end_cty))
                if temp == 0:
                    temp = int(next_stop[2])
                next_cost = int(cost) + temp
            elif gv_cst_func == 'segments':
                next_cost = int(cost) + 1
            elif gv_cst_func == 'time':
                time = int(next_stop[2])/int(next_stop[3])
                next_cost = float(cost) + time
            temp_dist = 0
            temp_dist = round(dist_calc(next_stop[0], next_stop[1]))
            if temp_dist == 0:
                temp_dist = int(next_stop[2])
            next_distance = distance + temp_dist
            next_seg = seg + 1
            next_hours = hours + (int(next_stop[2]) / int(next_stop[3]))
            route_queue.put((next_cost, next_seg, next_distance, next_hours, next_tgg, next_stop, route + next_stop[0] + ' '))


# Main Function
if __name__ == "__main__":
    gv_strt_cty = sys.argv[1]
    gv_end_cty = sys.argv[2]
    gv_cst_func = sys.argv[3].lower()
    if gv_cst_func != 'distance' and gv_cst_func != 'time' and gv_cst_func != 'segments' and gv_cst_func != 'mpg':
        print("Please enter a Valid cost function")
        exit(1)
    parse_document()
    # gv_total_dist = round(dist_calc(gv_strt_cty,gv_end_cty))
    # print("actual " ,gv_total_dist)
    # res = \
    A_star_srch()
    # print(res)