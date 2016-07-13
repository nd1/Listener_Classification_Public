#####################################################
# Creates a single-letter upper-case code for content type
#####################################################
def content_type_code(argument):
    switcher = {
        1: "N",
        9: "S",
        0: "S",
        15: "P"
    }
    return switcher.get(argument, "X")


#####################################################
# Creates a single-letter lower-case code for content ratings
#####################################################
def rate_code(argument):
    switcher = {
        "COMPLETED": "c",
        "THUMBUP": "t",
        "SKIP": "k",
        "SHARE": "h",
        "START": "r",
        "SRCHCOMPL": "l",
        "SRCHSTART": "s"
    }
    return switcher.get(argument, "x")


#####################################################
# Creates a single-digit code for device platform
#####################################################
def platform_code(argument):
    switcher = {
        "IPHONE": "1",
        "ANDROID": "2",
        "WINDOWPH": "3"
    }
    return switcher.get(argument, "X")


#####################################################
# Creates a single-letter lower-case code for content origin
#####################################################
def origin_code(argument):
    switcher = {
        "CURLIST": "a",
        "FEAATSPCL": "b",
        "FEATURED": "c",
        "FEATUREDB": "d",
        "FOLLOWING": "e",
        "LOCALPOD": "f",
        "RATED": "g",
        "SIMPLAFF": "h",
        "AFFIL": "i",
        "ARCHIVES": "j",
        "ASSIST": "k",
        "BREAK": "l",
        "CORE": "m",
        "EDTR": "n",
        "INVEST": "o",
        "LEAD": "p",
        "LOCALFALLB": "q",
        "NOTIFY": "r",
        "OPENDOOR": "s",
        "SELECTS": "t",
        "SPSTORY": "u",
        "WKENDNEWS": "v"
    }
    return switcher.get(argument, "x")
