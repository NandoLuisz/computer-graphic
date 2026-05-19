class Vec3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other): #Adição de vértices
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other): #Subtração de vértices
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar): #Multiplicação por escalar
        return Vec3(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def dot(self, other): #Produto escalar
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other): #Produto vetorial
        return Vec3(self.y * other.z - self.z * other.y,
                      self.z * other.x - self.x * other.z,
                      self.x * other.y - self.y * other.x)
    
    def magnitude(self): #Magnitude do vetor
        return (self.x**2 + self.y**2 + self.z**2)**0.5
    
    def normalize(self): #Normalização do vetor
        mag = self.magnitude()
        if mag < 1e-8:
            return Vec3(0, 0, 0)
        return Vec3(self.x / mag, self.y / mag, self.z / mag)
    
    def __repr__(self):
        return f"Vec3({self.x}, {self.y}, {self.z})"