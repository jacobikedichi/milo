"""
A utility module that uses google's map elevation api to calcuate the highest elevation between two points.
"""
__author__ = "Jacob Ikedichi"

import simplejson, urllib, argparse
from requests.exceptions import HTTPError

GOOGLE_ELEVATION_URL = 'https://maps.googleapis.com/maps/api/elevation/json'


def get_elevation():
    """
    Retrieves and returns the highest elevations between two points/paths (specified by lat,long lat,long).
    """
    
    description = 'Prints the highest elevation between 2 coordinates. Note: Latitude values must be an\
    integer/floating point value between -90 and 90. Longitude values must be an integer/floating point\
    value between -180 and 180'
    parser = argparse.ArgumentParser(description = description, 
                                     prefix_chars='@',
                                     prog = 'PROG', usage='%(prog)s lat,long lat,long')
    parser.add_argument('first_location', help='First coordinate. i.e lat, long')
    parser.add_argument('second_location', help='Second coordinate. i.e lat, long')
    parser.add_argument("@@samples", default=100, type=int, 
                        help="specifies the number of sample points along a path for which to return elevation data.\
                        The samples parameter divides the given path into an ordered set of equidistant points along\
                        the path")
    
    
    args = parser.parse_args()

    first_location = args.first_location.split(',')
    second_location = args.second_location.split(',')
    samples = args.samples
    
    assert len(first_location) == 2, 'First Location must be a comma separated lat long value'
    assert len(second_location) == 2, 'Second Location must be a comma separated lat long value'
    
    try:
        lat1 = float(first_location[0]) 
        lon1 = float(first_location[1])
        lat2 = float(second_location[0]) 
        lon2 = float(second_location[1])
    except ValueError:
        raise ValueError("Latitude and Longitudes must be integer or floating point values")
    
    #We need to check that the values they supplied for both lats and longs are within range.
    #Latitudes must be between -90 and 90, while Longitudes must be between -180 and 180
    assert -90 <= lat1 <= 90 and -90 <= lat2 <= 90, 'Latitudes values must be between -90 and 90'
    assert -180 <= lon1 <= 180 and -180 <= lon2 <= 180, 'Longitude values must be between -180 and 180'
    
    params = urllib.urlencode({'path': args.first_location + "|" + args.second_location, 'samples': samples})
    response = urllib.urlopen(GOOGLE_ELEVATION_URL + "?%s" %params)
    if response.code == 200:
        elevations = simplejson.load(response)
        if elevations.get('status') == 'OK':
            return max([elevation.get('elevation') for elevation in elevations.get("results")])
        else:
            raise Exception(elevations.get("status") + "! " + elevations.get('error_message', 
                'elevation could not be determined'))
    elif response.code == 404:
        raise HTTPError('404 Error! Unable to locate google\'s map elevation api')
    else:
         raise Exception(response.code + ' Error! Unknown error occured')
    
if __name__ == '__main__':
    print get_elevation()
