import matplotlib.pyplot as plt
import os
import pyproj
import pandas as pd


def plot_lat_long_points(points):
    # for lat, long in points:
    print(points)
    plt.scatter(x=[x[0] for x in points], y=[x[1] for x in points])
    plt.plot(points[0], points[-1])
    plt.show()


def gps_to_ecef_pyproj(lat_long_alt):
    if len(lat_long_alt) == 3 and lat_long_alt[-1] != -1:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y, z = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], lat_long_alt[2], radians=False)
        return (x, y, z)
    else:
        ecef = pyproj.Proj(proj='geocent', ellps='WGS84', datum='WGS84')
        lla = pyproj.Proj(proj='latlong', ellps='WGS84', datum='WGS84')
        x, y = pyproj.transform(lla, ecef, lat_long_alt[0], lat_long_alt[1], radians=False)
        return (x, y)


def delete_keys_dict(dict_, keys):
    """
    Delete multiple keys from a dictionary
    Args:
        dict_ (dict): Dictionary in which keys need to be removed
        keys (ndarray): List of keys to be removed

    Returns:
        dict_ with removed keys
    """
    for k in keys:
        del dict_[k]
    return dict_


def get_bounding_box_coordinates(n, probe_dict, link_data):
    """
    Get bounding box for each zone of the map
    Args:
        n (int): Number of part to divide each side in to. For n=2, divide entire map into 4 parts (2x2).
        probe_dict (dict): Dictionary of all probe points
        link_data (dataframe): Pandas df of all link data

    Returns:
        coordinates dictionary for each zone number as key and it's bounding box coordinates as it values

    """
    print(probe_dict, link_data)


def slope_using_two_points(x1, x2, y1, y2):
    return (y1 - y2) / (x1 - x2)


if __name__ == "__main__":
    data = 'data'
    link_cols = ['linkPVID', 'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'shapeInfo']
    probe_cols = ['sampleID', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_header = ['linkPVID', 'refNodeID', 'nrefNodeID', 'length', 'functionalClass', 'directionOfTravel',
                   'speedCategory',
                   'fromRefSpeedLimit', 'toRefSpeedLimit', 'fromRefNumLanes', 'toRefNumLanes', 'multiDigitized',
                   'urban',
                   'timeZone', 'shapeInfo', 'curvatureInfo', 'slopeInfo']
    probe_header = ['sampleID', 'dateTime', 'sourceCode', 'latitude', 'longitude', 'altitude', 'speed', 'heading']
    link_data = pd.read_csv(os.path.join(data, 'Partition6467LinkData.csv'), names=link_header, usecols=link_cols,
                            index_col='linkPVID')
    probe_data = pd.read_csv(os.path.join(data, 'Partition6467ProbePoints.csv'), names=probe_header, usecols=probe_cols)

    probe_dict = probe_data.sample(n=100).to_dict('index')
    get_bounding_box_coordinates(4, probe_dict, link_data.iloc[0:10])
