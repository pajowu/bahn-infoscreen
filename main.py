import requests, json, time
from datetime import datetime
from pprint import pprint
from geopy.distance import distance


from status import Status
from tripinfo import TripInfo

OFFLINE = False
def get_elements():
    status = Status(OFFLINE)
    tripInfo = TripInfo(OFFLINE)

    yield status.get_time().strftime("%d.%m %H:%M:%S")

    #yield "{}. Klasse".format(2 if status["wagonClass"] == "SECOND" else 1 if status["wagonClass"] == "FIRST" else "UNKNOWN")

    yield "{} km/h".format(status["speed"])
    if not status.is_valid_gps():
        yield "{} GPS".format(status["gpsStatus"])


    yield "\n{} {}".format(tripInfo["trainType"], tripInfo["vzn"])
    yield "nach {}".format(tripInfo["stopInfo"]["finalStationName"])

    stops_by_evanr = {x["station"]["evaNr"]:x for x in tripInfo["stops"]}

    next_stop = tripInfo.get_stop_by_evanr(tripInfo["stopInfo"]["actualLastStarted"])

    distance_to_next_stop = abs(tripInfo["actualPosition"] - next_stop["info"]["distanceFromStart"]) / 1000
    distance_to_next_stop = distance((status["latitude"], status["longitude"]),(next_stop["station"]["geocoordinates"]["latitude"], status["longitude"])).km
    """for stop in tripInfo["stops"]:
        if distance_to_next_stop > 0:
            distance_to_next_stop -= stop["info"]["distance"]"""

    actualArrivalTime = next_stop["timetable"]["actualArrivalTime"] if next_stop["timetable"]["actualArrivalTime"] is not None else next_stop["timetable"]["actualDepartureTime"]
    secs_to_next = int((actualArrivalTime - status["serverTime"]) / 1000) / 60

    next_arrival_time = datetime.fromtimestamp(actualArrivalTime / 1000)


    yield "\nNächster Halt:"
    yield next_stop["station"]["name"]
    if actualArrivalTime > status["serverTime"]:
        secs_to_next = int((actualArrivalTime - status["serverTime"]) / 1000)
        next_arrival_time = datetime.fromtimestamp(actualArrivalTime / 1000)
        if secs_to_next <= 100:
            yield "in {:.1f} sec ({:%H:%M})".format(secs_to_next, next_arrival_time)
        else:
            yield "in {:.1f} min ({:%H:%M})".format(secs_to_next / 60, next_arrival_time)
        if next_stop["timetable"]["arrivalDelay"] and next_stop["delayReasons"] is not None:
            yield "({} - {})".format(next_stop["timetable"]["arrivalDelay"], ", ".join(x["text"] for x in next_stop["delayReasons"] ))
        elif next_stop["timetable"]["arrivalDelay"]:
            yield "({})".format(next_stop["timetable"]["arrivalDelay"])
        yield "({:.1f} km)".format(distance_to_next_stop)
        yield "auf Gleis {actual} ({scheduled})".format(**next_stop["track"])
    else:
        secs_to_next = int((next_stop["timetable"]["actualDepartureTime"] - status["serverTime"]) / 1000) / 60
        next_arrival_time = datetime.fromtimestamp(next_stop["timetable"]["actualDepartureTime"] / 1000)
        yield "Abfahrt in {:.1f} min ({:%H:%M})".format(secs_to_next, next_arrival_time)

def gen_text(elements, max_len):
    ml = max([len(x) for x in elements])
    lines = []
    for e in elements:
        if "\n" in e:
            lines.extend(e.splitlines())
        elif len(lines) > 0 and (len(lines[-1] + e) < max_len):
            lines[-1] += " " + e.strip()
        else:
            lines.append(e)

    return [x for x in lines if x]

def get_text(max_len = 30):
    elements = list(get_elements())
    return gen_text(elements, max_len)

def print_text():

    lines = get_text()
    for line in lines:
        if line:
            print(line)

    print(end='\f', flush=True)

if __name__ == '__main__':
    print_text()
