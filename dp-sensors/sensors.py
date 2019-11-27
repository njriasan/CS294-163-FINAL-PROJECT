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

class Sensor:

    def __init__(self, location, fnr):
        assert(isinstance(location, Location))
        assert(isinstance(fnr, float))
        assert(0.0 <= fnr <= 1.0)
        self.location = location
        self.fnr = fnr

    def will_report_event(self):
        success_value = np.random.rand()
        print (success_value)
        return bool(success_value > self.fnr)

    def report_actual_location(self):
        return self.location.return_coordinates()


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

# Plots the locations given by all sensors that
# responded detecting the event
def plot_sensor_responses(sensors, color="red"):
    lons = []
    lats = []
    for s in sensors:
        loc_coor = s.report_actual_location()
        lons.append(loc_coor[0])
        lats.append(loc_coor[1])
    colors = (color)
    plt.scatter(np.array(lons), np.array(lats), c=colors)
    plt.title('Distribution of sensors in a circle of radius 5.0')
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    plt.show()


def test1():
    sensors = n_random_sensors_in_circle(100000, 5.0, 0.05)
    plot_sensor_responses(sensors)

if __name__ == "__main__":
    test1()
