"""Offline tests of the wave points, the wave scale and the Imbituba parser:
python3 -m unittest discover -s tools -p "test_*.py" """
import os
import sys
import tempfile
import unittest
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import build_scale  # noqa: E402
import check_seeds  # noqa: E402
import ciram_parse_core as ciram  # noqa: E402
from tools.lib import openmeteo as om  # noqa: E402


def year(hs, tp, hours=4380):
    """A year's answer: `hours` daylight hours with these waves."""
    return {"hourly": {"time": ["2025-01-01T12:00"] * hours, "wave_height": [hs] * hours, "wave_period": [tp] * hours}}


class Scale(unittest.TestCase):
    def test_a_land_cell_is_not_a_scale(self):
        self.assertIsNone(build_scale.scale(year(0.0, 0.0)))        # what GFS answers on land since 5/2025
        self.assertIsNone(build_scale.scale(year(0.2, 8.0)))
        self.assertIsNone(build_scale.scale(year(2.0, 3.0)))
        self.assertIsNone(build_scale.scale(year(2.0, 10.0, hours=2160)))

    def test_rocha_keeps_the_scale_of_the_world(self):
        top, per, hs, tp, n = build_scale.scale(year(2.04, 11.3))
        self.assertEqual((top, per, hs, tp, n), (1.8, 13.0, 2.04, 11.3, 4380))

    def test_the_published_scales_were_measured_at_sea(self):
        errors = []
        check_seeds.check_scale(errors)
        self.assertEqual(errors, [])


class WavePoints(unittest.TestCase):
    """A beach at (0, 0), its own cell land. There is sea to the north (lat > 0.1) and past lon 0.3:
    the nearest sea cell is (0.25, 0), straight north, 28 km away."""
    def setUp(self):
        self.answers = {(0.0, 0.0): (None, (0.0, 0.0))}      # (lat, lon) -> (height, cell): what the API does
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        for p in (mock.patch.object(om, "CACHE", tmp.name),
                  mock.patch.object(om, "_get", self.get),
                  mock.patch.object(om, "_is_sea", lambda lat, lon: lat > 0.1 or lon > 0.3),
                  mock.patch.object(om.time, "sleep", lambda s: None)):
            p.start()
            self.addCleanup(p.stop)

    def get(self, model, points):
        out = []
        for p in points:
            h, cell = self.answers.get(p, (1.0, p))
            out.append({"latitude": cell[0], "longitude": cell[1], "current": {"wave_height": h}})
        return out

    def test_the_nearest_in_front_not_the_nearest(self):
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [90]), [(0.25, 0.25)])

    def test_without_a_facing_the_nearest(self):
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)]), [(0.25, 0.0)])

    def test_the_swell_window_decides(self):
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [0]), [(0.25, 0.0)])

    def test_a_cell_the_api_moves_is_left_out(self):
        self.answers[(0.25, 0.25)] = (1.0, (0.5, 0.25))                  # Florianópolis: 28 km away
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [90]), [(0.0, 0.5)])

    def test_a_cell_without_waves_is_left_out(self):
        self.answers[(0.25, 0.25)] = (0.0, (0.25, 0.25))
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [90]), [(0.0, 0.5)])

    def test_nothing_in_front_takes_the_nearest(self):
        with mock.patch.object(om, "_is_sea", lambda lat, lon: lat > 0.1):
            self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [180]), [(0.25, 0.0)])

    def test_own_cell_with_waves_needs_no_point(self):
        self.answers[(0.0, 0.0)] = (1.0, (0.0, 0.0))
        self.assertEqual(om.wave_points("ncep_gfswave025", [(0.0, 0.0)], [90]), [None])

    def test_cells_are_kept(self):
        self.answers[(1.0, 1.0)] = (1.0, (0.75, 1.0))
        self.assertEqual(om.cells("ncep_gfswave025", [(1.0, 1.0)]), [(0.75, 1.0)])
        self.assertTrue(om.moved("ncep_gfswave025", (1.0, 1.0), (0.75, 1.0)))
        self.assertFalse(om.moved("ncep_gfswave025", (1.1, 1.0), (1.0, 1.0)))    # the cell it is in
        self.assertFalse(om.moved("ncep_gfswave025", (0.0, 179.95), (0.0, -180.0)))   # across ±180°


def word(x, y, text):
    return (float(x), float(y), float(x) + 20.0, text)


class Imbituba(unittest.TestCase):
    def test_a_column_with_two_extremes(self):
        """January 2026: the fifth column holds only the end of the 31st."""
        page = [word(24, 100, "24/1")]
        for i in range(12):
            page += [word(24, 110 + 10 * i, "%02d:00" % (i * 2)), word(50, 110 + 10 * i, "▲0,5")]
        page += [word(77, 100, "31/1"), word(77, 110, "02:40"), word(103, 110, "▲0,9"), word(77, 120, "08:19"), word(103, 120, "▼0,4")]
        page += [word(131, 100, "13:31"), word(156, 100, "▲0,5"), word(131, 110, "19:59"), word(156, 110, "▼"), word(170, 110, "-0,1")]
        page += [word(10, 20, "2026")]
        with mock.patch.object(ciram, "words", lambda pdf: [page]):
            year, data = ciram.parse("x.pdf")
        self.assertEqual(year, 2026)
        self.assertEqual(sorted(data[(1, 31)]), [(2, 40, 0.9, True), (8, 19, 0.4, False), (13, 31, 0.5, True), (19, 59, -0.1, False)])
        self.assertEqual(len(data[(1, 24)]), 12)
        self.assertFalse([p for p in ciram.problems(year, data) if "fuera de orden" in p])

    def test_problems(self):
        ok = {(1, 1): [(2, 0, 0.5, True), (8, 0, 0.1, False)], (1, 2): [(0, 0, 0.5, True)]}
        self.assertEqual(ciram.problems(2026, ok), [])
        gap = {(1, 31): [(8, 19, 0.4, False)], (2, 1): [(3, 1, 0.8, True)]}
        self.assertIn("18.7 h", ciram.problems(2026, gap)[0])
        diurnal = {(5, 8): [(23, 31, 0.7, True)], (5, 9): [(14, 10, 0.3, False)]}     # 14.6 h, real
        self.assertEqual(ciram.problems(2026, diurnal), [])
        order = {(1, 24): [(4, 59, 0.6, True), (13, 31, 0.5, True), (12, 16, 0.4, False)]}
        self.assertIn("fuera de orden", ciram.problems(2026, order)[0])


if __name__ == "__main__":
    unittest.main()
