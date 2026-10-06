import random
from pathlib import Path


class Point:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, minX, maxX, minY, maxY):
        if minX >= maxX or minY >= maxY:
            raise ValueError("Тэгш өнцөгт эерэг өргөн, өндөртэй байх ёстой")

        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

    def contains(self, point):
        # Хил дээрх цэгийг багтсан гэж үзнэ.
        return (
            self.minX <= point.x <= self.maxX
            and self.minY <= point.y <= self.maxY
        )


def generateRectangle(rng):
    while True:
        minX, maxX = sorted([rng.random(), rng.random()])
        minY, maxY = sorted([rng.random(), rng.random()])

        if minX < maxX and minY < maxY:
            return Rectangle(minX, maxX, minY, maxY)


def main():
    # Давтан ажиллуулахад ижил үр дүн гаргаж шалгахад зориулсан seed.
    rng = random.Random(42)

    points = []
    for i in range(4):
        points.append(Point(rng.random(), rng.random()))

    rectangles = []
    for i in range(4):
        rectangles.append(generateRectangle(rng))

    output_dir = Path(__file__).resolve().parent / "results"
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / "point_rectangle_results.txt"

    with output_file.open("w", encoding="utf-8") as file:
        for i, point in enumerate(points, start=1):
            file.write(f"P{i}: ({point.x:.6f}, {point.y:.6f})\n")

        for j, rectangle in enumerate(rectangles, start=1):
            file.write(
                f"R{j}: "
                f"x=[{rectangle.minX:.6f}, {rectangle.maxX:.6f}], "
                f"y=[{rectangle.minY:.6f}, {rectangle.maxY:.6f}]\n"
            )

        file.write("\nШалгалтын үр дүн:\n")

        for i, point in enumerate(points, start=1):
            for j, rectangle in enumerate(rectangles, start=1):
                inside = rectangle.contains(point)
                result = f"P{i} in R{j}: {inside}"
                print(result)
                file.write(result + "\n")

    print("Хадгалсан файл:", output_file)


if __name__ == "__main__":
    main()