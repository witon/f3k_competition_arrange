import pyodbc
import sys, os, getopt
from gliderscore_wrap import GliderScoreWrap
from common import get_rounds_from_input

class SetupGliderScoreCompetition:
    input_file_path = ""
    gliderscore_db_path = ""
    competition_name = ""
    competition_date = ""
    competition_venue = ""
    gliderscore_wrap = None

    @staticmethod
    def split_name(name):
        if len(name) <= 1:
            return "", name
        return  name[1:], name[0:1]
        
    @staticmethod
    def print_help():
        print(sys.argv[0] + ' -i <inputfile> -o <gliderscore db file> -n <competition name> -d <date> -v <venue>')

    def parse_argv(self, argv):
        try:
            opts, args = getopt.getopt(argv, "hi:o:n:d:v:", ["ifile=", "odb=", "nname=", "ddate=", "vvenue="])
        except getopt.GetoptError:
            return False
        for opt, arg in opts:
            if opt == '-h':
                return False
            elif opt in ("-i", "--ifile"):
                self.input_file_path = arg
            elif opt in ("-o", "--odb"):
                self.gliderscore_db_path = arg
            elif opt in ("-n", "--nname"):
                self.competition_name = arg
            elif opt in ("-d", "--ddate"):
                self.competition_date = arg
            elif opt in ("-v", "--vvenue"):
                self.competition_venue = arg
    
        if (self.input_file_path == '' and sys.stdin.isatty()) or self.gliderscore_db_path == '' or self.competition_name == '' or self.competition_date == '' :
            return False
        return True
    
    @staticmethod
    def get_competitors_from_rounds(rounds):
        competitors_set = set()
        for round in rounds:
            for competitor in round[2]:
                competitors_set.add(competitor)
        return list(competitors_set)

    def add_competitors_to_db(self, competitors):
        for competitor in competitors:
            first_name, last_name = self.split_name(competitor)
            self.gliderscore_wrap.add_pilot(first_name, last_name)

    def add_competition(self):
        return self.gliderscore_wrap.add_competition(self.competition_name, self.competition_date, self.competition_venue)
    
    def add_pilots_to_competition(self, competition_no, pilots):
        for pilot_name in pilots:
            first_name, last_name = self.split_name(pilot_name)
            pilot_no = self.gliderscore_wrap.get_pilot_no_by_name(first_name, last_name)
            if pilot_no == None:
                return False
            if not self.gliderscore_wrap.add_pilot_to_competition(competition_no, pilot_no):
                return False
        return True

    def add_pilot_scores(self, competition_no, rounds):
        for round in rounds:
            print(round)
            round_no = round[0]
            group_no = round[1]
            competitors = round[2]
            pilot_nos = []
            for competitor in competitors:
                print(competitor)
                first_name, last_name = self.split_name(competitor)
                pilot_no = self.gliderscore_wrap.get_pilot_no_by_name(first_name, last_name)
                if pilot_no == None:
                    return False
                pilot_nos.append(pilot_no)
            self.gliderscore_wrap.add_pilots_score_record(pilot_nos, competition_no, round_no, group_no)
        return True

    def proc(self):
        if not os.path.exists(self.gliderscore_db_path):
            print("gliderscore db file " + self.gliderscore_db_path + " isn't exist.")
            return False
        self.gliderscore_wrap = GliderScoreWrap(self.gliderscore_db_path)
        if not self.gliderscore_wrap.connect():
            print("connect to db failed.")
            return False

        competition_no = self.gliderscore_wrap.get_competition_no(self.competition_name, self.competition_date, self.competition_venue)
        if competition_no != None:
            print("competition is exist")
            return False
        rounds = get_rounds_from_input(self.input_file_path)
        all_competitors = self.get_competitors_from_rounds(rounds)
        self.add_competitors_to_db(all_competitors)
        competition_no = self.add_competition()
        if competition_no == None:
            print("add competition failed")
            return False
        if not self.add_pilots_to_competition(competition_no, all_competitors):
            print("add pilots to competition failed")
            return False
        if not self.add_pilot_scores(competition_no, rounds):
            print("add pilots' score failed")
            return False
        self.gliderscore_wrap.close()
        return True

        

def main(argv):
    setup = SetupGliderScoreCompetition()
    if not setup.parse_argv(argv):
        setup.print_help()
        exit(0)
    setup.proc()

   
if __name__ == '__main__':
    main(sys.argv[1:])