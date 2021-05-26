import json
import os
from shapely.geometry import Polygon, Point
import matplotlib.pyplot as plt
import matplotlib_terminal
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath('__file__'))

site_old_json_file = dir_path + "/site_old.json"
site_new_json_file = dir_path + "/site_new.json"
locations_json_file = dir_path + "/locations.json"


def _construct_polygon(coordinates):
    polygon = Polygon(coordinates)
    return polygon


def read_json_file(file_path):
    data = {}
    with open(file_path) as f:
        data = json.loads(f.read())
    return data


def convert_datetimeiso_to_datetime_obj(
        iso_format):
    return datetime.fromisoformat(iso_format)


def read_site_json_and_construct_polygon(json_file):
    data = read_json_file(json_file)
    geofence = data.get("geofence", {})
    start_datetime = convert_datetimeiso_to_datetime_obj(
        data.get("start_datetime"))
    end_datetime = convert_datetimeiso_to_datetime_obj(
        data.get("end_datetime"))
    coordinates = []
    if geofence.get("type") == "Polygon":
        coordinates = geofence.get("coordinates")[0]
    if coordinates:
        polygon = _construct_polygon(coordinates)
    return start_datetime, end_datetime, polygon


def write_to_file(data, file_name):
    with open(file_name, 'w') as outfile:
        json.dump(data, outfile)


def find_added_and_removed_locations(
        site_old_json_file, site_new_json_file, locations_json_file,
        create_graph=True):
    start_datetime, end_datetime, old_site_polygon = \
        read_site_json_and_construct_polygon(
            site_old_json_file)
    start_datetime, end_datetime, new_site_polygon = \
        read_site_json_and_construct_polygon(
            site_new_json_file)
    # find the difference
    removed_area = old_site_polygon.difference(new_site_polygon)
    added_area = new_site_polygon.difference(old_site_polygon)
    no_longer_contained_locations = []
    newly_added_locations = []
    added_location_xs = []
    added_location_ys = []
    removed_location_xs = []
    removed_location_ys = []

    with open(locations_json_file) as f:
        for line in f:
            item = json.loads(line)
            location_datetime = convert_datetimeiso_to_datetime_obj(
                item.get("datetime"))
            # for a site to contain a Location, the time of the
            # location should be in the time interval of the Site
            if not (start_datetime < location_datetime < end_datetime):
                continue
            if item.get("position", {}).get("type") == "Point":
                coordinates = item.get("position").get("coordinates")
                point = Point(coordinates)
                if added_area.contains(point):
                    newly_added_locations.append(item)
                    if create_graph:
                        added_location_xs.append(point.x)
                        added_location_ys.append(point.y)
                elif removed_area.contains(point):
                    no_longer_contained_locations.append(item)
                    if create_graph:
                        removed_location_xs.append(point.x)
                        removed_location_ys.append(point.y)
            else:
                continue
    # writes to json file in a single write
    write_to_file(no_longer_contained_locations, 'removed_locations.json')
    write_to_file(newly_added_locations, 'added_locations.json')
    if create_graph:
        x, y = old_site_polygon.exterior.xy
        a, b = new_site_polygon.exterior.xy
        plt.plot(a, b, c="green")
        plt.plot(x, y, c="red")
        plt.scatter(added_location_xs, added_location_ys,
                    c="green", label="Added locations")
        plt.scatter(removed_location_xs, removed_location_ys, c="red",
                    label="Removed locations")
        plt.savefig('visualization.png')
        plt.close()


find_added_and_removed_locations(
    site_old_json_file, site_new_json_file, locations_json_file)
