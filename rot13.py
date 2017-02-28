def rot_13(string):
    output_string = ""
    for c in string:
        ord_of_c = ord(c)
        rot_13_ord_of_c = ord_of_c
        if ord('A') <= ord_of_c <= ord('Z'):
            if ord_of_c <= ord('Z')-13:
                rot_13_ord_of_c = ord_of_c+13
            else:
                rot_13_ord_of_c = ord_of_c-13
        if ord('a') <= ord_of_c <= ord('z'):
            if ord_of_c <= ord('z')-13:
                rot_13_ord_of_c = ord_of_c+13
            else:
                rot_13_ord_of_c = ord_of_c-13
        output_string += chr(rot_13_ord_of_c)
    return output_string
