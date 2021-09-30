# LUT Dictionary
SD= {
    831:"S1",
    832:"S2",
    833:"S3",
    834:"S4",
    681:"D1",
    682:"D2",
    683:"D3",
    684:"D4"
}

def get(i):
    if i in SD.keys():
        return SD[i]
    return "Bots"