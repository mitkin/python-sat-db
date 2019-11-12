#!/usr/bin/env python

import unittest
import os
import tempfile

class TestRSAT2Reader(unittest.TestCase):
    """Test Radarsat2 reader"""

    def setUp(self):
        self._filepath = os.path.join(
            'tests',
            'test_data',
            'RS2_20191101_060829_0076_SCWA_HHHV_SGF_768757_0253_31179132'
            )

    def test_instantiate(self):
        from satdb.readers import rsat2
    
    def test_sample_data_exists(self):
        assert os.path.exists(self._filepath)

    def test_reader_accepts_rsdata(self):
        from satdb.readers import rsat2
        obj = rsat2.RSAT2Reader(self._filepath)
        self.assertIsInstance(obj, rsat2.RSAT2Reader)

    def test_reader_gets_geotransform(self):
        from satdb.readers import rsat2
        import affine
        obj = rsat2.RSAT2Reader(self._filepath)
        self.assertIsInstance(obj, rsat2.RSAT2Reader)
        gt = obj._get_geotransform()
        self.assertIsInstance(gt, affine.Affine)
    
    def test_simple_coverage_polygon(self):
        from satdb.readers import rsat2
        obj = rsat2.RSAT2Reader(self._filepath)
        self.assertIsInstance(obj._get_simple_coverage_polygon(), dict)
        
    def test_to_json(self):
        from satdb.readers import rsat2
        obj = rsat2.RSAT2Reader(self._filepath)
        with tempfile.NamedTemporaryFile(delete=False) as tf:
            obj.to_json(tf.name)

if __name__ == "__main__":
    unittest.main()