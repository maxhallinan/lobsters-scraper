import datetime

datetime_string = "2018-03-05 03:25:31 -0600"

datetime_string_format = "%Y-%m-%d %H:%M:%S %z"

dt = datetime.datetime.strptime(datetime_string, datetime_string_format)

ts = dt.timestamp()

print(ts)
