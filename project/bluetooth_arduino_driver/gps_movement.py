from motor import motor
import math
import time
from adafruit_ultimate_gps import GPS

class gps_movement:

    def __init__(self, coords):
        # coords[0] = latitude, coords[1] = longitude  
        self.coords = coords     
        self.distance = 0
        self.current_heading = 260
        self.dest_heading = 320
        self.min_distance = 3 
        self.min_degrees = 10
        self.gps_device = GPS()
        self.m = motor()

        
    
    def get_distance(self, currentCoords):  
        # Radius of the Earth in kilometers
        R = 6371.0
        currentLatitude = currentCoords[0]
        currentLongitude = currentCoords[1]
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(currentLatitude)
        lon1_rad = math.radians(currentLongitude)
        lat2_rad = math.radians(self.coords[0])
        lon2_rad = math.radians(self.coords[1])

        # Calculate the differences
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Haversine formula for distance
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        # convert distance to meters
        distance = R * c * 1000

        return distance

    def get_heading_move(self, coords1, coords2):
        # Radius of the Earth in kilometers
        R = 6371.0
        currentLatitude = coords1[0]
        currentLongitude = coords2[1]
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(currentLatitude)
        lon1_rad = math.radians(currentLongitude)
        lat2_rad = math.radians(coords2[0])
        lon2_rad = math.radians(coords2[1])

        # Calculate the differences
        dlon = lon2_rad - lon1_rad

        # Calculate the heading using arctangent
        x = math.sin(dlon) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))

        initial_heading = math.atan2(x, y)

        # Convert heading from radians to degrees
        initial_heading = math.degrees(initial_heading)

        # Normalize heading to be between 0 and 360 degrees
        initial_heading = (initial_heading + 360) % 360
        #self.dest_heading = initial_heading
        return initial_heading

    def get_heading(self, currentCoords):
        # Radius of the Earth in kilometers
        R = 6371.0
        currentLatitude = currentCoords[0]
        currentLongitude = currentCoords[1]
        # Convert latitude and longitude from degrees to radians
        lat1_rad = math.radians(currentLatitude)
        lon1_rad = math.radians(currentLongitude)
        lat2_rad = math.radians(self.coords[0])
        lon2_rad = math.radians(self.coords[1])

        # Calculate the differences
        dlon = lon2_rad - lon1_rad

        # Calculate the heading using arctangent
        x = math.sin(dlon) * math.cos(lat2_rad)
        y = math.cos(lat1_rad) * math.sin(lat2_rad) - (math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon))

        initial_heading = math.atan2(x, y)

        # Convert heading from radians to degrees
        initial_heading = math.degrees(initial_heading)

        # Normalize heading to be between 0 and 360 degrees
        initial_heading = (initial_heading + 360) % 360
        #self.dest_heading = initial_heading
        return initial_heading
    
    def get_adjusted_heading(self):
        print(f"currentHeading: {self.current_heading}") 
        print(f"destHeading: {self.dest_heading}") 
        resultheading = self.dest_heading - self.current_heading
        adj_heading = 360 - abs(resultheading)
        
        #heading = 0
        direction = ""
        if adj_heading < 180:
            heading = adj_heading
            
            if resultheading < 0:
                direction = "CW"
            else:
                direction = "CCW"

        else: 
            heading = resultheading
            
            if resultheading < 0:
                direction = "CCW"
            else:
                direction = "CW"
        return heading, direction

    def start_sequence(self):
        first_coords = self.gps_device.obtain_coords()
        self.coords = first_coords
        self.m.drive_forward()
        
	
        time.sleep(10)
        
        self.m.stop()
        second_coords = self.gps_device.obtain_coords()
        initial_heading = self.get_heading(second_coords)
	
        print(f"INITIAL_HEADING {initial_heading}")
        self.current_heading = initial_heading
	
 
        

    def move_to_gps_coords_sequence(self):
        # make sure motors have stopped 
        self.m.stop()
        coords = self.gps_device.obtain_coords()
        distance = self.get_distance(coords)
        print(f"Distance {distance}")
        heading = self.get_heading(coords)
        print(f"Heading {heading}")
        required_rotation, direction = self.get_adjusted_heading()
        print(f"required rotation {required_rotation}")
        print(direction)
        self.m.face_correct_heading(required_rotation, direction)     
        self.m.drive_forward()
	    
        coords_1 = self.gps_device.obtain_coords()
        self.m.drive_forward()
        coords_2 = self.gps_device.obtain_coords()
        print(coords_1)
        print(coords_2)
        current_heading_on_move = self.get_heading_move(coords_1, coords_2)
        print(current_heading_on_move)

        self.m.stop()  
        '''
        while distance > self.min_distance:
            self.m.drive_forward()
	    
            coords_1 = self.gps_device.obtain_coords()
            coords_2 = self.gps_device.obtain_coords()
            current_heading_on_move = self.get_heading_move(coords_1, coords_2)
            
            self.current_heading = current_heading_on_move
            print(current_heading_on_move)
            current_coords_on_move = self.gps_device.obtain_coords()

            distance = self.get_distance(current_coords_on_move)
            adj_heading, adj_direction = self.get_adjusted_heading()

            self.m.movement_correction(adj_heading, adj_direction)
'''



