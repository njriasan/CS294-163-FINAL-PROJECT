# File that contains the code to generate a series of random points subject
# to specific parameters.

# Experiments should show varying in: Network density, radius, 
# Probability of individual failure, reporting threshold
# As well as examining the accuracy that can be obtained with
# various delta and epsilon values

import numpy as np
import matplotlib.pyplot as plt


class Location:

    def __init__(self, longitude, latitude):
        assert(isinstance(latitude, float))
        assert(isinstance(longitude, float))
        self.latitude = latitude
        self.longitude = longitude

    def return_coordinates(self):
        return (self.longitude, self.latitude)

    def get_euclidean_distance_from(self, other_location):
        assert(isinstance(other_location, Location))
        return np.sqrt(np.power(self.latitude - other_location.latitude, 2) + \
                np.power(self.longitude - other_location.longitude, 2))

origin = Location(0.0, 0.0)

class Sensor:

    def __init__(self, location, fnr):
        assert(isinstance(location, Location))
        assert(isinstance(fnr, float))
        assert(0.0 <= fnr <= 1.0)
        self.location = location
        self.fnr = fnr
        self.triggered = False
        self.witnessed_event = False

    def will_report_event(self):
        success_value = np.random.rand()
        self.triggered = True
        self.witnessed_event = bool(success_value > self.fnr)
        return self.witnessed_event

    def reset_event(self):
        self.triggered = False
        self.witnessed_event = False

    def report_actual_location(self):
        return self.location.return_coordinates()

    def get_euclidean_distance_from(self, other_location):
        assert(isinstance(other_location, Location))
        return self.location.get_euclidean_distance_from(other_location)

# Returns a list contain n sensors each within a random location
# in a circle centered at the origin each with failure rate fnr.
# To do this we follow the example given here: 
# https://programming.guide/random-point-within-circle.html
# which generates the cdf for a circle of radius r and samples
# based on that function.
def n_random_sensors_in_circle(n, r, fnr):
    sensors = []
    for _ in range(n):
        theta = 2 * np.random.rand() * np.pi
        radius = r * np.sqrt(np.random.rand())

        # Convert to lat and long
        lon = radius * np.cos(theta)
        lat = radius * np.sin(theta)
        loc = Location(lon, lat)
        sensors.append(Sensor(loc, fnr))
    return sensors

# Causes all sensors within r of the origin to give a response.
def trigger_event(sensors, r):
    for s in sensors:
        if s.get_euclidean_distance_from(origin) <= r:
            s.will_report_event()

# Calculates the percentage of sensors that detected the event
# that are within radius r of location
def calculate_percentage_success(sensors, r, location):
    total_within_r = 0.0
    success_within_r = 0.0
    for s in sensors:
        if s.get_euclidean_distance_from(location) <= r and s.triggered:
            total_within_r += 1.0
            if s.witnessed_event:
                success_within_r += 1.0
    return success_within_r / total_within_r


def find_closest_sensor(sensors):
    min_value = float("inf")
    closest_sensor = None
    for s in sensors:
        dist = s.get_euclidean_distance_from(origin)
        if dist < min_value:
            min_value = dist
            closest_sensor = s
    assert(closest_sensor is not None)
    return closest_sensor

def calculate_origin_percentage_success(sensors, r):
    return calculate_percentage_success(sensors, r, origin)

def calculate_centered_percentage_success(sensors, r, closest_sensor):
    closest_location = closest_sensor.location
    return calculate_percentage_success(sensors, r, closest_location)

def n_random_sensors_in_ring(n, r1, r2, fnr=1):
    pass

def calculate_percentage_success_dp(sensors, r):
    pass

def calculate_centered_percentage_success(sensors, r):
    pass

# Resets all sensors. This allows running multiple tests on the
# same sensor distribution
def reset_sensors(sensors):
    for s in sensors:
        s.reset_event()

# Plots the locations given by all sensors that
# responded detecting the event in red, all sensors
# that responded a miss in blue, and all sensors
# that were out of range in black.
def plot_sensor_results(sensors, r, fnr):
    success_color = ("red")
    failure_color = ("blue")
    missed_color = ("black")
    success_lons = []
    success_lats = []
    failure_lons = []
    failure_lats = []
    missed_lons = []
    missed_lats = []
    for s in sensors:
        loc_coor = s.report_actual_location()
        if s.get_euclidean_distance_from(origin) <= r:
            if s.triggered:
                if s.witnessed_event:
                    success_lons.append(loc_coor[0])
                    success_lats.append(loc_coor[1])
                else:
                    failure_lons.append(loc_coor[0])
                    failure_lats.append(loc_coor[1])
            else:
                missed_lons.append(loc_coor[0])
                missed_lats.append(loc_coor[1])
        else:
            missed_lons.append(loc_coor[0])
            missed_lats.append(loc_coor[1])
    plt.scatter(np.array(success_lons), np.array(success_lats), c=success_color)
    plt.scatter(np.array(failure_lons), np.array(failure_lats), c=failure_color)
    plt.scatter(np.array(missed_lons), np.array(missed_lats), c=missed_color)
    plt.title('Distribution of sensor successes in a circle of radius {} with failure rate {}'.format (r, fnr))
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()

def test1():
    fnr = 0.05
    r = 5.0
    sensors = n_random_sensors_in_circle(100000, r, fnr)
    for i in range(1):
        trigger_event(sensors, r)
        print (calculate_percentage_success(sensors, r))
        plot_sensor_results(sensors, r / 2, fnr)
        reset_sensors(sensors)

if __name__ == "__main__":
    test1()
