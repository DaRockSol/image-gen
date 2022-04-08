def arrayToString(someArray):
    baseString = "-"
    newArray = []
    for thing in someArray:
        newArray.append(str(thing))
    return (baseString.join(newArray))

def numJoin(someArray):
    baseString = ""
    newArray = []
    for thing in someArray:
        newArray.append(str(thing))
    return (baseString.join(newArray))