'''
Lookup table for chip Id and ArUco Markers Mapping
With Getter functions
'''
# LUT Dictionary
A = {
    60  :   7892874,
    120 :   7870122,
    180 :   7893554,
    240 :   7889076
}

# Computations
key_list = list(A.keys())
val_list = list(A.values())

# ========Methods=========
def get_id(num):
    return A[num]

def get_num(id):
    return key_list[val_list.index(id)]



# test it yourself
if __name__ == '__main__':
    print(get_num(7892874))
    print(get_id(240))