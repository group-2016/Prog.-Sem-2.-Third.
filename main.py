"""
Логунов Алексей.
Группа Р3175.
2017 год.
"""

from math import sqrt

"""
Класс вектора на плоскости.
Включает в себя стадартный инструментарий работы с векторами
(вычисление нормали, нормализация, скалярное произведение)
"""
class Vector2:
    x = y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def normalize(self):
        len = math.sqrt(self.x ** 2 + self.y ** 2)
        return Vector2(self.x / len, self.y / len)

    def normal(self):
        return Vector2(self.y, -self.x)

    def __add__(self, vector):
        return Vector2(self.x + vector.x, self.y + vector.y)

    def __str__(self):
        return str(self.x) + ":" + str(self.y)

    @staticmethod
    def extract(vector1, vector2):
        return Vector2(vector2.x - vector1.x, vector2.y - vector1.y)

    @staticmethod
    def dot(vector1, vector2):
        dot = vector1.x * vector2.x + vector1.y * vector2.y
        return dot

"""
Класс полигона.
Включает список вершин и нормалей к сторонам.
"""
class Poly:
    position = Vector2(0, 0)
    vertices = []
    normals = []

    def __init__(self, position, vertices):
        self.position = position
        self.vertices = [vertex + position for vertex in vertices]
        self.normals = vertices[:]
        for i in range(len(self.vertices)):
            next = (i + 1) % len(self.vertices)
            self.normals.append(Vector2.extract(vertices[i], vertices[next]).normal().normalize())

    # Метод процеирования полигона на ось
    # Возвращает пару значений - крайние значения отрезка - проекции полигона на ось
    def polyProj(poly, axis):
        max = min = Vector2.dot(poly.vertices[0], axis)
        for vertex in poly.vertices:
            proj = Vector2.dot(vertex, axis)
            if proj > max:
                max = proj
            if proj < min:
                min = proj
        return (min, max)

# Ядро программы - проверка на взаимопроникновение
def isCollide(poly1, poly2):
    for normal in poly1.normals:
        axis = normal.normalize()
        proj1 = poly1.polyProj(axis)
        proj2 = poly2.polyProj(axis)
        if proj1[0] > proj2[1] or proj1[1] < proj2[0]:
            return False

    for normal in poly2.normals:
        axis = normal.normalize()
        proj1 = poly1.polyProj(axis)
        proj2 = poly2.polyProj(axis)
        if proj1[0] > proj2[1] or proj1[1] < proj2[0]:
            return False

    return True


# Задание вершин многоугольника в локальных координатах (по часовой стрелке)
vertices1 = \
    [
        Vector2(10, 10),
        Vector2(10, -10),
        Vector2(-10, -10),
        Vector2(-10, 10)
    ]

vertices2 = \
    [
        Vector2(0, 10),
        Vector2(10, 0),
        Vector2(0, -10),
        Vector2(-10, 0)
    ]

poly1 = Poly(Vector2(0, 10), vertices1)
poly2 = Poly(Vector2(0, 0), vertices2)

print(isCollide(poly1, poly2))
