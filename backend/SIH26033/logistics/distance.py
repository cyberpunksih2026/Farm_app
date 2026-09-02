def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Demo geographic distance metric.

    IMPORTANT:
    This is NOT road distance and the returned value is not kilometres.
    It is suitable only for the current prototype ranking demonstration.
    """
    return ((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2) ** 0.5
