import matplotlib.pyplot as plt
import numpy as np

coords = []


def get_start_cords():
    global coords
    path = "points.txt"
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            try:
                coords.append([float(i) for i in line.split("\t")])
            except:
                pass


get_start_cords()
x_cords = [i[0] for i in coords]
y_cords = [i[1] for i in coords]

plt.scatter(x_cords, y_cords)
polyline = np.linspace(0.3, 9.6, 30)


def adjR(x, y, degree):
    results = {}
    coeffs = np.polyfit(x, y, degree)
    p = np.poly1d(coeffs)
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    results = 1 - (((1 - (ssreg / sstot)) * (len(y) - 1)) / (len(y) - degree - 1))
    return results


dgr = 1
while (result := adjR(x=x_cords, y=y_cords, degree=dgr)) < 0.94:
    dgr += 1
print()
print(result, dgr)
plt.plot(polyline, np.poly1d(np.polyfit(x_cords, y_cords, dgr))(polyline), color="red")
print(np.poly1d(np.polyfit(x_cords, y_cords, dgr)))
plt.show()
