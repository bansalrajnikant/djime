def colour(number):
    """
    This is just a simple function that return a colour code. It is used to
    create colour codes for some of the flashcharts.
    """
    if number%6 == 1:
        return '#FF0000'
    elif number % 6 == 2:
        return '#00FF00'
    elif number % 6 == 3:
        return '#0000FF'
    elif number % 6 == 4:
        return '#00FFFF'
    elif number % 6 == 5:
        return '#FF00FF'
    elif number % 6 == 0:
        return '#FFFF00'

