from adafruit_ultimate_gps import GPS
from gps_movement import gps_movement
from motor import motor

'''
gps_device = GPS()
m = motor()
m.stop()
gps = gps_movement([38.532456,-121.795145])
coords = gps_device.obtain_coords()
distance = gps.get_distance(coords)
print(f"Distance {distance}")
heading = gps.get_heading(coords)
print(f"Heading {heading}")


required_rotation, direction = gps.get_adjusted_heading()

print(f"required rotation {required_rotation}")
print(direction)

m.face_correct_heading(required_rotation, direction)
'''


gps = gps_movement([38.532458,-121.795155])
gps.move_to_gps_coords_sequence()
