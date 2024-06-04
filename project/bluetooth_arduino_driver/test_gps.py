from adafruit_ultimate_gps import GPS
from gps_movement import gps_movement
from motor import motor



gps_device = GPS()
m = motor()
gps = gps_movement([38.536975,-121.753763])
coords = gps_device.obtain_coords()
distance = gps.get_distance(coords)
print(f"Distance {distance}")

heading = gps.get_heading(coords)
print(f"Heading {heading}")


required_rotation, direction = gps.get_adjusted_heading(338)

print(f"required rotation {required_rotation}")
print(direction)

m.face_correct_heading(required_rotation, direction)


'''
gps = gps_movement([38.536975,-121.753763])
gps.move_to_gps_coords_sequence()
'''