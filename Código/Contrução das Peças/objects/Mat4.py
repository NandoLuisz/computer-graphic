import math

class Mat4:
    def __init__(self, rows):
        self.rows = rows
    
    @staticmethod
    def identity(size):
        return Mat4([[1 if i == j else 0 for j in range(size)] for i in range(size)])
    
    def __mul__(self, other):
        if isinstance(other, Mat4):
            result = [[0 for _ in range(len(other.rows[0]))] for _ in range(len(self.rows))]
            for i in range(len(self.rows)):
                for j in range(len(other.rows[0])):
                    for k in range(len(other.rows)):
                        result[i][j] += self.rows[i][k] * other.rows[k][j]
            return Mat4(result)
        elif isinstance(other, list) and len(other) == len(self.rows[0]):
            result = [0 for _ in range(len(self.rows))]
            for i in range(len(self.rows)):
                for j in range(len(other)):
                    result[i] += self.rows[i][j] * other[j]
            return result
        else:
            raise ValueError("Multiplicação inválida")
    
    @staticmethod
    def translation(tx, ty, tz):
        return Mat4([[1, 0, 0, tx],
                      [0, 1, 0, ty],
                      [0, 0, 1, tz],
                      [0, 0, 0, 1]])
    
    @staticmethod
    def scaling(sx, sy, sz):
        return Mat4([[sx, 0, 0, 0],
                       [0, sy, 0, 0],
                       [0, 0, sz, 0],
                       [0, 0, 0, 1]])
    
    @staticmethod
    def rotation_x(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([[1, 0, 0, 0],
                       [0, c, -s, 0],
                       [0, s, c, 0],
                       [0, 0, 0, 1]])
    
    @staticmethod
    def rotation_y(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([[c, 0, s, 0],
                       [0, 1, 0, 0],
                       [-s, 0, c, 0],
                       [0, 0, 0, 1]])
    
    @staticmethod
    def rotation_z(angle):
        c = math.cos(angle)
        s = math.sin(angle)
        return Mat4([[c, -s, 0, 0],
                       [s, c, 0, 0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
    
    def transpose(self):
        return Mat4([[self.rows[j][i] for j in range(len(self.rows))] for i in range(len(self.rows[0]))])
    
    def __repr__(self):
        return f"Mat4({self.rows})"
    
    @property
    def shape(self):
        return (len(self.rows), len(self.rows[0]))
    
    