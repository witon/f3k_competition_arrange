import unittest
import gliderscore_wrap

class TestGliderScoreWrap(unittest.TestCase):
    def test_connect(self):
        gw = gliderscore_wrap.GliderScoreWrap("test/test.mdb")
        ret = gw.connect()
        self.assertTrue(ret)
        gw.close()

    def test_add_and_get_and_remove_pilot(self):
        gw = gliderscore_wrap.GliderScoreWrap("test/test.mdb")
        gw.connect()
        first_name = "test first name"
        last_name = "test last name"
        pilot_no = gw.add_pilot(first_name, last_name)
        self.assertTrue(pilot_no != None)
        ret = gw.remove_pilot_by_no(pilot_no)
        self.assertTrue(ret)
        pilot_no = gw.get_pilot_no_by_name(first_name, last_name)
        self.assertTrue(pilot_no == None)
        gw.close()

    def test_del_and_add_pilot(self):
        gw = gliderscore_wrap.GliderScoreWrap("test/test.mdb")
        ret = gw.connect()
        self.assertTrue(ret)
        gw.close()

    def test_add_and_get_no_and_set_drop_and_remove_competition(self):
        gw = gliderscore_wrap.GliderScoreWrap("test/test.mdb")
        ret = gw.connect()
        self.assertTrue(ret)

        competition_no = gw.add_competition("test name", "2021/5/21", "test avenue")
        self.assertTrue(competition_no != None)

        competition_no_got = gw.get_competition_no("test name", "2021/5/21", "test avenue")
        self.assertEqual(competition_no, competition_no_got)

        ret = gw.set_competition_drop_by_no(competition_no, 1, 2, 3, 4, 5)
        self.assertTrue(ret)

        ret = gw.remove_competition_by_no(competition_no)
        self.assertTrue(ret)

        gw.close()

    def test_add_pilot_to_competition(self):
        gw = gliderscore_wrap.GliderScoreWrap("test/test.mdb")
        ret = gw.connect()
        self.assertTrue(ret)
        ret = gw.add_pilot_to_competition(100, 103)
        self.assertTrue(ret)
        ret = gw.remove_competition_pilot(100, 103)
        self.assertTrue(ret)
        gw.close()
