from myvectors.vectors import Segment3D, Vector3D


def test_intersections():
    def vec(x, y, z): return Vector3D(x, y, z)

    tests = [
        {
            "name": "Пересечение в центре",
            "s1": Segment3D(vec(0, 0, 0), vec(1, 1, 1)),
            "s2": Segment3D(vec(1, 0, 0), vec(0, 1, 1)),
            "expected": True,
        },
        {
            "name": "Разные плоскости",
            "s1": Segment3D(vec(0, 0, 0), vec(1, 0, 0)),
            "s2": Segment3D(vec(0, 1, 1), vec(1, 1, 1)),
            "expected": False,
        },
        {
            "name": "Параллельные, но не совпадают",
            "s1": Segment3D(vec(0, 0, 0), vec(1, 0, 0)),
            "s2": Segment3D(vec(0, 1, 0), vec(1, 1, 0)),
            "expected": False,
        },
        {
            "name": "Пересекаются на границе",
            "s1": Segment3D(vec(0, 0, 0), vec(1, 0, 0)),
            "s2": Segment3D(vec(1, 0, 0), vec(1, 1, 0)),
            "expected": True,
        },
        {
            "name": "Совпадают по направлению, но не пересекаются",
            "s1": Segment3D(vec(0, 0, 0), vec(1, 0, 0)),
            "s2": Segment3D(vec(2, 0, 0), vec(3, 0, 0)),
            "expected": False,
        },
        {
            "name": "Частичное совпадение отрезков",
            "s1": Segment3D(vec(0, 0, 0), vec(2, 0, 0)),
            "s2": Segment3D(vec(1, 0, 0), vec(3, 0, 0)),
            "expected": True,  # В твоей реализации вернёт одну точку
        },
    ]

    for test in tests:
        result = test["s1"].intersect(test["s2"])
        ok = (result is not None) == test["expected"]
        print(f"{'OK' if ok else 'ERR'} {test['name']}: result = {result}")

test_intersections()
