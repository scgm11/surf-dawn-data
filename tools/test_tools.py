"""Offline tests of the wave points, the wave scale and the Imbituba parser:
python3 -m unittest discover -s tools -p "test_*.py" """
import contextlib
import io
import json
import os
import sys
import tempfile
import unittest

import numpy as np
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import armada  # noqa: E402
import build_scale  # noqa: E402
import check_seeds  # noqa: E402
import check_spots  # noqa: E402
import era5_normals as era5  # noqa: E402
import wind  # noqa: E402
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


class CellControl(unittest.TestCase):
    M = "ncep_gfswave025"

    def test_wave_point(self):
        spot, wave = (-27.63, -48.45), (-27.75, -48.5)
        self.assertIn("corre", check_spots.cell_problem(self.M, spot, wave, (-28.0, -48.5), 152))
        self.assertIsNone(check_spots.cell_problem(self.M, spot, (-27.75, -48.25), (-27.75, -48.25), 152))
        self.assertIn("detrás", check_spots.cell_problem(self.M, (-27.4, -48.41), (-27.25, -48.5), (-27.25, -48.5), 84))

    def test_own_position(self):
        spot = (-34.04, -53.54)
        self.assertIsNone(check_spots.cell_problem(self.M, spot, None, (-34.0, -53.5), 94))     # the cell it is in
        self.assertIn("detrás", check_spots.cell_problem(self.M, spot, None, (-34.25, -53.5), 56))
        self.assertIn("km", check_spots.cell_problem(self.M, (-34.0, -53.5), None, (-34.5, -53.5), 180))
        self.assertIsNone(check_spots.cell_problem(self.M, spot, None, (-34.25, -53.5), 170))
        self.assertIn("sin respuesta", check_spots.cell_problem(self.M, spot, None, None, 94))


class FlagshipCutOff(unittest.TestCase):
    """A run cut off while it looks for the flagship spots keeps the rest, with the last run's."""
    ZONE = {"id": "UY-X", "m": ["ncep_gfswave025"], "c": "UY", "s": [["A", -34.0, -53.5, 94, "beach"]]}
    CELLS = [{"region": "UY-X", "spot": "A", "cell": [-34.25, -53.5], "wave": None, "km": 28.0, "why": "detrás"}]
    OLD = {"region": "UY-X", "spot": "A", "lat": -34.0, "lon": -53.5, "status": "ok", "km": 0.1}

    def run_main(self, out, argv, flagship):
        with open(os.path.join(out, "spots.json"), "w", encoding="utf-8") as f:
            json.dump({"flagship": [self.OLD]}, f)
        with mock.patch.object(check_spots, "OUT", out), \
                mock.patch.object(check_spots, "zones", return_value=[self.ZONE]), \
                mock.patch.object(check_spots.seeds, "spots", return_value=[{"name": "A", "f": {"top": 1}}]), \
                mock.patch.object(check_spots, "fetch_waves", return_value={}), \
                mock.patch.object(check_spots, "check_cells", return_value=self.CELLS), \
                mock.patch.object(check_spots, "check_flagship", side_effect=flagship) as called, \
                mock.patch.object(sys, "argv", ["check_spots.py"] + argv), \
                contextlib.redirect_stdout(io.StringIO()):
            try:
                check_spots.main()
            except KeyboardInterrupt:
                pass
        return called

    def read(self, out):
        with open(os.path.join(out, "spots.json"), encoding="utf-8") as f:
            data = json.load(f)
        with open(os.path.join(out, "spots.md"), encoding="utf-8") as f:
            return data, f.read()

    def test_cut_off_keeps_the_rest(self):
        with tempfile.TemporaryDirectory() as out:
            self.run_main(out, [], KeyboardInterrupt)
            data, md = self.read(out)
        self.assertEqual(data["cells"], self.CELLS)
        self.assertEqual(data["flagship"], [self.OLD])
        self.assertTrue(data["flagship_old"])
        self.assertIn("Celdas de olas para mirar (1)", md)
        self.assertIn("de la corrida anterior", md)

    def test_whole_run_replaces_them(self):
        with tempfile.TemporaryDirectory() as out:
            self.run_main(out, [], [{"status": "ok", "km": 0.2}])
            data, md = self.read(out)
        self.assertEqual(data["flagship"][0]["km"], 0.2)
        self.assertNotIn("flagship_old", data)
        self.assertNotIn("de la corrida anterior", md)

    def test_no_wikidata_says_so(self):
        with tempfile.TemporaryDirectory() as out:
            called = self.run_main(out, ["--no-wikidata"], [])
            data, md = self.read(out)
        called.assert_not_called()
        self.assertEqual(data["flagship"], [self.OLD])
        self.assertIn("de la corrida anterior", md)


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


