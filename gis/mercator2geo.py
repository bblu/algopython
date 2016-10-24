from decimal import Decimal
import math

def webmercator2geo(mx,my):
    if (math.fabs(mx) > 20037508.3427892) or (math.fabs(my) > 20037508.3427892):
        return NULL;
    if math.fabs(mx) < 180 and math.fabs(my) < 90:
        return NULL;


    x = mx
    y = my
    num3 = x / 6378137.0
    num4 = num3 * 57.295779513082323
    num5 = math.floor(((num4 + 180.0) / 360.0))
    num6 = num4 - (num5 * 360.0)
    num7 = 1.5707963267948966 - (2.0 * math.atan(math.exp((-1.0 * y) / 6378137.0)))
    lon = num6
    lat = num7 * 57.295779513082323
    return lon,lat



geo = webmercator2geo(13792610.8276824,7072436.33446523)
print geo
