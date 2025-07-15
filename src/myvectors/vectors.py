from typing import Optional, Tuple
import math

EPSILON = 1e-6

class Vector3D:
    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar: float):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def __rmul__(self, scalar: float):
        return self.__mul__(scalar)

    def dot(self, other) -> float:
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def length(self) -> float:
        return math.sqrt(self.dot(self))

    def is_close(self, other, eps=EPSILON) -> bool:
        return (math.isclose(self.x, other.x, abs_tol=eps) and
                math.isclose(self.y, other.y, abs_tol=eps) and
                math.isclose(self.z, other.z, abs_tol=eps))


    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"


def project(p: Vector3D, origin: Vector3D, direction: Vector3D) -> float:
    # Проецируем точку на вектор направления
    return (p - origin).dot(direction) / direction.dot(direction)

class Segment3D:
    def __init__(self, start: Vector3D, end: Vector3D):
        self.start = start
        self.end = end

    def direction(self) -> Vector3D:
        return self.end - self.start

    def intersect(self, other: 'Segment3D') -> Optional[Vector3D]:
        p1, p2 = self.start, self.end
        q1, q2 = other.start, other.end

        u = p2 - p1
        v = q2 - q1
        w = p1 - q1

        # Проверка, лежат ли отрезки в одной плоскости
        triple_product = u.cross(v).dot(w)
        if abs(triple_product) > EPSILON:
            print("same place")
            return None # точно не пересекаются

        a = u.dot(u)
        b = u.dot(v)
        c = v.dot(v)
        d = u.dot(w)
        e = v.dot(w)

        D = a * c - b * b
        if abs(D) < EPSILON:
            if w.cross(u).length() > EPSILON:
                return None  # Не коллинеарны

            proj_p1: float = project(p1, p1, u)  # 0
            proj_p2: float = project(p2, p1, u)  # 1
            proj_q1: float = project(q1, p1, u)
            proj_q2: float = project(q2, p1, u)

            # Диапазоны проекций как числовые отрезки
            range_a: Tuple[float, float] = (min(proj_p1, proj_p2), max(proj_p1, proj_p2))
            range_b: Tuple[float, float] = (min(proj_q1, proj_q2), max(proj_q1, proj_q2))

            # Поиск пересечения интервалов
            overlap_start: float = max(range_a[0], range_b[0])
            overlap_end: float = min(range_a[1], range_b[1])

            if overlap_start > overlap_end + EPSILON:
                return None

            # Вычисляем точку пересечения
            t: float = (overlap_start + overlap_end) / 2
            return p1 + u * t


        # Решение системы уравнений на нахождение точки пересечения (поиск параметра)
        sc = (b * e - c * d) / D
        tc = (a * e - b * d) / D

        point_on_self = p1 + sc * u
        point_on_other = q1 + tc * v

        if not point_on_self.is_close(point_on_other):
            return None

        if not (0 - EPSILON <= sc <= 1 + EPSILON):
            return None
        if not (0 - EPSILON <= tc <= 1 + EPSILON):
            return None

        return point_on_self
