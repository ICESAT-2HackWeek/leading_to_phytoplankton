from .dataset import *
from sentinelsat import SentinelAPI # external dependencyto use Sentinel API
import numpy as np
import pyproj
import shapely.wkt as wkt
import shapely.geometry as sg
#from shapely.ops import unary_union
#from astropy.time import TimeDelta, Time, TimeYearDayTime
from tqdm import tqdm

class Sentinels(DataSet):

    def __init__(self, shape, timeframe):
        self.shape = shape
        # call coord standardization method (see icepyx)
        self.bounding_box = shape.exterior.bounds
        self.time_frame = timeframe # call fmt_timerange

    def _interpolate_polygon_from_corners(self, x, y, nx=100, ny=100):
        """Update. Maybe substitute with some icepyx functionality"""

        ### Compute x, y
        xx  = []
        yy  = []
        for i in range(len(x)-1):
            if x[i] == x[i+1]:
                xx = np.append(xx, [x[i]] * nx)
            else:
                xx = np.append(xx, np.linspace(x[i], x[i+1], nx))
            if y[i] == y[i+1]:
                yy = np.append(yy, [y[i]] * ny)
            else:
                yy = np.append(yy, np.linspace(y[i], y[i+1], ny))

        # ### Append first corner to close polygon
        # if x[-1] == x[0]:
        #     xx = np.append(xx, [x[-1]] * nx)
        # else:
        #     xx = np.append(xx, np.linspace(x[-1], x[0], nx))
        # if y[-1] == y[0]:
        #     yy = np.append(yy, [y[-1]] * ny)
        # else:
        #     yy = np.append(yy, np.linspace(y[-1], y[0], ny))

        return xx, yy

    def search_data(self, usr, pwd, queryparams):

        self.query_params = queryparams
        self.proj4_string = 'EPSG:3995' # make this an input

        ### Print query parameters
        print("Querying {} with:".format(queryparams['platformname']))
        for k in self.query_params:
            if k not in ('platformname',):
                print(k + ': {}'.format(self.query_params[k]))

        ### Interpolate polygon coordinates (already implemented in icepyx?)
        proj        = pyproj.Proj(self.proj4_string)
        lon_p, lat_p  = self._interpolate_polygon_from_corners(
            self.shape.exterior.xy[0], self.shape.exterior.xy[1],
            nx=1000, ny=1000)
        x, y        = proj(lon_p, lat_p)
        aoi_poly    = sg.Polygon(list(zip(x, y)))

        ### !!!! add check for maximum longitude range 180 deg

        ### Time strings to Time objects
        t_start     = Time(self.time_frame[0], format='iso', scale='utc')
        t_stop      = Time(self.time_frame[1], format='iso', scale='utc')
        print("Query for metadata between {} and {}...".format(
            t_start.utc.iso, t_stop.utc.iso))

        ### Query data
        api = SentinelAPI(usr, pwd, timeout=60000)
        out = api.query(area=self.shape.to_wkt(),
                        date=(t_start.datetime, t_stop.datetime),
                        **self.query_params)
        print("N. of hits:", len(out))

        return out

    def download(self, queryresult, outpath):

        raise NotImplementedError
