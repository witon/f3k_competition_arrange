#!/usr/bin/python
# encoding:utf-8

import itertools
import random
import math

class RoundsCompetitorsDraw:
    competitors = None
    groups_pilot_num = None

    def __init__(self):
        return

    def set_competitors(self, competitors):
        self.competitors = competitors

    def set_groups_pilot_num(self, groups_pilot_num):
        self.groups_pilot_num = groups_pilot_num
        return

    def draw(self, round_num):
        rounds = []
        if len(self.groups_pilot_num) != 2:
            return None 
        round_index = 0
        
        competitors_set = set(self.competitors)

        combs = list(itertools.combinations(self.competitors, self.groups_pilot_num[0]))

        round_index = 0

        while round_index < round_num:
            for group in combs:
                round_assistants = list(competitors_set - set(group))
                rounds.append([])
                rounds[round_index].append(group)
                rounds[round_index].append(round_assistants)
                round_index = round_index + 1
                if round_index >= round_num:
                    break
        return rounds
