#!/usr/bin/env python3

import sys
from satdb.readers import rsat2
import zipfile
import tempfile

tdir = tempfile.mkdtemp()
with zipfile.ZipFile("{}.zip".format(sys.argv[1])) as zp:
    zp.extract("{}/product.xml".format(sys.argv[1]), path="{}\{}".format(tdir, sys.argv[1]))
    a = rsat2.RSAT2Reader("{}\{}".format(tdir, sys.argv[1]))
    a.to_json("out.json")
