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

# Computations
key_list = list(SD.keys())
val_list = list(SD.values())

# Method to get the strings for user
def get_name(i):
    if i in SD.keys():
        return SD[i]
    return "Bots"
# Method to get ArUco Id from String
def get_id(i):
    return key_list[val_list.index(i)]