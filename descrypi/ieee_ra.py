"""Query the IEEE Registration Authority for MAC prefixes.

Each physical device has a MAC address made of six parts, the first three
indicate who made the device. We use this prefix to identify the model/maker.

These prefixes are handed out by the IEEE Registration Authority and are
queryable at https://regauth.standards.ieee.org/standards-ra-web/pub/view.html

The Raspberry Pi folks have two MAC prefixes. It's possible in the future
they'll add another. This file demonstrates how to query the IEEE RA database
for those MAC prefixes.

For some reason the Rock Pi doesn't appear in the IEEE RA.
"""

import csv
import textwrap
import urllib.parse
import urllib.request

# Known MAC prefixes by model, sorted
MAC_PREFIX_MAP = {
    "Raspberry Pi": ("B8:27:EB", "DC:A6:32"),
    "Rock Pi": ("EA:62:9D",),
}
MAC_PREFIXES = [mac for macs in MAC_PREFIX_MAP.values() for mac in macs] # ['B8:27:EB', ...]
MAC_PREFIX_MODEL_MAP = dict(
    # {"B8:27:EB": "Raspberry Pi", ...}
    ((mac, model) for model, macs in MAC_PREFIX_MAP.items() for mac in macs)
)

# URL to query the IEEE Registration Authority for updated MAC prefixes
# Browser URL is https://regauth.standards.ieee.org/standards-ra-web/pub/view.html
IEEE_RA_URL = "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/"

def model_by_mac_prefix(mac_prefix):
  """Take a three octet MAC prefix and return the device model."""
  return MAC_PREFIX_MODEL_MAP.get(mac_prefix.upper(), "Unknown")

def ieee_ra_url(query):
  """Return a URL to query IEEE Registration Authority's MAC database."""
  # curl "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/"\
  #      "?registry=MAC&text=%22raspberry%20pi%22"
  params = urllib.parse.urlencode({'registry': 'MAC', 'text': query})
  return IEEE_RA_URL + "?" + params

def macs_from_ieee_ra(query):
  """Query IEEE Reg Authority for `query`.

  Data looks like,
  Registry,Assignment,Organization Name,Organization Address
  MA-L,DCA632,Raspberry Pi Trading Ltd,"Maurice Wilkes Building, Cowley Road Cambridge  GB CB4 0DS "
  MA-L,B827EB,Raspberry Pi Foundation,Mitchell Wood House Caldecote Cambridgeshire US CB23 7NU
  """
  try:
    with urllib.request.urlopen(ieee_ra_url(query)) as f:
      reader = csv.reader((line.decode() for line in f), delimiter=',', quotechar='"')
      next(reader) # skip header
      # Split "01AB23" into "01:AB:23"
      return tuple(sorted((":".join(textwrap.wrap(row[1], 2)) for row in reader)))
  except urllib.error.HTTPError as err:
    print("IEEE RA query failed:", err, "(may be transient; try again?)")
    return ()

def check_ieee_macs(query='"raspberry pi"', model="Raspberry Pi"):
  """Check and return new MAC prefixes, else return False."""
  macs = MAC_PREFIX_MAP[model]
  new_macs = macs_from_ieee_ra(query)
  return new_macs if macs != new_macs else False
