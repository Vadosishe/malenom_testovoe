import matplotlib.pyplot as plt

sensors = {}
carriages = {}


def get_carriage(path="typeRailwayCarriage.txt"):
    global carriages
    with open(path, "r", encoding="utf-8") as file:
        i = 1
        for line in file:
            common = line.strip().split()
            pairs_count = len(common) + 1
            center_distance = float(common[(len(common) - 1) // 2])
            delta = center_distance / float(common[0])

            carriages[i] = {"pairs_count": pairs_count, "center_distance": center_distance,
                            "other_distance": float(common[0]), "delta": delta}
            i += 1


def get_sensors(path="sensorResponse.txt"):
    global sensors
    with open(path, "r", encoding="utf-8") as file:
        i = 1
        for line in file:
            sensors[i] = {"time": float(line.strip().split(" ")[0]), "sensor_id": int(line.strip().split(" ")[1])}
            # (float(line.strip().split(" ")[0]), int(line.strip().split(" ")[1]))
            i += 1


get_carriage()
get_sensors()
print(carriages)
print(sensors)
fr_4_to_1 = True if sensors[1]["sensor_id"] == 4 else False
print(fr_4_to_1)
sensors_1 = [value["time"] for key, value in sensors.items() if value["sensor_id"] == 1]
sensors_2 = [value["time"] for key, value in sensors.items() if value["sensor_id"] == 2]
sensors_3 = [value["time"] for key, value in sensors.items() if value["sensor_id"] == 3]
sensors_4 = [value["time"] for key, value in sensors.items() if value["sensor_id"] == 4]

sensors_1_delta = [sensors_1[i + 1] - sensors_1[i] for i in range(len(sensors_1) - 1)]
sensors_2_delta = [sensors_2[i + 1] - sensors_2[i] for i in range(len(sensors_2) - 1)]
sensors_3_delta = [sensors_3[i + 1] - sensors_3[i] for i in range(len(sensors_3) - 1)]
sensors_4_delta = [sensors_4[i + 1] - sensors_4[i] for i in range(len(sensors_4) - 1)]
sensors_delta_total = [(sensors_1_delta[i] + sensors_2_delta[i] + sensors_3_delta[i] + sensors_4_delta[i]) / 4 for i in
                       range(len(sensors_1_delta))]

print(sensors_delta_total)

neighbor_ratio = [sensors_delta_total[i + 1] / sensors_delta_total[i] for i in
                  range(len(sensors_delta_total) - 1)]
print(neighbor_ratio)
# for i in range(len(sensors)):
plt.scatter(sensors_1, [1.1] * len(sensors_1), color="red")
plt.scatter(sensors_2, [1.2] * len(sensors_2), color="green")
plt.scatter(sensors_3, [1.3] * len(sensors_3), color="blue")
plt.scatter(sensors_4, [1.4] * len(sensors_4), color="orange")
plt.ylim(1, 2)
plt.show()

wheel_ratio = {}
for key, value in carriages.items():
    wheel_ratio[key] = [1] * (value["pairs_count"] // 2 - 2) \
                       + [value["center_distance"] / value["other_distance"],
                          value["other_distance"] / value["center_distance"]] \
                       + [1] * (value["pairs_count"] // 2 - 2)
print(wheel_ratio)


def confidence_degree_calc(time_ratio, train_ratio, pointer, wieght):
    if pointer + len(train_ratio) > len(time_ratio):
        return 0
    confidence_degree = 1
    for i in range(len(train_ratio)):
        try:
            confidence_degree *= a if (a := 1 - wieght * abs(train_ratio[i] - time_ratio[i + pointer]) / train_ratio[
                i]) > 0 else 0
        except:
            return 0
    return confidence_degree


pointer = 0
pointer_shift = 0
trains = []
while True:
    max_confidence = 0
    train_true_index = 0
    for train_index, train_ratios in wheel_ratio.items():
        confidence_degree = confidence_degree_calc(neighbor_ratio, train_ratios, pointer, wieght=10)
        if confidence_degree > max_confidence:
            train_true_index = train_index
            max_confidence = confidence_degree
            pointer_shift = len(train_ratios) + 2
    trains.append(train_true_index)
    pointer += pointer_shift
    if pointer > len(neighbor_ratio):
        break

print(trains)
print(len(trains))

"""
1 - [3, 8, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 7, 7, 7, 8, 7, 7, 7, 8, 7, 8, 7, 8]
2 - [3, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 8, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 8, 7, 7]
3 - [3, 7, 7, 8, 7, 8, 7, 7, 7, 8, 7, 7, 7, 7, 8, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 7]
4 - [3, 8, 7, 7, 8, 7, 8, 7, 7, 8, 7, 7, 8, 7, 8, 7, 7, 8, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 7]

s - [3, 8, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7, 7, 8, 7, 7]
"""