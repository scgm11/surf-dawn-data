"""Offline tests of the parsers, the matching and the scores: python3 -m unittest discover validate"""
import math
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import buoys  # noqa: E402
import evaluate  # noqa: E402
import models  # noqa: E402
import regions  # noqa: E402
import report  # noqa: E402
import score  # noqa: E402
from tools.lib import geo, openmeteo  # noqa: E402

T0 = 1790000000 - 1790000000 % 3600        # an hour boundary

NDBC_TXT = """#YY  MM DD hh mm WDIR WSPD GST  WVHT   DPD   APD MWD   PRES  ATMP  WTMP  DEWP  VIS PTDY  TIDE
#yr  mo dy hr mn degT m/s  m/s     m   sec   sec degT   hPa  degC  degC  degC  nmi  hPa    ft
2026 10 13 00 56  MM   MM   MM   1.4    20   8.0 205     MM    MM  23.1    MM   MM   MM    MM
2026 10 13 00 26  MM   MM   MM   1.5    15   8.1 209     MM    MM  23.1    MM   MM   MM    MM
2026 10 12 23 56  MM   MM   MM    MM    MM    MM  MM     MM    MM  23.1    MM   MM   MM    MM
2026 10 12 22 56  MM   MM   MM  99.0    20   8.4 216     MM    MM  23.1    MM   MM   MM    MM
"""

NDBC_XML = """<?xml version="1.0" encoding="utf-8"?><stations created="x" count="2">
  <station id="46225" lat="32.93" lon="-117.391" name="Torrey Pines Outer, CA (100)" owner="CDIP" pgm="IOOS Partners" type="buoy" met="n"/>
  <station id="ygnn6" lat="43.262" lon="-79.064" name="Niagara" owner="x" pgm="x" type="fixed" met="n"/>
</stations>"""

NDBC_HTML = """<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="46225.txt">46225.txt</a></td><td align="right">2026-10-13 01:10  </td><td align="right"> 95K</td></tr>
<tr><td valign="top"><img src="/icons/text.gif" alt="[TXT]"></td><td><a href="46225.spec">46225.spec</a></td><td align="right">2026-10-13 01:10  </td><td align="right"> 95K</td></tr>"""

CDIP_CSV = """station_id,time,latitude,longitude,waveHs,waveTp,waveTa,waveDp
,UTC,degrees_north,degrees_east,m,s,s,degreeT
100,2026-10-12T00:00:00Z,32.93,-117.392,1.2,14.3,8.1,265.0
100,2026-10-12T00:30:00Z,32.93,-117.392,1.3,14.3,8.0,NaN
067,2026-10-12T00:00:00Z,33.22,-119.88,2.0,12.5,7.0,290.0
"""

MI_CSV = """station_id,time,latitude,longitude,SignificantWaveHeight,PeakPeriod,PeakDirection,EnergyPeriod
,UTC,degrees_north,degrees_east,cm,s,degrees_true,s
AMETS Berth B Wave Buoy,2026-10-12T00:00:00Z,54.2753,-10.1497,250.0,11.1,90.0,8.2
"""

MI_INFO = """Row Type,Variable Name,Attribute Name,Data Type,Value
attribute,NC_GLOBAL,title,String,Irish Wave Buoys 30 Min
variable,PeakPeriod,,float,
attribute,PeakPeriod,standard_name,String,sea_surface_wave_period_at_variance_spectral_density_maximum
attribute,PeakPeriod,units,String,s
variable,PeakDirection,,float,
attribute,PeakDirection,standard_name,String,sea_surface_wave_to_direction
attribute,PeakDirection,units,String,degrees_true
variable,EnergyPeriod,,double,
attribute,EnergyPeriod,standard_name,String,sea_surface_wave_mean_period_from_variance_spectral_density_inverse_frequency_moment
variable,SignificantWaveHeight,,float,
attribute,SignificantWaveHeight,standard_name,String,sea_surface_wave_significant_height
attribute,SignificantWaveHeight,units,String,cm
variable,SignificantWaveHeight_qc,,double,
"""

IWB_INFO = """Row Type,Variable Name,Attribute Name,Data Type,Value
variable,WaveHeight,,double,
attribute,WaveHeight,units,String,m
variable,WavePeriod,,double,
attribute,WavePeriod,units,String,s
variable,MeanWaveDirection,,double,
attribute,MeanWaveDirection,units,String,degrees_true
variable,Tp,,double,
"""


