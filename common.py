import sys
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
 
def get_output_file(output_file_path):
    output_file = None
    if output_file_path == "":
        output_file = sys.stdout
    else:
        output_file = open(output_file_path, 'w',  encoding='UTF-8')

    if output_file == None:
        return None
    return output_file