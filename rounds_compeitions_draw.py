#!/usr/bin/python
# encoding:utf-8

import itertools
import random
import sys
import io
import getopt
import string
import math
from common import get_output_file, get_competitors_from_input

input_file_path = ''
output_file_path = ''
flight_num = 0
round_num = 0

def rounds_competitors_draw(competitors, flight_num):
    i = itertools.combinations(competitors, flight_num)
    return list(i)

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


def write_to_output(rounds_competitors, all_competitors):
    global output_file_path
    global round_num
    output_file = get_output_file(output_file_path)
    competitors_set = set(all_competitors)
    loop_count = math.ceil(round_num / len(rounds_competitors))
    count = 0
    for i in range(loop_count):
        for round_competitors in rounds_competitors:
            for competitor in round_competitors:
                output_file.write(competitor)
                output_file.write("|")
            output_file.write("\t")
            round_assistants = list(competitors_set - set(round_competitors))
            for assistant in round_assistants:
                output_file.write(assistant)
                output_file.write("|")
            output_file.write("\n")
            count = count + 1
            if count >= round_num:
                i = loop_count + 1
                break
    if not output_file_path == "" :
        output_file.close()


def main(argv):

    if not parse_argv(argv):
        return
    global input_file_path
    competitors = get_competitors_from_input(input_file_path)
    global flight_num
    rounds_competitors = rounds_competitors_draw(competitors, flight_num)
    random.shuffle(rounds_competitors)
    write_to_output(rounds_competitors, competitors)


if __name__ == '__main__':
    main(sys.argv[1:])