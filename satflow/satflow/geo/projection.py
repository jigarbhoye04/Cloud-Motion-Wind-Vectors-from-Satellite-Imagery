"""Geospatial projection utilities."""

def latlon_to_pixel(lat, lon, proj_params):
    """
    Convert latitude and longitude to pixel coordinates.

    Args:
        lat (float): Latitude.
        lon (float): Longitude.
        proj_params (dict): Projection parameters.

    Returns:
        (int, int): Pixel coordinates (x, y).
    """
    # TODO: Implement forward projection
    raise NotImplementedError("latlon_to_pixel not implemented")


def pixel_to_latlon(x, y, proj_params):
    """
    Convert pixel coordinates to latitude and longitude.

    Args:
        x (int): Pixel X coordinate.
        y (int): Pixel Y coordinate.
        proj_params (dict): Projection parameters.

    Returns:
        (float, float): (lat, lon).
    """
    # TODO: Implement inverse projection
    raise NotImplementedError("pixel_to_latlon not implemented")
