import math

def create_circular_geometry(lat, lon, radius_km, num_points=36):
    """
    Creates a circular polygon in Well-Known Text (WKT) format around a given point.

    Args:
        lat (float): Latitude of the center point in degrees.
        lon (float): Longitude of the center point in degrees.
        radius_km (float): Radius of the circle in kilometers.
        num_points (int): Number of points to approximate the circle.

    Returns:
        str: WKT string representing the circular polygon.
    """
    # Average radius of the Earth in kilometers
    R = 6371.0

    # Convert the radius from linear distance to angular distance in radians
    radius_rad = radius_km / R

    points = []
    for i in range(num_points + 1):
        # Calculate the angle for each point (evenly divided)
        angle = 2 * math.pi * i / num_points

        # Calculate displacements in latitude and longitude
        delta_lat = radius_rad * math.sin(angle)
        delta_lon = radius_rad * math.cos(angle) / math.cos(math.radians(lat))

        # Convert the displacements to degrees and add them to the central coordinates
        new_lat = lat + math.degrees(delta_lat)
        new_lon = lon + math.degrees(delta_lon)

        # Add the point to the list in "longitude latitude" format
        points.append(f"{new_lon} {new_lat}")

    # Form the WKT string of the polygon
    polygon = f"POLYGON(({', '.join(points)}))"
    return polygon

