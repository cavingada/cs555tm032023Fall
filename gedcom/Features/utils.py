from datetime import datetime

""" returns 
1: date1 > date2
-1: date1 < date2 
0: date1 = date2 
format of date1 and date 2 is two strings of this exammple: 9 SEP 1999"""
def compare_dates(date1, date2):
    # convert date strings into datetime objects
    try:
        d1 = datetime.strptime(date1, "%d %b %Y")
        d2 = datetime.strptime(date2, "%d %b %Y")
    except ValueError:
        # invalid formats
        raise Exception("Invalid date format")

    # Compare and return
    if d1 > d2:
        return 1
    elif d1 < d2:
        return -1
    else:
        return 0