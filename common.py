import sys
import re
def get_competitors_from_input(input_file_path):
    competitors = []
    if not sys.stdin.isatty():
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        while True:
            line = input_stream.readline()
            if not line: break
            competitors.append(line.replace("\n", ""))
    elif input_file_path != '' :
        with open(input_file_path, 'r',  encoding='UTF-8') as input_file:
            while True:
                line = input_file.readline()
                if not line: break
                competitors.append(line.replace("\n", ""))
    return competitors

def parse_rounds_one_line(line):
    fields = str.split(line, '|')
    p = re.compile("([0-9]*)\.([0-9]*)")
    matchs = p.findall(fields[0])
    if matchs == None:
        return None, None, None
    
    round = int(matchs[0][0])
    group = int(matchs[0][1])
    competitors = []
    for i in range(1, len(fields)):
        if len(fields[i]) > 0:
            competitors.append(fields[i])
    return round, group, competitors

def proc_rounds_one_line(line, rounds):
    round, group, competitors = parse_rounds_one_line(line.replace("\n", ""))
    if round == None:
        return False
    rounds.append([])
    index = len(rounds) - 1
    rounds[index].append(round)
    rounds[index].append(group)
    rounds[index].append(competitors)
    return True



def get_rounds_from_input(input_file_path):
    rounds = []
    if not sys.stdin.isatty():
        input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        while True:
            line = input_stream.readline()
            if not line: break
            if not proc_rounds_one_line(line, rounds):
                break
    elif input_file_path != '' :
        with open(input_file_path, 'r',  encoding='UTF-8') as input_file:
            while True:
                line = input_file.readline()
                if not line: break
                if not proc_rounds_one_line(line, rounds):
                    break
    return rounds
 
def get_output_file(output_file_path):
    output_file = None
    if output_file_path == "":
        output_file = sys.stdout
    else:
        output_file = open(output_file_path, 'w',  encoding='UTF-8')

    if output_file == None:
        return None
    return output_file