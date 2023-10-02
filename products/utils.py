import datetime


def convert_to_time(seconds):
    time = datetime.timedelta(seconds=seconds)
    formatted_time = str(time)
    return formatted_time