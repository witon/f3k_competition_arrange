#!/usr/bin/python
# encoding:utf-8

import itertools
import random
import sys
import io
import getopt
import string
import math
import rounds_competitors_draw
from common import get_output_file, get_competitors_from_input

input_file_path = ''
output_file_path = ''
flight_num = 0
round_num = 0

#def rounds_competitors_draw(competitors, flight_num):
#    i = itertools.combinations(competitors, flight_num)
#    return list(i)

def print_help():
    print(sys.argv[0] + ' -i <inputfile> -o <outputfile> -n <flight num> -r <round num>')

def parse_argv(argv):
    global flight_num
    global round_num
    global input_file_path
    global output_file_path
    try:
        opts, args = getopt.getopt(argv, "hi:o:n:r:", ["ifile=", "ofile=", "num=", "round="])
    except getopt.GetoptError:
        print_help()
        return False
    for opt, arg in opts:
        if opt == '-h':
            print_help()
            return False
        elif opt in ("-i", "--ifile"):
            input_file_path = arg
        elif opt in ("-o", "--ofile"):
            output_file_path = arg
        elif opt in ("-n", "--num"):
            flight_num = int(arg)
        elif opt in ("-r", "--round"):
            round_num = int(arg)
    if (input_file_path == '' and sys.stdin.isatty()) or flight_num == 0 or round_num == 0:
        print_help()
        return False
    return True


def write_to_output(rounds):
    global output_file_path
    global round_num
    output_file = get_output_file(output_file_path)

    round_index = 1
    for round in rounds:
        group_index = 1
        for group in round:
            output_file.write(str(round_index))
            output_file.write(".")
            output_file.write(str(group_index))
            output_file.write("|")
            for competitor in group:
                output_file.write(competitor)
                output_file.write("|")
            output_file.write("\n")
            group_index = group_index + 1
        round_index = round_index + 1
    if not output_file_path == "" :
        output_file.close()


def main(argv):

    if not parse_argv(argv):
        return
    global input_file_path
    competitors = get_competitors_from_input(input_file_path)
    global flight_num
    draw = rounds_competitors_draw.RoundsCompetitorsDraw()
    random.shuffle(competitors)
    draw.set_competitors(competitors)
    total_pilot_num = len(competitors)
    groups_pilot_num = [flight_num, total_pilot_num - flight_num]
    draw.set_groups_pilot_num(groups_pilot_num)
    rounds = draw.draw(round_num)
    write_to_output(rounds)


if __name__ == '__main__':
    main(sys.argv[1:])