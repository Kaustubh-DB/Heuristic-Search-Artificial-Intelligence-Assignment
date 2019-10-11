import math
import sys
import queue as q

# Global variable
gv_rd_seg_lst = {}
gv_cty_gps_lst = {}


# Parse the text files with data
def parse_document():
    with open("road-segments.txt", "r") as f:
        for line_strip in f.readlines():
            line = line_strip.strip()
            key, v = line.split(" ", 1)
            value = v.split(" ")
            gv_rd_seg_lst.setdefault(key, []).append(value)
            line = line_strip.strip()
            cty1, cty2, val = line.split(" ", 2)
            value1 = val.split(" ")
            value1.insert(0, cty1)
            # print(value1)
            gv_rd_seg_lst.setdefault(cty2, []).append(value1)
    with open("city-gps.txt", "r") as f:
        for line_strip in f.readlines():
            line = line_strip.strip()
            key, v = line.split(" ", 1)
            value = v.split(" ")
            gv_cty_gps_lst.setdefault(key, []).append(value)


# haversine distance for two locations
# Reference https://stackoverflow.com/questions/44743075/calculate-the-distance-between-two-coordinates-with-python
def haversine_distance(origin, destination):
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


def dist_calc(start_cty, end_cty, lv_cty_gps_lst):
    det_strt_cty = lv_cty_gps_lst.get(start_cty)
    det_end_cty = lv_cty_gps_lst.get(end_cty)
    if det_strt_cty and det_end_cty:
        start_cty_loc = (float(det_strt_cty[0][0]), float(det_strt_cty[0][1]))
        end_cty_loc = (float(det_end_cty[0][0]), float(det_end_cty[0][1]))
        return haversine_distance(start_cty_loc, end_cty_loc)
    return 0


# Cost Calculation function
def cost_calc(cost, next_stop, cst_func, end_cty, lv_cty_gps_lst):
    if cst_func == 'distance':
        temp = 0
        temp = round(dist_calc(next_stop[0], end_cty, lv_cty_gps_lst))
        if temp == 0:
            temp = int(next_stop[1])
        return int(cost) + temp
    elif cst_func == 'segments':
        return int(cost) + 1
    elif cst_func == 'time':
        time = int(next_stop[1]) / int(next_stop[2])
        return float(cost) + time
    elif cst_func == 'mpg':
        mpg = (400.0 * (float(next_stop[2]) / 150.0)) * (float((1 - (float(next_stop[2]) / 150))) ** 4)
        return float(cost) + mpg


# A* search
def a_star_srch(lv_strt_cty, lv_end_cty, lv_cst_func, lv_rd_seg_lst, lv_cty_gps_lst):
    if lv_strt_cty == lv_end_cty:
        print(0, 0, 0, 0, lv_strt_cty)
        return True
    route_queue = q.PriorityQueue()
    rd_seg_lst_get = lv_rd_seg_lst.get
    qput = route_queue.put
    for child in rd_seg_lst_get(lv_strt_cty):
        cost = 0
        if lv_cst_func == 'distance':
            cost = int(child[1])
        elif lv_cst_func == 'segments':
            cost = 1
        elif lv_cst_func == 'time':
            time = int(child[1]) / int(child[2])
            cost = time
        elif lv_cst_func == 'mpg':
            cost = (400.0 * (float(child[2]) / 150)) * (float((1 - (float(child[2]) / 150))) ** 4)

        distance = int(child[1])
        seg = 1
        hours = (int(child[1]) / int(child[2]))
        if lv_cst_func != 'mpg':
            tgg = float(child[1]) / ((400.0 * (float(child[2]) / 150.0)) * (float((1 - (float(child[2]) / 150))) ** 4))
        else:
            tgg = float(child[1]) / cost
        qput((cost, seg, distance, hours, tgg, child, lv_strt_cty))
    closed = []
    closed_append = closed.append
    while not route_queue.empty():
        # Get current state
        (cost, seg, distance, hours, tgg, curr_stop, route) = route_queue.get()
        # Goal state found
        if curr_stop[0] == lv_end_cty:
            print(seg, distance, hours, tgg, route + " " + lv_end_cty)
            return True
        # add current state in visited/closed
        closed_append(curr_stop)
        # print(curr_stop[0])
        # Get successor state and loop on it
        for next_stop in rd_seg_lst_get(curr_stop[0]):
            # Visisted condition/Closed condition
            if next_stop in closed:
                continue
            # cost calculation
            next_cost = cost_calc(cost, next_stop, lv_cst_func, lv_end_cty, lv_cty_gps_lst)
            # distance calc
            next_distance = distance + int(next_stop[1])
            # segment calculation
            next_seg = seg + 1
            # hours calculation
            next_hours = hours + (int(next_stop[1]) / int(next_stop[2]))
            # total gas gallons calculation
            mpg = (400.0 * (float(next_stop[2]) / 150.0)) * (float((1 - (float(next_stop[2]) / 150))) ** 4)
            next_tgg = tgg + (float(next_stop[1]) / mpg)
            # route
            next_route = route + ' {}'.format(curr_stop[0])
            # put the calculated details for the child in the route with the cost
            qput((next_cost, next_seg, next_distance, next_hours, next_tgg, next_stop, next_route))
    print("Inf")

import time
# Main Function
if __name__ == "__main__":
    start_city = sys.argv[1]
    end_city = sys.argv[2]
    cost_constraint = sys.argv[3].lower()
    start_time = time.time()
    if cost_constraint != 'distance' and cost_constraint != 'time' and cost_constraint != 'segments' and cost_constraint != 'mpg':
        print("Please enter a Valid cost function")
        exit(1)
    parse_document()
    a_star_srch(start_city, end_city, cost_constraint, gv_rd_seg_lst, gv_cty_gps_lst)
    print("--- %s seconds ---" % (time.time() - start_time))
