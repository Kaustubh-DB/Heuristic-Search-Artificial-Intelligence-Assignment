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
def dist_calc(start_cty, end_cty):
    #    lv_strt_cty = list()
    # print(gv_cty_gps_lst)
    lv_strt_cty = list(filter(lambda lv_strt_cty: start_cty in lv_strt_cty, gv_cty_gps_lst))
    lv_end_cty = list(filter(lambda lv_end_cty: end_cty in lv_end_cty, gv_cty_gps_lst))
    if lv_strt_cty or lv_end_cty:
        #        print("in dist calc if")
        #    print(lv_strt_cty)
        start_cty_loc = (float(lv_strt_cty[0][1]), float(lv_strt_cty[0][2]))

        #    print(lv_end_cty)
        end_cty_loc = (float(lv_end_cty[0][1]), float(lv_end_cty[0][2]))
        #    print(start_cty_loc, end_cty_loc)
        # print(lv_strt_cty)
        return haversine(start_cty_loc, end_cty_loc, unit=Unit.MILES)
    return 0


# A* search
def A_star_srch():
    if gv_strt_cty == gv_end_cty:
        return True
    route_queue = Q.PriorityQueue()
    #    route_queue.put((7, gv_strt_cty))
    child_list = child_succ(gv_strt_cty)
    #    print(child_list[0][0])
    for child in child_list:
        cost = round(dist_calc(child[0], child[1]))
        if cost == 0:
            cost = child[2]
        route_queue.put((cost, child, ""))

    # print (route_queue.queue)
    closed = []
    #    i = 0
    #    print(route_queue.empty())
    while not route_queue.empty():
        (cost, curr_stop, route) = route_queue.get()

        if (curr_stop[1] == gv_end_cty or curr_stop[0] == gv_end_cty):
            #            print( curr_stop[2], curr_stop[1])
            return route
        print(curr_stop)
        child_list = child_succ(curr_stop[1])
        #        print(child_list)
        for next_stop in child_list:
            #            print(next_stop)
            temp = 0
            if next_stop not in closed:
                val1 = next_stop[0].find('Jct')
                val2 = next_stop[1].find('Jct')
                #                print(val1,val2)
                if val1 == -1 and val2 == -1:
                    #                    print(next_stop)
                    temp = round(dist_calc(next_stop[0], next_stop[1]))
                if temp == 0:
                    temp = int(next_stop[2])
                cost = cost + temp
                route_queue.put((cost, next_stop, route + next_stop[0]))
        #                print(route_queue.queue)

        #        closed.insert(curr_stop[1])
        ##            check = list(filter(lambda check:next_stop in check, closed))
        ##            if not check :
        ##                continue
        ##            #cost function call
        ##            #1. distance
        ##            cost = cost + dist_calc(curr_stop,next_stop)
        ##            insert in pqueue (cost, details of child)
        ##         put curr_stop in closed
        #                print(next_stop)
        #                route_queue.put(i, next_stop)
        #                i=i+1
        closed.append(curr_stop[1])
    #        print(curr_stop[1])


#    print(route_queue.queue)


# Main Function
if __name__ == "__main__":
    gv_strt_cty = sys.argv[1]
    gv_end_cty = sys.argv[2]
    gv_cst_func = sys.argv[3].lower()
    parse_document()
    gv_total_dist = round(dist_calc(gv_strt_cty, gv_end_cty))
    print(gv_total_dist)
    res = A_star_srch()
    print(res)
#    print(gv_rd_seg_lst,"\n\n",gv_cty_gps_lst) #testing line
# lv_child_succ_lst = child_succ()
# print(lv_child_succ_lst,gv_end_cty)
