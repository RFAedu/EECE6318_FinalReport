import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Parameters (match your MPB code)
# -----------------------------
a = 1.0          # normalized lattice constant (for plotting)
r = 0.25         # rod radius (same as MPB)
N = 10           # number of unit cells in each direction

# -----------------------------
# Create square lattice points
# -----------------------------
x_vals = np.arange(-N, N + 1) * a
y_vals = np.arange(-N, N + 1) * a

# -----------------------------
# Plot setup
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 6))

# Draw rods
for x in x_vals:
    for y in y_vals:
        circle = plt.Circle(
            (x, y),
            r,
            color='blue',
            alpha=0.5
        )
        ax.add_patch(circle)

# -----------------------------
# Formatting
# -----------------------------
ax.set_aspect('equal')
ax.set_xlim(-N * a - 1, N * a + 1)
ax.set_ylim(-N * a - 1, N * a + 1)

ax.set_xlabel("x (normalized units)")
ax.set_ylabel("y (normalized units)")
ax.set_title("2D Square Lattice Photonic Crystal (Dielectric Rods)")

ax.grid(True, linestyle='--', alpha=0.3)

plt.show()
