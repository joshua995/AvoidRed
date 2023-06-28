def read_data():
    file = open("SaveData.txt", "r")
    data = file.readline().split(" ")
    file.close()
    return int(data[0]), int(data[1])


def write_data(time, score):
    file = open("SaveData.txt", "w")
    file.write(str(time) + " " + str(score))
    file.close()
