from motor import motor
import math
from adafruit_ultimate_gps import GPS

class gps_movement:

    def __init__(self, coords):
        # coords[0] = latitude, coords[1] = longitude  
        self.coords = coords     
        self.distance = 0
        self.heading = 0
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
        self.heading = initial_heading
        return initial_heading
    
    def get_adjusted_heading(self, currentHeading):
        print(f"currentHeading: {currentHeading}") 
        print(f"destHeading: {self.heading}") 
        resultheading = self.heading - currentHeading
        adj_heading = 360 - abs(resultheading)
        
        heading = 0
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

         
     
        

    def move_to_gps_coords_sequence(self):
        # make sure motors have stopped 
        self.m.stop()
        # obtain current robot coordinates 
        current_coords = self.gps_device.obtain_coords()
        # determine distance from dest coords
        distance = self.get_distance(current_coords)
        # determine heading to travel
        current_heading = self.get_heading(current_coords)
        # determine which direction to rotate and how many degrees to rotate by
        adj_heading, adj_direction = self.get_adjusted_heading(current_heading)
        print(f"adjusted heading")
        # rotate to correct general heading 
        self.m.face_correct_heading(adj_heading, adj_direction)

        
       # while distance > self.min_distance:
         #   self.m.drive_forward()
          #  self.m.movement_correction(current_heading, distance)



