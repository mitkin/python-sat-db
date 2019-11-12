import rasterio
import json
import numpy as np

class RSAT2Reader(object):
    def __init__(self, filepath, read=True):
        self._filepath = filepath
        self._fh = None
        if read: self._read()

    def _read(self):
        self._fh = rasterio.open(self._filepath)

    def _get_geotransform(self):
        gt = self._fh.get_transform()
        if gt == [0.0, 1.0, 0.0, 0.0, 0.0, 1.0]:
            gt = _compute_geotranform_from_gcps(self._fh)
        return gt

    def to_json(self, outputpath):
        md = self._fh.tags()
        geometry = self._get_simple_coverage_polygon()
        geojson = {
            "type": "Feature",
            "geometry": geometry,
            "properties": md
        }
        with open(outputpath, mode="w") as of:
            json.dump(geojson, of)

    def close(self):
        self._fh.close()
    
    def _get_simple_coverage_polygon(self):
        return _transform_to_polygon(
            _compute_geotranform_from_gcps(self._fh),
            self._fh.width,
            self._fh.height
            )


def _compute_geotranform_from_gcps(fh):
    from rasterio.transform import from_gcps
    gcps = fh.get_gcps()
    return from_gcps(gcps[0])

def _transform_to_polygon(transform, w, h):
    px_width = transform[0]
    px_height = transform[4]
    north = transform[5]
    west = transform[2]
    south = north + px_height * (h + 1)
    east = west + px_width * (w + 1)

    xmin = west
    xmax = east
    ymin = south
    ymax = north

    polygon = {
        "coordinates":
        [
            [
            [xmin, ymin],
            [xmax, ymin],
            [xmax, ymax],
            [xmin, ymax],
            [xmin, ymin]
        ]
        ],
        "type": "Polygon"
    }
    
    return polygon

def gcps_to_polygon(gcps, w, h):
    row = [a.row for a in gcps]
    col = [a.col for a in gcps]
    lat = [a.lat for a in gcps]
    lon = [a.lon for a in gcps]
    

    
