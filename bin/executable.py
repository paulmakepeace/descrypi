"""Silly path mangling so bin/* can work."""

import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
