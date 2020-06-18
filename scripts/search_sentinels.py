
def search_sentinels(df, aoi, dt=2, user=None, pwd=None,
                     proj_string='+init=EPSG:3995',
                     f_out=None, min_cloud_cover=0,
                     max_cloud_cover=100, product_type='S2MSI1C'):
    """
    Search Sentinel images overlapping ICESat-2 data within +- dt

    Parameters: (to be finished!)
    -----------
    df : panda dataframe
        ICESat-2 data
    aoi: str, list
        area of interest as WKT string or bounding box [lllon, lllat, urlon, urlat]
    dt: int, float
        difference in hours between CS2 and S2
    proj_string: str
        projection string to be used with the pyproj module
    min_cloud_cover: int, float
        Minimum cloud coverage in percentage
    max_cloud_cover: int, float
        Maximum cloud coverage in percentage


    Old:
    f_out:              str
        file name where to write the results

    Returns:
    --------

    """

    #==========================================================================
    # Pre-processing
    #==========================================================================

    ### Imports
    from sentinelsat import SentinelAPI
    # import wkt
    import pyproj
    import numpy as np
    import shapely.geometry as sg
    from shapely.wkt import dumps, loads
    from astropy.time import Time, TimeDelta
    from tqdm import tqdm

    ### Convert aoi to shapely polygon in projected CRS
    # define projection
    print("Creating AOI polygon...")
    proj        = pyproj.Proj(proj_string)
    # read aoi polygon
    if type(aoi) == str:
        aoi_temp    = loads(aoi)
    elif type(aoi) in (list, tuple):
        aoi_temp    = sg.box(aoi[0], aoi[1], aoi[2], aoi[3])
        aoi         = aoi_temp.wkt
    else:
        print("ERROR: 'aoi' should be provided as a WKT string or bounding box (list)")
        sys.exit(1)
    # project coordinates and convert to shapely polygon
    x, y        = proj(aoi_temp.exterior.xy[0], aoi_temp.exterior.xy[1])
    aoi_poly    = sg.Polygon(list(zip(x, y)))

    ### Convert dt to astropy time object
    dtt         = TimeDelta(3600 * dt, format='sec')

    #==========================================================================
    # Processing
    #==========================================================================

    ### Project IS2 data to desired CRS
    print("Selecting orbit data inside AOI...")
    lon, lat    = np.array(df['lons']), np.array(df['lats'])
    x, y        = proj(lon, lat)
    
    ### Extract IS2 orbit number
    is2_orbits  = np.unique(df['orbit_number'])
    print("N. of orbits/points inside AOI: {}/{}".format(len(is2_orbits),
                                                         len(df)))

    ### Extract time period from IS2 data to query the server
    t_is2       = Time(df['time'], scale='utc')
    t_is2_start = min(t_is2) - dtt
    t_is2_stop  = max(t_is2) + dtt

    ### Read metadata
    print("Query for metadata...")
    api = SentinelAPI(user, pwd,'https://scihub.copernicus.eu/dhus',
                      timeout=600)
    md  = api.query(area=aoi, date=(t_is2_start.datetime, t_is2_stop.datetime),
                    platformname='Sentinel-2', area_relation='Intersects',
                    cloudcoverpercentage=(min_cloud_cover, max_cloud_cover),
                    producttype=product_type)
    print("N. of total images: {}".format(len(md)))
    if len(md) == 0:
        return [], [], [], [], [], []

    ### Convert Sentinel-2 time strings to astropy time objects
    t_sen   = {}
    print("Converting time to astropy objects...")
    for el in md:
        t_sen[el]    = Time(md[el]['beginposition'], format='datetime',
                           scale='utc')

    ### Loop over orbits to find images that satisfy time costraints
    TimeDict    = {}
    t_is2       = []
    print("Looping over orbits to find intersections within {}h...".format(dt))
    for c, o in tqdm(enumerate(is2_orbits)):
        ### select CS2 data
        d_is2   = df[df['orbit_number'] == o]

        ### compute CS2 track central time
        t_temp      = Time(d_is2['time'], scale='utc')
        t_start_is2 = min(t_temp)
        t_stop_is2  = max(t_temp)
        t_is2_o     = t_start_is2 + (t_stop_is2 - t_start_is2) / 2
        t_is2.append(t_is2_o)

        ### save dict keys of images within +-dt from CS2
        i_t         = np.array(
            [el for el in md if np.abs((t_sen[el]  - t_is2_o).sec) <= dtt.sec])
        TimeDict[o] = i_t

    # get unique images within +-dt from all orbit data
    i_sen_t_int  = set(np.concatenate(list(TimeDict.values())).ravel())
    print("N. of images within {}h: {}".format(dt, len(i_sen_t_int)))
    if len(i_sen_t_int) == 0:
        return [], [], [], [], [], []

    ### Project images corner coordinates and convert to shapely polygons
    print("Creating images footprint polygons...")
    # loop over them, project corner coords and create polygons
    SenPolygonsDict  = {}
    for i in i_sen_t_int:
        # load S2 footprint
        aoi_sen      = loads(md[i]['footprint'])

        # check if multipolygon has more than 1 polygon defined
        if len(aoi_sen) > 1:
            print("WARNING: footprint for product {}".format(i),
                  "is defined by more than 1 polygon!!!")
        aoi_sen      = aoi_sen[0]

        # project corner coords
        x_sen, y_sen  = proj(aoi_sen.exterior.xy[0], aoi_sen.exterior.xy[1])

        # add polygon to dictionary
        SenPolygonsDict[i]   = sg.Polygon(list(zip(x_sen, y_sen)))


    ### Loop over orbits to find spatial intersections
    print("Looping over orbits to find intersections...")
    orbit_number    = []
    product_name    = []
    browse_url      = []
    download_url    = []
    t_diff          = []
    md_out          = {}
    for c, o in tqdm(enumerate(is2_orbits)):
        ### select CS2 data
        i       = df['orbit_number'] == o
        # check if track has at least 2 points
        if sum(i) < 2:
            continue
        d_is2    = df[i]
        x_is2    = x[i]
        y_is2    = y[i]

        ### create shapely line from CS track
        is2_line = sg.LineString(list(zip(x_is2, y_is2)))

        ### collect LS8 polygon indices
        i_sen    = TimeDict[o]

        ### Loop over S2 polygons
        for i_poly in i_sen:
            ls_poly     = SenPolygonsDict[i_poly]
            if is2_line.intersects(ls_poly):
                orbit_number.append(o)
                t_diff.append((t_sen[i_poly] - t_is2[c]).sec / 3600)
                product_name.append(md[i_poly]['filename'])
                download_url.append(md[i_poly]['link'])
                browse_url.append(md[i_poly]['link_icon'])
                md_out[i_poly]  = md[i_poly]

    print("N. of total intersections: {}".format(len(orbit_number)))

    ### Print to file
    if f_out != None:
        print("Printing results to {}...".format(f_out))
        with open(f_out, 'w') as fp:
            fp.write("orbit_number,t_diff_(h),product_id,dowload_url,browse_url\n")
            for i in range(len(orbit_number)):
                fp.write("{},{:.2f},{},{},{}\n".format(
                    orbit_number[i], t_diff[i], product_name[i],
                    download_url[i], browse_url[i]))

    return orbit_number, product_name, browse_url, download_url, t_diff, md_out

