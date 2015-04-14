import pyproj

osgb36 = pyproj.Proj("+init=EPSG:27700")
wgs84 = pyproj.Proj("+init=EPSG:4326")


def osgb_to_wgs84(easting, northing):
    return pyproj.transform(osgb36, wgs84, easting, northing)

# http://snorf.net/blog/2014/08/12/converting-british-national-grid-and-irish-grid-references/
# 5x5 grid letters, missing I
alphabet = 'ABCDEFGHJKLMNOPQRSTUVWXYZ'


def grid_to_xy(false_easting, false_northing, gridsizes, grid_ref):
    '''Convert grid reference to coordinates'''
    # false easting and northing
    easting = -false_easting
    northing = -false_northing

    # convert letter(s) to easting and northing offset
    for n in range(0, len(gridsizes)):
        letter = grid_ref[n]
        idx = alphabet.index(letter)
        col = (idx % 5)
        row = 4 - ((idx) / 5)
        easting += (col * gridsizes[n])
        northing += (row * gridsizes[n])

    grid_ref = grid_ref[len(gridsizes):]

    e = '{:0<5}'.format(grid_ref[0:len(grid_ref)//2])
    e = '{}.{}'.format(e[0:5], e[5:])
    easting += float(e)

    n = '{:0<5}'.format(grid_ref[len(grid_ref)//2:])
    n = '{}.{}'.format(n[0:5], n[5:])
    northing += float(n)

    return easting, northing


def ngr_to_osgb(ngr):
    return grid_to_xy(1000000, 500000, [500000, 100000], ngr)


def ngr_to_wgs84(ngr):
    easting, northing = ngr_to_osgb(ngr)
    return osgb_to_wgs84(easting, northing)
