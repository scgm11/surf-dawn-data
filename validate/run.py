#!/usr/bin/env python3
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe  # noqa: E402
for name, fn in probe.P:
    probe.probe(name, fn)
