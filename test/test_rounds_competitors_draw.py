import unittest
import rounds_competitors_draw

class TestRoundsCompetitorsDraw(unittest.TestCase):
    def test_draw(self):
        draw = rounds_competitors_draw.RoundsCompetitorsDraw()
        competitors = ['a', 'b', 'c', 'd', 'e', 'f']
        draw.set_competitors(competitors)
        groups_pilot_num = [4, 2]
        draw.set_groups_pilot_num(groups_pilot_num)
        rounds = draw.draw(10)
        for round in rounds:
            print(round)