class Armada(unittest.TestCase):
    """tools/armada.py: las series de la página (horas de Uruguay a UTC, sin los vacíos) y el CSV que
    suma solo lo nuevo."""

    PAGE = ('g = new Dygraph(document.getElementById("graphM"), [[new Date("2026/11/10 08:40:02"), 0.951],'
            ' [new Date("2026/11/10 08:45:02"), null], [new Date("2026/11/10 08:50:02"), 0.934]], {labels: []});'
            ' h = new Dygraph(document.getElementById("graphT"), [[new Date("2026/11/10 08:40:02"), 18.4]], {});')

    def test_parse(self):
        s = armada.parse(self.PAGE)
        self.assertEqual(sorted(s), ["graphM", "graphT"])
        self.assertEqual(len(s["graphM"]), 2)                       # sin el null
        t = min(s["graphM"])
        self.assertEqual(t, 1794310802)                             # 08:40:02 en Uruguay = 11:40:02 UTC
        self.assertEqual(s["graphT"][t], 18.4)

    def test_merge(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "x.csv")
            s = armada.parse(self.PAGE)
            self.assertEqual(armada.merge(p, s), 2)
            self.assertEqual(armada.merge(p, s), 0)                 # las 48 h se solapan: nada repetido
            rows = open(p).read().splitlines()
            self.assertEqual(rows[0], "utc,nivel_m,agua_c")
            self.assertEqual(rows[1], "2026-11-10T11:40:02Z,0.951,18.4")
            self.assertEqual(rows[2], "2026-11-10T11:50:02Z,0.934,")


class Era5Normals(unittest.TestCase):
    """The requests of tools/era5_normals.py are the ones `swift run normals` asks (surf-dawn: Normals)."""
    TODAY = __import__("datetime").date(2026, 11, 13)

    def zone(self):
        with open(os.path.join(os.path.dirname(HERE), "spots", "r", "UY-MAL.json"), encoding="utf-8") as f:
            return json.load(f)

    def test_the_reference_spot_is_the_one_whose_wave_point_most_share(self):
        z = {"s": [["A", 1, 2, 90, 1], ["B", 1, 3, 90, 1, 5, 6], ["C", 1, 4, 90, 1, 5, 6], ["D", 1, 2, 90, 1]]}
        self.assertEqual(era5.reference(z), 0)      # A and D share (1, 2), B and C (5, 6): a tie, the first
        z["s"].append(["E", 1, 5, 90, 1, 5, 6])
        self.assertEqual(era5.reference(z), 1)      # now (5, 6) has three
        self.assertEqual(era5.reference({"s": [["A", 1, 2, 90, 1]]}), 0)

    def test_maldonado_asks_at_the_bravas_point(self):
        pl = era5.plan(self.zone(), self.TODAY)
        self.assertEqual(pl["spot"], "LA VIRGEN")   # the first of the Brava's eight, not PUNTA DEL CHILENO in the bay
        wind, marine = dict(pl["wind"][1]), dict(pl["marine"][1])
        self.assertEqual((wind["latitude"], wind["longitude"]), ("-34.9653", "-54.9422"))
        self.assertEqual((marine["latitude"], marine["longitude"]), ("-35.0000", "-54.7500"))
        self.assertEqual(wind["models"], "era5")
        self.assertEqual(marine["models"], "era5_ocean")
        self.assertEqual(marine["hourly"], "wave_height,wave_peak_period,wave_direction")
        self.assertEqual((marine["start_date"], marine["end_date"]), ("2016-01-01", "2024-11-17"))
        self.assertEqual(dict(pl["factor_era5"][1])["start_date"], "2026-08-13")
        self.assertEqual(dict(pl["factor_model"][1])["models"], "ncep_gfswave025")

    def test_a_region_weighs_some_570_calls(self):
        # the waves and the wind with the air's max and min (no more calls: 6 variables), the factor, the water's 3 years
        # (78) and the air's offset (13)
        self.assertAlmostEqual(era5.cost(self.zone(), self.TODAY), 568.0, delta=2)

    def test_the_waves_come_in_the_winds_time_zone(self):
        asked = []

        def get(url, params):
            asked.append(dict(params))
            return {"timezone": "America/Montevideo", "hourly": {"wave_peak_period": [8.0, None]}}

        with mock.patch.object(era5, "get", get):
            b = era5.fetch(self.zone(), self.TODAY)
        self.assertEqual(asked[1]["timezone"], "America/Montevideo")
        self.assertEqual([a["timezone"] for a in asked[4:]], ["America/Montevideo"] * 3)   # the water and the air too
        self.assertEqual([a["timezone"] for a in asked[2:4]], ["GMT", "GMT"])              # the factor's, as they were
        self.assertEqual(asked[0]["daily"], "sunrise,sunset,temperature_2m_max,temperature_2m_min")
        self.assertEqual((asked[4]["latitude"], asked[4]["longitude"]), ("-34.9653", "-54.9422"))   # the water at the spot
        self.assertEqual(asked[5]["models"], "gfs_seamless")                                        # the zone's wind model
        self.assertEqual(sorted(b["asked"]), ["air_era5", "air_model", "factor_era5", "factor_model", "marine", "water", "wind"])
        self.assertEqual(era5.entry(b)["hours"], 1)
        self.assertTrue(era5.current(era5.entry(b), era5.plan(self.zone(), self.TODAY)))
        old = dict(era5.entry(b), v=1)              # asked before the water and the air: again
        self.assertFalse(era5.current(old, era5.plan(self.zone(), self.TODAY)))
        moved = self.zone()
        moved["s"] = moved["s"][9:]                 # LA BOCA first, its own wave point
        self.assertFalse(era5.current(era5.entry(b), era5.plan(moved, self.TODAY)))


