"""Query the IEEE Registration Authority for MAC prefixes.

The Raspberry Pi folks have two MAC prefixes. It's possible in the future
they'll add another. This file demonstrates how to query the IEEE RA database
for those MAC prefixes.
"""

import csv
import textwrap
import urllib.parse
import urllib.request

# Known RPi MAC prefixes, sorted
RASPBERRY_PI_MACS = ('B8:27:EB', 'DC:A6:32')

# URL to query the IEEE Registration Authority for updated MAC prefixes
IEEE_RA_URL = "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/"
IEEE_RA_QUERY = '"raspberry pi"'

def ieee_ra_url(query):
  """Return a URL to query IEEE Registration Authority's MAC database."""
  # curl "https://services13.ieee.org/RST/standards-ra-web/rest/assignments/download/"\
  #      "?registry=MAC&text=%22raspberry%20pi%22"
  params = urllib.parse.urlencode({'registry': 'MAC', 'text': query})
  return IEEE_RA_URL + "?" + params

def macs_from_ieee_ra(query=IEEE_RA_QUERY):
  """Query IEEE Reg Authority for RPi MAC.

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

def check_ieee_macs(query=IEEE_RA_QUERY, macs=RASPBERRY_PI_MACS):
  """Check and return new MAC prefixes, else return False."""
  new_macs = macs_from_ieee_ra(query)
  return new_macs if macs != new_macs else False
