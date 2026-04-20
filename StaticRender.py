import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# -----------------------------
# Geometry parameters
# -----------------------------
a = 0.01          # lattice spacing (m)
nx = 40           # reduced for plotting clarity
ny = 30

eps = 10
r = 0.25 * a

# physical extent
sx = nx * a
sy = ny * a

# -----------------------------
# Waveguide definition
# -----------------------------
def is_waveguide(i, j):
    # L-shaped defect
    if j == -5 and i < 10:
        return True
    if i == 10 and -5 <= j <= 10:
        return True
    if j == 10 and i >= 10:
        return True
    return False

# -----------------------------
# Create figure
# -----------------------------
fig, ax = plt.subplots(figsize=(8, 6))

# -----------------------------
# Draw dielectric rods
# -----------------------------
for i in range(-nx//2, nx//2):
    for j in range(-ny//2, ny//2):

        if is_waveguide(i, j):
            continue  # remove rods → waveguide

        x = i * a
        y = j * a

        circle = patches.Circle(
            (x, y),
            radius=r,
            facecolor="black",
            edgecolor="none",
            alpha=0.25
        )
        ax.add_patch(circle)

# -----------------------------
# Highlight waveguide path
# -----------------------------
wg_x = []
wg_y = []

for i in range(-nx//2, nx//2):
    for j in range(-ny//2, ny//2):
        if is_waveguide(i, j):
            wg_x.append(i * a)
            wg_y.append(j * a)

ax.scatter(
    wg_x,
    wg_y,
    c="red",
    s=10,
    label="Waveguide defect"
)

# -----------------------------
# Formatting
# -----------------------------
ax.set_title("Photonic Crystal Waveguide Structure (2D)")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

ax.set_aspect("equal")
ax.grid(True, alpha=0.2)

plt.legend()

# -----------------------------
# Save output
# -----------------------------
plt.savefig("photonic_crystal_structure.png", dpi=300, bbox_inches="tight")

plt.show()
