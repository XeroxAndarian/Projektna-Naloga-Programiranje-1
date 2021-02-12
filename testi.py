def number_from_string(string):
    seznam = list(string.split(" "))
    seznam2 = []
    seznam3 = []
    seznam4 = []
    for i in seznam:
        if i.find("1") == 0 or i.find("2") == 0:
            seznam3.append(i)
        else:
            seznam2.append(i)
    for j in seznam3:
        if len(j) == 4:
            seznam4.append(j)
    return int(seznam4[0])

def number_from_(string):
    seznam = list(string.split(" "))
    seznam2 = []
    seznam3 = []
    seznam4 = []
    for i in seznam:
        if i.find("1") == 0 or i.find("2") == 0:
            seznam3.append(i)
        else:
            seznam2.append(i)
    for j in seznam3:
        if len(j) == 4:
            seznam4.append(j)
    return int(seznam4[0])

print(number_from_string("Jan, 2021 to ?"))
print(number_from_string("Jan, 2021 to Dec, 2022"))
print(number_from_string("Jul 8, 2004 to Aug 7, 2004"))
print(number_from_string("2004"))