def obs(hs, tp=10.0, dp=270.0, tm=8.0, start=T0, step=3600):
    return {(start + i * step) // 3600: (h, tp, dp, tm) for i, h in enumerate(hs)}


def cols(hs, per=8.0, peak=None, dp=270.0):
    n = len(hs)
    return {"wave_height": list(hs), "wave_period": [per] * n,
            "wave_peak_period": [peak] * n, "wave_direction": [dp] * n}


class Parsers(unittest.TestCase):
    def test_ndbc_txt(self):
        r = buoys.parse_ndbc_txt(NDBC_TXT)
        self.assertEqual(len(r), 4)
        self.assertEqual(r[0][1:], (1.4, 20.0, 205.0, 8.0))
        self.assertEqual(r[0][0] % 3600, 56 * 60)
        self.assertIsNone(r[2][1])                       # MM
        self.assertIsNone(buoys.clean(*r[3][1:])[0])     # 99.0 sentinel: out of range

    def test_ndbc_stations_listing(self):
        st = buoys.parse_ndbc_stations(NDBC_XML)
        self.assertEqual(st["46225"][1:3], (32.93, -117.391))
        self.assertIn("YGNN6", st)
        ls = buoys.parse_ndbc_listing(NDBC_HTML)
        self.assertEqual(ls["46225.txt"], "2026-10-13 01:10")
        self.assertIn("46225.spec", ls)

    def test_erddap_cdip(self):
        rows = buoys.parse_erddap_csv(CDIP_CSV)
        st = {s.sid: s for s in buoys.stations_from_rows("cdip", rows, "station_id", buoys.cdip_conv)}
        self.assertEqual(set(st), {"100", "067"})
        s = buoys.finish(st["100"], 0)
        self.assertEqual(len(s.hourly), 2)
        self.assertIsNone(s.records[1][3])             # NaN direction
        self.assertAlmostEqual(s.lon, -117.392)

    def test_mi_units_and_direction(self):
        cols = buoys.wave_columns(buoys.erddap_vars(MI_INFO))
        self.assertEqual(cols["hs"], ("SignificantWaveHeight", 0.01))
        self.assertEqual(cols["dir"], ("PeakDirection", 180.0))
        self.assertEqual(cols["tm"], "EnergyPeriod")
        rows = buoys.parse_erddap_csv(MI_CSV)
        s = buoys.stations_from_rows("mi", rows, "station_id", buoys.column_conv(cols), slug=True)[0]
        self.assertEqual(s.id, "mi:amets-berth-b-wave-buoy")
        t, hs, tp, dp, tm = s.records[0]
        self.assertAlmostEqual(hs, 2.5)                # cm -> m
        self.assertAlmostEqual(dp, 270.0)              # "to" 90 -> "from" 270
        self.assertAlmostEqual(tp, 11.1)

    def test_weather_buoys_by_name(self):
        cols = buoys.wave_columns(buoys.erddap_vars(IWB_INFO))
        self.assertEqual(cols, {"hs": ("WaveHeight", 1.0), "tp": "Tp", "tm": "WavePeriod", "dir": ("MeanWaveDirection", 0.0)})
        conv = buoys.column_conv(cols)
        self.assertEqual(conv({"WaveHeight": "2.5", "Tp": "11", "MeanWaveDirection": "250", "WavePeriod": "7"}), (2.5, 11.0, 250.0, 7.0))
        self.assertIsNone(buoys.wave_columns({"AirTemperature": {}}))

    def test_aodn_columns(self):
        c = {"TIME": [T0, T0 + 1800, T0 + 3600], "LATITUDE": [-33.8, -33.8, -33.8], "LONGITUDE": [151.4] * 3,
             "WSSH": [1.5, float("nan"), 1.7], "WPPE": [10.0, 10.0, 11.0], "WPDI": [170.0, 171.0, 172.0],
             "WPFM": [7.0, 7.0, 7.1], "site_name": ["Sydney"] * 3}
        s = buoys.aodn_stations(c)[0]
        buoys.finish(s, 0)
        self.assertEqual(s.id, "aodn:sydney")
        self.assertEqual(len(s.hourly), 2)
        c["site_name"] = ["APOLLO-BAY", "Apollo%20Bay", "Apollo%20Bay"]
        st = buoys.aodn_stations(c)
        self.assertEqual([x.id for x in st], ["aodn:apollo-bay"])   # two spellings, one buoy
        self.assertEqual(len(st[0].records), 3)

    def test_hourly_nearest(self):
        recs = [(T0 - 600, 1.0, None, None, None), (T0 + 300, 2.0, None, None, None), (T0 + 1800, 3.0, None, None, None)]
        h = buoys.hourly(recs)
        self.assertEqual(h[T0 // 3600][0], 2.0)
        self.assertEqual(h[T0 // 3600 + 1][0], 3.0)    # :30 belongs to the next hour (rounding up)

    def test_clean(self):
        self.assertEqual(buoys.clean(0.01, 0.5, 400, 40), (None, None, None, None))
        self.assertEqual(buoys.clean(1.0, 10.0, 360.0, 8.0), (1.0, 10.0, 0.0, 8.0))

    def test_dedupe(self):
        a = buoys.Station("cdip", "100", "", 32.93, -117.392, [])
        b = buoys.Station("ndbc", "46225", "", 32.933, -117.391, [])
        c = buoys.Station("ndbc", "46232", "", 32.5, -117.4, [])
        kept, dropped = buoys.dedupe([b, a, c], geo.km)
        self.assertEqual({s.id for s in kept}, {"cdip:100", "ndbc:46232"})
        self.assertEqual(dropped[0][0].id, "ndbc:46225")

    def test_erddap_url_encoding(self):
        u = buoys.erddap_url("https://x/t.csv", ["a", "b"], ["time>=now-31days", "flag=1"])
        self.assertIn("time%3E=now-31days", u)
        self.assertIn("&flag=1", u)


class OpenMeteo(unittest.TestCase):
    def test_split_models(self):
        block = {"hourly": {"time": [1, 2], "wave_height_a": [1.0, 1.1], "wave_period_a": [8, 8],
                            "wave_height_b": [None, None], "wave_peak_period_a": [None, None]}}
        t, m = openmeteo.split_models(block, ["a", "b"], ["wave_height", "wave_period", "wave_peak_period"])
        self.assertEqual(t, [1, 2])
        self.assertEqual(set(m), {"a"})                # b is all null: outside its domain
        t, m = openmeteo.split_models({"hourly": {"time": [1], "wave_height": [0.5]}}, ["a"], ["wave_height"])
        self.assertEqual(m["a"]["wave_height"], [0.5])

    def test_weight(self):
        self.assertEqual(openmeteo.call_weight(10, 4, 14), 10)
        self.assertAlmostEqual(openmeteo.call_weight(10, 20, 31), 10 * 2 * 31 / 14)

    def test_models_for(self):
        self.assertIn("ncep_gfswave016", models.models_for(33.0, -117.0))
        self.assertNotIn("ncep_gfswave016", models.models_for(-34.9, -54.9))
        self.assertIn("dwd_ewam", models.models_for(43.5, -1.6))
        self.assertNotIn("dwd_ewam", models.models_for(53.0, -11.0))   # west of 10.5°W

    def test_pacer(self):
        clock = [0.0]
        slept = []
        p = models.Pacer(100, clock=lambda: clock[0], sleep=lambda s: (slept.append(s), clock.__setitem__(0, clock[0] + s)))
        p.wait(60)
        p.wait(30)
        self.assertEqual(slept, [])
        p.wait(30)
        self.assertEqual(len(slept), 1)


class Scores(unittest.TestCase):
    def test_metrics(self):
        o = obs([1.0, 2.0, 1.0, 2.0], tp=12.0, dp=350.0)
        c = cols([1.1, 2.2, 1.1, 2.2], per=9.0, peak=11.0, dp=10.0)
        ps = score.pairs(o, [T0 + 3600 * i for i in range(4)], c)
        m = score.metrics(ps)
        self.assertEqual(m["n"], 4)
        self.assertAlmostEqual(m["hs_bias"], 0.1)
        self.assertAlmostEqual(m["hs_rmse"], math.sqrt((0.01 + 0.04) / 2), places=3)
        self.assertAlmostEqual(m["tp_bias"], -1.0)
        self.assertAlmostEqual(m["tm_bias"], 1.0)
        self.assertAlmostEqual(m["dir_mae"], 20.0)     # 350 -> 10 across north
        self.assertAlmostEqual(m["dir_bias"], 20.0)
        self.assertAlmostEqual(m["hs_si"], 0.05 / 1.5, places=3)

    def test_mean_period_fallback(self):
        hs, tp, kind, per, dp = score.model_columns(cols([1.0], per=8.5, peak=None))
        self.assertEqual(kind, "mean")
        self.assertEqual(tp, [8.5])
        self.assertEqual(score.model_columns(cols([1.0], peak=12.0))[2], "peak")
        self.assertEqual(score.model_columns(cols([1.0]), "ncep_gfswave025")[2], "primary")

    def test_pairs_drop_missing_and_limit_hours(self):
        o = obs([1.0, None, 1.0])
        o[(T0 // 3600) + 1] = (None, None, None, None)
        c = cols([1.0, 1.0, None])
        self.assertEqual(len(score.pairs(o, [T0, T0 + 3600, T0 + 7200], c)), 1)
        self.assertEqual(len(score.pairs(obs([1, 1, 1]), [T0, T0 + 3600, T0 + 7200], cols([1, 1, 1]), {T0 // 3600})), 1)

    def test_dir_ignores_small_waves(self):
        ps = score.pairs(obs([0.2, 1.0], dp=0.0), [T0, T0 + 3600], cols([0.2, 1.0], dp=90.0))
        self.assertEqual(score.metrics(ps)["dir_mae"], 90.0)
        ps = score.pairs(obs([0.2], dp=0.0), [T0], cols([0.2], dp=90.0))
        self.assertIsNone(score.metrics(ps)["dir_mae"])

    def S(self, rmse, bias, d=10.0):
        return {"hs_rmse": rmse, "hs_bias": bias, "dir_mae": d}

    def test_best_rule(self):
        s = {"a": self.S(0.20, 0.30), "b": self.S(0.25, 0.05), "c": self.S(0.30, -0.10)}
        self.assertEqual(score.best(s), "b")           # a is lower but biased > 15 %
        s = {"a": self.S(0.200, 0.0, 20), "b": self.S(0.205, 0.0, 12)}
        self.assertEqual(score.best(s), "b")           # tie within 1 cm: direction decides
        self.assertIsNone(score.best({"a": self.S(0.2, 0.5)}))

    def test_confidence(self):
        s = {"a": self.S(0.20, 0.0), "b": self.S(0.25, 0.0)}
        self.assertEqual(score.confidence(s, "a", "b", 600, 2, 2, 20)[0], "alta")
        self.assertEqual(score.confidence(s, "a", "b", 600, 2, 2, 140)[0], "media")    # far buoy
        self.assertEqual(score.confidence(s, "a", "b", 300, 1, 1, 20)[0], "media")
        self.assertEqual(score.confidence(s, "a", "b", 600, 1, 2, 20)[0], "baja")      # buoys split
        s = {"a": self.S(0.20, 0.0), "b": self.S(0.205, 0.0)}
        self.assertEqual(score.confidence(s, "a", "b", 600, 2, 2, 20)[0], "baja")      # no margin

    def test_spread(self):
        sp, n, means = score.spread([1, 2], {"a": {"wave_height": [1.0, 2.0]}, "b": {"wave_height": [1.0, 2.0]}})
        self.assertEqual(sp, 0.0)
        sp, n, means = score.spread([1], {"a": {"wave_height": [1.0]}, "b": {"wave_height": [3.0]}})
        self.assertAlmostEqual(sp, 0.5)
        self.assertEqual(score.spread_confidence(0.31), "baja")
        self.assertEqual(score.spread_confidence(0.2), "media")


class Regions(unittest.TestCase):
    def test_fixed(self):
        self.assertTrue(regions.is_fixed("UY-MAL", "UY"))
        self.assertTrue(regions.is_fixed("AR-MDP", "AR"))
        self.assertTrue(regions.is_fixed("BR-SC-NOR", "BR"))
        self.assertTrue(regions.is_fixed("BR-RS-SUL", "BR"))
        self.assertFalse(regions.is_fixed("BR-SP", "BR"))
        self.assertEqual(regions.default_models("BR-SP", "BR", -23.9)[0], "ncep_gfswave025")
        self.assertEqual(regions.default_models("US-CA-SD", "US", 32.8)[0], "ncep_gfswave016")
        self.assertEqual(regions.default_models("UY-MAL", "UY", -10)[0], "ncep_gfswave025")

    def test_match_antimeridian(self):
        r = regions.Region("FJ-X", "FJ", "x", [(-18.0, 179.9), (-18.1, 179.8)])
        near = buoys.Station("ndbc", "1", "", -18.0, -179.5, [])
        far = buoys.Station("ndbc", "2", "", -18.0, -170.0, [])
        m, _ = regions.match(r, [far, near])
        self.assertEqual([s.id for s, _, _ in m], ["ndbc:1"])
        self.assertLess(m[0][1], 70)                   # 0.6° of longitude across ±180

    def test_match_order_and_cap(self):
        r = regions.Region("US-X", "US", "x", [(33.0, -117.3)])
        st = [buoys.Station("cdip", str(i), "", 33.0 + 0.2 * i, -117.3, []) for i in range(6)]
        m, _ = regions.match(r, st, top=3)
        self.assertEqual([s.sid for s, _, _ in m], ["0", "1", "2"])
        self.assertEqual(len(regions.match(r, st)[0]), regions.CANDIDATES)

    def test_same_sea(self):
        # land: everything east of lon 10.0 (a straight north-south coast facing west), plus a
        # closed bay: a lagoon west of the coast walled off to the open sea
        def is_land(lats, lons):
            out = []
            for a, b in zip(lats, lons):
                lagoon_wall = 9.9 <= b <= 9.92 and -0.2 <= a <= 0.2 or -0.2 <= a <= -0.18 and 9.9 <= b <= 10.0 \
                    or 0.18 <= a <= 0.2 and 9.9 <= b <= 10.0
                out.append(b >= 10.0 or lagoon_wall)
            return out
        ex = regions.Exposure(is_land)
        r = regions.Region("X", "X", "x", [(1.0, 9.995), (1.2, 9.995)])     # spots on the open coast
        sea = buoys.Station("x", "sea", "", 1.1, 9.8, [])
        bay = buoys.Station("x", "bay", "", 0.0, 9.96, [])                  # inside the lagoon
        other = buoys.Station("x", "east", "", 1.1, 10.6, [])               # inland "buoy": another sea
        self.assertGreater(ex.shared(r, 1.1, 9.8), 0.9)
        m, blocked = regions.match(r, [bay, sea, other], exposure=ex)
        self.assertEqual([s.sid for s, _, _ in m], ["sea"])
        self.assertEqual({s.sid for s, _, _ in blocked}, {"bay", "east"})
        rays = regions.open_rays(1.0, 9.995, is_land, 2.0)
        self.assertEqual(len(rays), regions.RAYS)
        self.assertFalse(rays[8])                      # east (bearing 90°) is land
        self.assertTrue(rays[24])                      # west is open sea

    def test_seeds_load(self):
        rs = {r.code: r for r in regions.load()}
        self.assertGreater(len(rs), 200)
        self.assertTrue(rs["UY-MAL"].fixed)
        self.assertEqual(rs["UY-MAL"].current[0], "ncep_gfswave025")


class Evaluate(unittest.TestCase):
    def setUp(self):
        self.r = regions.Region("US-X", "US", "x", [(33.0, -117.3), (33.1, -117.35)])
        n = 300
        truth = [1.0 + 0.5 * math.sin(i / 12.0) for i in range(n)]
        self.times = [T0 + 3600 * i for i in range(n)]
        st = buoys.Station("cdip", "100", "", 32.95, -117.4, [])
        st.hourly = obs(truth)
        self.st = st
        good = [h * 1.02 for h in truth]
        bad = [h * 1.3 for h in truth]
        self.series = {(32.95, -117.4): (self.times, {"ncep_gfswave016": cols(bad), "ncep_gfswave025": cols(bad),
                                                      "meteofrance_wave": cols(good), "ecmwf_wam": cols(good, peak=10.0)})}

    def test_region_result(self):
        body, info = evaluate.region_result(self.r, [(self.st, 6.0, None)], self.series, ("2026-09-12", "2026-10-12"),
                                            (self.times, {"a": {"wave_height": [1.0] * 300}, "b": {"wave_height": [1.2] * 300}}))
        self.assertEqual(body["buoys"], ["cdip:100"])
        self.assertIn(body["best"]["wave"], ("meteofrance_wave", "ecmwf_wam"))
        self.assertEqual(body["wave"]["meteofrance_wave"]["tp_type"], "mean")
        self.assertEqual(body["wave"]["ecmwf_wam"]["tp_type"], "peak")
        self.assertEqual(body["confidence"], "media")  # 300 h: not enough for alta
        self.assertEqual(body["vs"], "ncep_gfswave016")
        self.assertEqual(body["current"], "ncep_gfswave016")
        self.assertIsNotNone(body["spread"]["hs"])
        rows = report.suggestions([(body, info)])
        self.assertEqual(rows[0][0], "US-X")
        self.assertEqual(rows[0][2], "gfs_seamless")

    def test_sheltered_buoy_skipped(self):
        bay = buoys.Station("cdip", "bay", "", 32.96, -117.41, [])
        bay.hourly = {h: (v[0] * 0.3,) + v[1:] for h, v in self.st.hourly.items()}
        self.series[(32.96, -117.41)] = self.series[(32.95, -117.4)]
        body, info = evaluate.region_result(self.r, [(bay, 2.0, None), (self.st, 6.0, None)], self.series, ("a", "b"))
        self.assertEqual(body["buoys"], ["cdip:100"])
        self.assertEqual(body["excluded"][0]["id"], "cdip:bay")

    def test_fixed_never_suggested(self):
        r = regions.Region("UY-X", "UY", "x", [(33.0, -117.3)])
        body, info = evaluate.region_result(r, [(self.st, 6.0, None)], self.series, ("a", "b"))
        self.assertTrue(body["fixed"])
        self.assertIn("best", body)
        self.assertEqual(report.suggestions([(body, info)]), [])

    def test_buoy_without_current_model(self):
        st = buoys.Station("cdip", "106", "", 33.01, -117.31, [])
        st.hourly = self.st.hourly
        t, c = self.series[(32.95, -117.4)]
        self.series[(33.01, -117.31)] = (t, {m: v for m, v in c.items() if m != "ncep_gfswave016"})
        body, info = evaluate.region_result(self.r, [(st, 1.0, None), (self.st, 6.0, None)], self.series, ("a", "b"))
        self.assertEqual(body["buoys"], ["cdip:100"])
        self.assertIn("ncep_gfswave016", body["excluded"][0]["why"])

    def test_model_with_few_hours_left_out(self):
        t, c = self.series[(32.95, -117.4)]
        c = dict(c)
        half = dict(c["meteofrance_wave"])
        half["wave_height"] = [h if i % 2 else None for i, h in enumerate(half["wave_height"])]
        c["meteofrance_wave"] = half
        self.series[(32.95, -117.4)] = (t, c)
        body, info = evaluate.region_result(self.r, [(self.st, 6.0, None)], self.series, ("a", "b"))
        self.assertEqual(body["buoys"], ["cdip:100"])
        self.assertNotIn("meteofrance_wave", body["wave"])
        self.assertEqual(body["wave"]["ecmwf_wam"]["n"], 300)          # the others keep every hour
        cur = dict(c["ncep_gfswave016"])
        cur["wave_height"] = [h if i < 30 else None for i, h in enumerate(cur["wave_height"])]
        c["ncep_gfswave016"] = cur
        body, info = evaluate.region_result(self.r, [(self.st, 6.0, None)], self.series, ("a", "b"))
        self.assertEqual(body["buoys"], [])                             # today's model barely there
        self.assertIn("pocas horas", body["excluded"][0]["why"])

    def test_no_buoys(self):
        body, info = evaluate.region_result(self.r, [], {}, ("a", "b"),
                                            ([1, 2], {"a": {"wave_height": [1.0, 1.0]}, "b": {"wave_height": [3.0, 3.0]}}))
        self.assertEqual(body["buoys"], [])
        self.assertNotIn("best", body)
        self.assertEqual(body["confidence"], "baja")
        self.assertAlmostEqual(body["spread"]["hs"], 0.5)

    def test_markdown_renders(self):
        body, info = evaluate.region_result(self.r, [(self.st, 6.0, None)], self.series, ("a", "b"))
        nob, ninfo = evaluate.region_result(regions.Region("US-Y", "US", "y", [(10.0, 10.0)]), [], {}, ("a", "b"))
        md = report.markdown([(body, info), (nob, ninfo)], ("a", "b"), {"cdip": "ok"}, {}, models.USED, [])
        self.assertIn("US-X", md)
        self.assertIn("Regiones sin boyas (1)", md)


if __name__ == "__main__":
    unittest.main()
