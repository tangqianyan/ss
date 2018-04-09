


def map_weather():
    weather_dict = {}
    i = 0
    with open('01.txt') as f:
        for line in f:
            if line == '\n':
                continue
            else:
                line = line.strip().split(' ')[1:]
                line = ' '.join(line)
                weather_dict.setdefault(line,i+1)
                i += 1
    print (weather_dict)

if __name__ == "__main__":
    map_weather()