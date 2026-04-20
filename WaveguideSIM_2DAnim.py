import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter

# -----------------------------
# Scaling
# -----------------------------
a = 0.01
c = 3e8

f0 = 14.173e9
f0_norm = f0 * a / c

print(f"Simulating single frequency: {f0/1e9:.2f} GHz")

# -----------------------------
# Geometry
# -----------------------------
nx = 120
ny = 80

sx = nx * a
sy = ny * a

cell = mp.Vector3(sx, sy, 0)

eps = 10
r = 0.25 * a

geometry = []
rod_positions = []

# -----------------------------
# Waveguide definition
# -----------------------------
def is_waveguide(i, j):
    if j == -10 and i < 20:
        return True
    if i == 20 and -10 <= j <= 20:
        return True
    if j == 20 and i >= 20:
        return True
    return False

# -----------------------------
# Build photonic crystal
# -----------------------------
for i in range(-nx//2, nx//2):
    for j in range(-ny//2, ny//2):

        pos = mp.Vector3(i*a, j*a)

        # left/right air regions
        if i < -40 or i > 40:
            continue

        # waveguide defect
        if is_waveguide(i, j):
            continue

        geometry.append(
            mp.Cylinder(
                radius=r,
                height=mp.inf,
                center=pos,
                material=mp.Medium(epsilon=eps)
            )
        )

        rod_positions.append((pos.x, pos.y))

# -----------------------------
# Continuous-wave source
# -----------------------------
sources = [
    mp.Source(
        mp.ContinuousSource(frequency=f0_norm),
        component=mp.Ez,
        center=mp.Vector3(-sx/2 + 1*a, 0),
        size=mp.Vector3(0, sy)
    )
]

# -----------------------------
# Simulation setup
# -----------------------------
sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    boundary_layers=[mp.PML(1.0*a)],
    resolution=50
)

# -----------------------------
# Frame storage (|Ez|^2)
# -----------------------------
frames = []

def grab_frame(sim):
    ez = sim.get_array(
        center=mp.Vector3(),
        size=cell,
        component=mp.Ez
    )

    energy = np.abs(ez)**2
    frames.append(energy.copy())

# -----------------------------
# Run simulation
# -----------------------------
sim.run(mp.at_every(5, grab_frame), until=800)

# -----------------------------
# Visualization setup
# -----------------------------
fig, ax = plt.subplots(figsize=(10, 4))

extent = [-sx/2, sx/2, -sy/2, sy/2]

# fixed contrast for energy visualization
vmax = np.percentile(frames[0], 99)

im = ax.imshow(
    frames[0].T,
    cmap='inferno',
    origin='lower',
    extent=extent,
    animated=True,
    vmin=0,
    vmax=vmax,
    alpha=0.95
)

plt.colorbar(im, ax=ax, label=r"Energy density $|E_z|^2$")

# -----------------------------
# Rod overlay
# -----------------------------
x_rods = [p[0] for p in rod_positions]
y_rods = [p[1] for p in rod_positions]

ax.scatter(
    x_rods, y_rods,
    s=8,
    c='white',
    alpha=0.2,
    zorder=10
)

# -----------------------------
# Labels
# -----------------------------
ax.set_title(f"RF Waveguide Energy Propagation at f0 = {f0/1e9:.2f} GHz")
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")

# -----------------------------
# Animation function
# -----------------------------
def update(frame):
    im.set_array(frames[frame].T)
    return [im]

ani = animation.FuncAnimation(
    fig,
    update,
    frames=len(frames),
    interval=100,
    blit=False   # IMPORTANT for saving GIFs
)

# -----------------------------
# SAVE GIF
# -----------------------------
writer = PillowWriter(fps=10)
ani.save("waveguide_energy.gif", writer=writer)

plt.show()