class WindTest(unittest.TestCase):
    """tools/wind.py: the tiles of the weather map, as the phone finds them."""

    LEVELS = [{"deg": 10, "rows": 18, "cols": 36, "offset": 0}, {"deg": 40, "rows": 5, "cols": 9, "offset": 648 * 137842}]

    def test_offsets(self):
        size = len(wind.HOURS) * 2 * wind.N * wind.N
        self.assertEqual(wind.tile_offset(self.LEVELS, -90, -180), (0, size))
        # La Boca: row 5 (-40 to -30), column 12 (-60 to -50)
        self.assertEqual(wind.tile_offset(self.LEVELS, -34.92, -54.87)[0], (5 * 36 + 12) * size)
        self.assertEqual(wind.tile_offset(self.LEVELS, 90, 180)[0], (17 * 36 + 35) * size)
        self.assertEqual(wind.tile_offset(self.LEVELS, -34.92, -54.87, 1)[0], 648 * 137842 + (1 * 9 + 3) * size)

    def test_tiles(self):
        hours = len(wind.HOURS)
        lat = np.arange(721, dtype=np.int32)[None, :, None]
        lon = np.arange(1441, dtype=np.int32)[None, None, :]
        # u holds the latitude's index mod 127, v the longitude's: each point says where it came from
        u = np.broadcast_to((lat % 127).astype(np.int8), (hours, 721, 1441))
        v = np.broadcast_to((lon % 127).astype(np.int8), (hours, 721, 1441))
        parts = wind.tiles(u, v)
        self.assertEqual(len(parts), 18 * 36 + 5 * 9)
        t = np.frombuffer(parts[5 * 36 + 12], np.int8).reshape(hours, 2, wind.N, wind.N)
        self.assertEqual(t[0, 0, 0, 0], (5 * 40) % 127)          # south-west corner: lat -40 is index 200
        self.assertEqual(t[0, 1, 0, 0], (12 * 40) % 127)         # lon -60 is index 480
        self.assertEqual(t[3, 0, 40, 0], (6 * 40) % 127)         # the north edge is the next tile's south
        c = np.frombuffer(parts[648 + 4 * 9 + 8], np.int8).reshape(hours, 2, wind.N, wind.N)
        self.assertEqual(c[0, 0, 40, 0], 720 % 127)              # over the pole, the pole
        self.assertEqual(c[0, 1, 0, 40], 1440 % 127)             # the east edge is 180


if __name__ == "__main__":
    unittest.main()
