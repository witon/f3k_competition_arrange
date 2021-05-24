import pyodbc
import hashlib


class GliderScoreWrap:
    gliderscore_db_path = ""
    cursor = None
    conn = None
    def __init__(self, db_file_path):
        self.gliderscore_db_path = db_file_path
        return
 
    def connect(self):
        try:
            self.conn = pyodbc.connect(u'Driver={Microsoft Access Driver (*.mdb)};DBQ=' + self.gliderscore_db_path)
            self.cursor = self.conn.cursor()
        except :
            return False
        return True

    def close(self):
        if self.cursor != None:
            self.cursor.close()
            self.cursor = None
        if self.conn != None:
            self.conn.close()
            self.conn = None

    def remove_pilot_by_no(self, pilot_no):
        sql = 'delete from [Pilots] where [PilotNo]=?'
        try:
            self.conn.execute(sql, (pilot_no))
        except:
            return False
        return True

    def get_pilot_no_by_name(self, first_name, last_name):
        sql = 'select PilotNo from [Pilots] where [FirstName]=? and [LastName]=?'
        try:
            self.cursor.execute(sql, (first_name, last_name))
        except:
            return None
        data = self.cursor.fetchall()
        if len(data) != 0:
            return data[0][0]
        return None

    def _get_max_competition_no(self):
        sql = 'select max(CompNo) from Comps'
        try:
            self.cursor.execute(sql)
        except:
            return None
        data = self.cursor.fetchall()
        if len(data) != 0:
            return data[0][0]
        return 1
        
 
        
    def add_pilot(self, first_name, last_name):
        pilot_no = self.get_pilot_no_by_name(first_name, last_name)
        if pilot_no != None:
            return pilot_no
        
        sql = 'select max(PilotNo) from Pilots'
        try:
            self.cursor.execute(sql)
        except:
            return None
        data = self.cursor.fetchall()
        pilot_no = 1
        if len(data) != 0:
            pilot_no = data[0][0] + 1
        sql = 'insert into [Pilots] (PilotNo, FirstName, LastName) values(?, ?, ?)'
        try:
            self.conn.execute(sql, (pilot_no, first_name, last_name))
            self.conn.commit()
        except:
            return None
        return pilot_no
    
    def remove_competition_by_no(self, competition_no):
        sql = 'delete from [Comps] where [CompNo]=?'
        sql1 = 'delete from [F3K] where [CompNo]=?'
        try:
            self.conn.execute(sql, (competition_no))
            self.conn.execute(sql1, (competition_no))
            self.conn.commit()
        except:
            return False
        return True
    
    def add_competition(self, name, date, venue):
        competition_no = self._get_max_competition_no()
        if competition_no == None:
            return None 
        competition_no = competition_no + 1
        md5 = hashlib.md5()
        md5.update((name + date + venue).encode('utf-8'))
        competition_id = md5.hexdigest()[0:13]
        sql = "insert into Comps(\
            CompNo, CompName, CompDate, CompVenue, \
            Drop1AtRound, Drop2AtRound, Drop3AtRound, Drop4AtRound, \
            Drop5AtRound, UseTeams, UseTeamProtection, UseClasses, \
            UseModels, UsePilotNumbering, Enforce20KHz, GroupScoreDecimals, \
            ScoresLocked, NbrForTeamScore, CompSeriesNo, printCountry, \
            RoundOrTruncate, GroupScoreOption, printRegistration, UseRoles, \
            BadgeSpecs, DropScoreOption, MergedComps, CompID, \
            IsPublic, AssignHelpers, AudioProfileDT, AudioProfileAP, \
            AudioProfileBT, DrawMode, GSCompClass, WasLastUploadPublic, \
            PrelimCompNo, F3QDrop6to10) \
            values(?, ?, ?, ?, \
            99, 99, 99, 99, \
            99, 0, 0, 0, \
            0, 0, -1, 0, \
            0, 2, 0, 0, \
            1, 1, 0, 0, \
            '', 0, '', ?, \
            0, 0, 'AudioProfileDT1', 'AudioProfileAP1', \
            'AudioProfileBT1', 0, 'F3K', 'NotUploaded', \
            -1, '99,99,99,99,99' \
            )"
        try:
            self.conn.execute(sql, (competition_no, name, date, venue, competition_id))
        except:
            return None

        sql = "insert into F3K( \
            CompNo, f3kGroupsPerRound, f3kPilotsMax, f3kPilotsMin, \
            f3kDrawLocked, f3kAllowBackToBack, f3kDecimalsForTiming) \
            values( \
            ?, 2, 15, 'TmProt=False&Enf20kHz=True&LaneOpt=0&Back2Back=True&NbrPlts=8&GrpsInRnd=2&NbrRnds=0&', \
            0, 0, 0)"
        try:
            self.conn.execute(sql, (competition_no))
            self.conn.commit()
        except:
            return None
        return competition_no
    
    def set_competition_drop_by_no(self, competition_no, round_of_drop1=None, round_of_drop2=None, round_of_drop3=None, round_of_drop4=None, round_of_drop5=None):
        if round_of_drop1 == None:
            round_of_drop1 = 99
        if round_of_drop2 == None:
            round_of_drop2 = 99
        if round_of_drop3 == None:
            round_of_drop3 = 99
        if round_of_drop4 == None:
            round_of_drop4 = 99
        if round_of_drop5 == None:
            round_of_drop5 = 99
        sql = "update Comps set Drop1AtRound=?, Drop2AtRound=?, Drop3AtRound=?, Drop4AtRound=?, Drop5AtRound=? where CompNo=?"
        try:
            self.conn.execute(sql, (round_of_drop1, round_of_drop2, round_of_drop3, round_of_drop4, round_of_drop5, competition_no))
            self.conn.commit()
        except:
            return False
        return True

    def is_competition_pilot_exist(self, competition_no, pilot_no):
        sql = "select * from CompPilots where CompNo=? and PilotNo=?"
        try:
            self.cursor.execute(sql, (competition_no, pilot_no))
        except:
            return False, None
        data = self.cursor.fetchall()
        if len(data) == 0:
            return True, False
        return True, True

    def remove_competition_pilot(self, competition_no, pilot_no):
        sql = 'delete from CompPilots where CompNo=? and PilotNo=?'
        try:
            self.conn.execute(sql, (competition_no, pilot_no))
            self.conn.commit()
        except:
            print("except")
            return False
        return True
    
    def add_pilot_to_competition(self, competition_no, pilot_no):
        ret, is_exist = self.is_competition_pilot_exist(competition_no, pilot_no)
        if not ret:
            return False
        if is_exist:
            return True
        sql = "insert into CompPilots ( \
            CompNo, PilotNo, PilotClass, Team, \
            DrawFreq, Retired, StartNo, Model, \
            Role, IsPilot, OmitFromTeamScore, ModelData) \
            values( \
            ?, ?, '', 0, \
            '2.4', 0, 0, '', \
            'Plt', -1, 0, -1)"
        effect_row = 0
        try:
            effect_row = self.conn.execute(sql, (competition_no, pilot_no)).rowcount
            self.conn.commit()
        except:
            return False
        return effect_row == 1

    def get_competition_no(self, name, date, venue):
        sql = 'select CompNo from [Comps] where [CompName]=? and [CompDate]=? and [CompVenue]=?'
        try:
            self.cursor.execute(sql, (name, date, venue))
        except:
            return None
        data = self.cursor.fetchall()
        if len(data) != 0:
            return data[0][0]
        return None

    def add_pilots_score_record(self, pilot_nos, competition_no, round, group):
        sql = "insert into Scores( \
            CompNo, TaskNo, RoundNo, GroupNo, \
            ReFlightNo, PilotNo, SeqNo, DrawFreq, \
            Laps, Time1Mins, Time1Secs, Time2Mins, \
            Time2Secs, FlightScoreDeduction, Landing, RawScore, \
            NormalisedScore, Penalty, OriginalRoundNo, ScoresChecked, \
            Updated, LandingOver75m, ModelID, \
            Flight1, Flight2, Flight3, Flight4) values (\
            ?, 5, ?, ?, \
            0, ?, ?, 2.4, \
            0, 0, 0, 0, \
            0, 0, 0, 0, \
            0, 0, ?, 0, \
            False, 0, '', \
            '', '', '', '')"
        #try:
        index = 1
        for pilot_no in pilot_nos:
            print(competition_no, round, group, pilot_no, index, round)
            self.conn.execute(sql, (competition_no, round, group, \
                pilot_no, index, \
                round))
        self.conn.commit()
        #except:
        return False
        return True
 

if __name__ == '__main__':
    unittest.main()