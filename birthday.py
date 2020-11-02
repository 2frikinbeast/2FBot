from general_util import remove_prefix


def number_to_month(month):
    switcher = {
        1: "January",
        2: "February",
        3: "March",
        4: "April",
        5: "May",
        6: "June",
        7: "July",
        8: "August",
        9: "September",
        10: "October",
        11: "November",
        12: "December"
    }
    return switcher.get(int(month), "Invalid month")
    pass


def string_to_ymd(date_string):
    if date_string[0:4] == "6969":
        year = None
    else:
        year = date_string[0:4]
    month = date_string[5:7]
    day = remove_prefix(date_string[8:10], "0")
    date_dictionary = {
        "year": year,
        "month": month,
        "month_name": number_to_month(month),
        "day": day
    }
    return date_dictionary
