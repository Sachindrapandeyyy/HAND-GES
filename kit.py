import math

def Linemag(point1, point2):
    """
    Calculate the magnitude of a line segment defined by two points.
    Args:
        point1: Tuple containing (x, y) coordinates of the first point.
        point2: Tuple containing (x, y) coordinates of the second point.
    Returns:
        The magnitude of the line segment.
    """
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def distance(point1, point2):
    """
    Calculate the Euclidean distance between two points.
    Args:
        point1: Tuple containing (x, y) coordinates of the first point.
        point2: Tuple containing (x, y) coordinates of the second point.
    Returns:
        The Euclidean distance between the two points.
    """
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

def R_sq(x1, y1, x2, y2, x3, y3):
    """
    Calculate the squared radius of the circle defined by three points.
    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.
        x3, y3: Coordinates of the third point.
    Returns:
        The squared radius of the circle defined by the three points.
    """
    A = x1 * (y2 - y3) - y1 * (x2 - x3) + x2 * y3 - y2 * x3
    B = (x1 ** 2 + y1 ** 2) * (y3 - y2) + (x2 ** 2 + y2 ** 2) * (y1 - y3) + (x3 ** 2 + y3 ** 2) * (y2 - y1)
    C = (x1 ** 2 + y1 ** 2) * (x2 - x3) + (x2 ** 2 + y2 ** 2) * (x3 - x1) + (x3 ** 2 + y3 ** 2) * (x1 - x2)
    return (A ** 2 + B ** 2 + C ** 2) / ((x1 - x2) ** 2 + (y1 - y2) ** 2)

def get_swipe_direction(prev_x, prev_y, curr_x, curr_y):
    """
    Determine the swipe direction based on previous and current positions.
    Args:
        prev_x, prev_y: Previous position coordinates.
        curr_x, curr_y: Current position coordinates.
    Returns:
        A string representing the swipe direction ("left", "right", "up", "down"),
        or None if the movement is too small to be considered a swipe.
    """
    dx = curr_x - prev_x
    dy = curr_y - prev_y
    delta = 20  # Minimum delta for swipe detection

    if abs(dx) > abs(dy):
        if dx > delta:
            return "right"
        elif dx < -delta:
            return "left"
    else:
        if dy > delta:
            return "down"
        elif dy < -delta:
            return "up"

    return None
