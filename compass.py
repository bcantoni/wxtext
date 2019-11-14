def degrees_direction(degrees):
    "Convert wind direction from 0..15 to compass point text"
    compass_directions = (
        'N', 'NNE', 'NE', 'ENE',
        'E', 'ESE', 'SE', 'SSE',
        'S', 'SSW', 'SW', 'WSW',
        'W', 'WNW', 'NW', 'NNW',
    )
    index = int((degrees / 22.5) + 0.5) % 16
    return compass_directions[index]


if __name__ == '__main__':
    tests = [0, 33, 45, 85, 130, 250, 355]
    for t in tests:
        print("{} degrees = {}".format(t, degrees_direction(t)))
