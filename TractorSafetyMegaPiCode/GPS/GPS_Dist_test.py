import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate the differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula for distance
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c * 1000

    return distance

def heading(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

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

    return initial_heading

# Example coordinates for points A and B
point_A = (38.558268, -121.698892)  # San Francisco, CA
point_B = (38.558290, -121.698917)  # Los Angeles, CA

# Calculate distance
distance = haversine(point_A[0], point_A[1], point_B[0], point_B[1])
print(f"Distance between A and B: {distance:.6f} m")

# Calculate heading
heading_angle = heading(point_A[0], point_A[1], point_B[0], point_B[1])
print(f"Heading from A to B: {heading_angle:.2f} degrees")
