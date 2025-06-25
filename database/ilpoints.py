def points(rank: int) -> float:
    """
    Calculates the number of points that a given IL rank deserves

    Parameters:
        rank - the rank to find points for

    Returns:
        The number of points, rounded to two decimal places
    """

    cutoff = 30

    if rank < 1:
        raise ValueError("Highest accepted rank is 1!")

    if rank > cutoff:
        return 0.0
    
    return round((100/cutoff) * ((cutoff-(rank-1))**2/cutoff), 2)
