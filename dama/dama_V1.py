import numpy as np
import matplotlib.pyplot as plt

# =====================================
# PARÂMETROS
# =====================================

raio = 5
altura = 2

# ângulo
theta = np.linspace(0, 2*np.pi, 100)

# altura
y = np.linspace(0, altura, 100)

# malha lateral
THETA, Y = np.meshgrid(theta, y)

# =====================================
# SUPERFÍCIE LATERAL
# =====================================

X = raio * np.cos(THETA)
Z = raio * np.sin(THETA)

# =====================================
# FIGURA
# =====================================

fig = plt.figure(figsize=(15,15))
ax = fig.add_subplot(111, projection='3d')

# lateral
ax.plot_surface(X, Y, Z, color='black')

# =====================================
# TAMPA SUPERIOR E INFERIOR
# =====================================

r = np.linspace(0, raio, 100)

R, THETA2 = np.meshgrid(r, theta)

X2 = R * np.cos(THETA2)
Z2 = R * np.sin(THETA2)

# tampa inferior (y = 0)
Y_bottom = np.zeros_like(X2)

# tampa superior (y = altura)
Y_top = np.ones_like(X2) * altura

ax.plot_surface(X2, Y_bottom, Z2, color='black')
ax.plot_surface(X2, Y_top, Z2, color='black')

# =====================================
# AJUSTES
# =====================================

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")

ax.set_title("Dama")

# proporção correta
ax.set_box_aspect([10, 2, 10])

# salva imagem
plt.savefig("Dama.png")

# mostra
plt.show()