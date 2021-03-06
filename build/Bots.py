'''
Lookup table for chip Id and ArUco Markers Mapping
With Getter functions
'''
# LUT Dictionary
A = {
    60  :   7889076,
    120 :   5167258,
    180 :   7893554,
    240 :   7892874
}

# Computations
key_list = list(A.keys())
val_list = list(A.values())

# ========Methods=========
# Method to get the chip Ids
def get_id(num):
    return A[num]
#Method to get the ArUco numbers
def get_num(id):
    return key_list[val_list.index(id)]



# test it yourself
if __name__ == '__main__':
    print(get_num(7892874))
    print(get_id(240))