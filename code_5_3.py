import math
from pathlib import Path


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Polyline:
    def __init__(self, points=None):
        self.points = list(points) if points is not None else []

    def getLength(self):
        length = 0.0

        for i in range(len(self.points) - 1):
            first = self.points[i]
            second = self.points[i + 1]

            length += math.sqrt(
                (second.x - first.x) ** 2
                + (second.y - first.y) ** 2
            )

        return length


def readPolylineFile(fileName):
    polylines = []
    current_points = None

    with open(fileName, "r", encoding="utf-8") as file:
        header = file.readline().strip()
        if header.lower() != "polyline;":
            raise ValueError("Эхний мөр 'Polyline;' байх ёстой")

        for line_number, line in enumerate(file, start=2):
            line = line.strip()
            if not line:
                continue

            if ":" in line:
                if current_points is not None:
                    polylines.append(Polyline(current_points))

                _, line = line.split(":", 1)
                current_points = []

            if current_points is None:
                raise ValueError(
                    f"{line_number}-р мөр: шугамын ID байхгүй"
                )

            # Нэг мөрөнд нэг эсвэл олон координат байж болно.
            for coordinate in line.split(";"):
                coordinate = coordinate.strip()
                if not coordinate:
                    continue

                x_text, y_text = coordinate.split(",", 1)
                current_points.append(
                    Point(float(x_text), float(y_text))
                )

    if current_points is not None:
        polylines.append(Polyline(current_points))

    if not polylines:
        raise ValueError("Файлд шугамын өгөгдөл алга")

    firstPolylineNum = len(polylines[0].points)
    return polylines, firstPolylineNum


if __name__ == "__main__":
    input_file = (
        Path(__file__).resolve().parent / "data" / "polylines.txt"
    )

    polylines, firstPolylineNum = readPolylineFile(input_file)
    total_points = sum(len(line.points) for line in polylines)

    print("Нийт шугам:", len(polylines))
    print("Нийт цэгийн бичлэг:", total_points)
    print("Эхний шугамын цэг:", firstPolylineNum)

    for number, line in enumerate(polylines, start=1):
        print(
            f"Шугам {number}: "
            f"{len(line.points)} цэг, "
            f"урт = {line.getLength():.6f}"
        )