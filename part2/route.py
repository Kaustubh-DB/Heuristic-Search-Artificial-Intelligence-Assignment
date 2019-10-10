#!/usr/local/bin/python3

# put your routing program here!
# User_id : dtolia@iu.edu, kbhalerao@iu.edu, sporedi@iu.edu
# =============List of Functions and descriptions==============================
# @author : Deepali Tolia, Kaustubh Bhalerao, Suyash Poredi
# 1. Main function
#   -we take command line arguments in global variables 
#   -call parse_document function
# 2. parse_document()
#   -Called in:
#       main
#   -parse road-segments.txt in gv_rd_seg_lst list structure
#   -parse city-gps.txt in gv_cty_gps_lst list structure 
# 3. child_succ()
#   -used filter function of list with lambda function to filter and create a 
#    list of child successor
#   -returns child succesors of city B of the current state
#   -checks and returns for City B in the list for both directions
# 4. Using haversine function of Python directly
#   -the haversine module is not available on SICE server - added a function for it haversineDistance()
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

# Global variable
gv_strt_cty = ""
gv_end_cty = ""
gv_cst_func = ""
gv_rd_seg_lst = []
gv_cty_gps_lst = []

# Parse the text files with data
def parse_document():
    with open("road-segments.txt", "r") as f:
        for line_strip in f.readlines():
            gv_rd_seg_lst.append(line_strip.split())
    with open("city-gps.txt", "r") as f:
        for line_strip in f.readlines():
            gv_cty_gps_lst.append(line_strip.split())

# all possible next route for reaching goal state, Successor states
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
    lv_strt_cty = list(filter(lambda lv_strt_cty: start_cty in lv_strt_cty, gv_cty_gps_lst))
    lv_end_cty = list(filter(lambda lv_end_cty: end_cty in lv_end_cty, gv_cty_gps_lst))
    if lv_strt_cty and lv_end_cty:
        start_cty_loc = (float(lv_strt_cty[0][1]), float(lv_strt_cty[0][2]))
        end_cty_loc = (float(lv_end_cty[0][1]), float(lv_end_cty[0][2]))
        return haversineDistance(start_cty_loc, end_cty_loc)
    return 0

#Cost Calculation function
def cost_calc(cost, next_stop):
    if gv_cst_func == 'distance':
        temp = 0
        temp = round(dist_calc(next_stop[1], gv_end_cty))
        if temp == 0:
            temp = int(next_stop[2])
        return int(cost) + temp
    elif gv_cst_func == 'segments':
        return int(cost) + 1
    elif gv_cst_func == 'time':
        time = int(next_stop[2]) / int(next_stop[3])
        return float(cost) + time
    elif gv_cst_func == 'mpg':
        mpg = (400.0 * (float(next_stop[3]) / 150.0)) * (float((1 - (float(next_stop[3]) / 150))) ** 4)
        return float(cost) + mpg

# A* search
def A_star_srch():
    if gv_strt_cty == gv_end_cty:
        print(0, 0, 0, 0, gv_strt_cty)
        return True
    route_queue = Q.PriorityQueue()
    child_list = child_succ(gv_strt_cty)
    seg = distance = hours = tgg = 0
    for child in child_list:
        if child[1] == gv_strt_cty:
            child[1] = child[0]
            child[0] = gv_strt_cty
        if gv_cst_func == 'distance':
            cost = int(child[2])
        elif gv_cst_func == 'segments':
            cost = 1
        elif gv_cst_func == 'time':
            time = int(child[2]) / int(child[3])
            cost = time
        elif gv_cst_func == 'mpg':
            cost = (400.0 * (float(child[3]) / 150)) * (float((1 - (float(child[3] )/ 150)))**4)
        distance = int(child[2])
        seg = 1
        hours = (int(child[2]) / int(child[3]))
        tgg = float(child[2])/((400.0*(float(child[3])/150.0))*(float((1-(float(child[3])/150)))**4))
        route_queue.put((cost, seg, distance, hours, tgg, child, gv_strt_cty + ' '))
    closed = []

    while not route_queue.empty():
        #Get current state
        (cost, seg, distance, hours, tgg, curr_stop, route) = route_queue.get()
        #Goal state found
        if (curr_stop[0] == gv_end_cty or curr_stop[1] == gv_end_cty):
            print(seg, distance, hours, tgg, route+gv_end_cty)
            return True
            # return seg, distance, hours, tgg, route+gv_end_cty
        #add current state in visited/closed
        closed.append(curr_stop)
        #Get successor state and loop on it
        child_list = child_succ(curr_stop[1])
        for next_stop in child_list:
            next_seg = next_distance = next_hours = next_tgg = next_cost = 0
            #Visisted condition/Closed condition
            if next_stop in closed:
                continue
            #handling bidirectional
            if next_stop[1] == curr_stop[1]:
                temp_name = next_stop[1]
                next_stop[1] = next_stop[0]
                next_stop[0] = temp_name
            #cost calculation
            next_cost = cost_calc(cost, next_stop)
            #distance calc
            next_distance = distance + int(next_stop[2])
            #segment calculation
            next_seg = seg + 1
            #hours calculation
            next_hours = hours + (int(next_stop[2]) / int(next_stop[3]))
            #total gas gallons calculation
            mpg = (400.0*(float(next_stop[3])/150.0))*(float((1-(float(next_stop[3])/150)))**4)
            next_tgg = tgg + (float(next_stop[2])/mpg)
            #put the calculated details for the child in the route with the cost
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
    A_star_srch()