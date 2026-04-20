import meep as mp
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Scaling
# -----------------------------
a = 0.01
c = 3e8

fmin = 1e9
fmax = 20e9

# convert to normalized units
fmin_n = fmin * a / c
fmax_n = fmax * a / c

fcen = 0.5 * (fmin_n + fmax_n)
df = fmax_n - fmin_n

print("Simulating broadband excitation for S21 extraction")

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

# waveguide definition
def is_waveguide(i, j):
    if j == -10 and i < 20:
        return True
    if i == 20 and -10 <= j <= 20:
        return True
    if j == 20 and i >= 20:
        return True
    return False

for i in range(-nx//2, nx//2):
    for j in range(-ny//2, ny//2):

        pos = mp.Vector3(i*a, j*a)

        # air regions left/right
        if i < -40 or i > 40:
            continue

        # defect waveguide
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

# -----------------------------
# Broadband pulse source
# -----------------------------
sources = [
    mp.Source(
        mp.GaussianSource(frequency=fcen, fwidth=df),
        component=mp.Ez,
        center=mp.Vector3(-sx/2 + 2*a, 0),
        size=mp.Vector3(0, sy)
    )
]

# -----------------------------
# Simulation
# -----------------------------
pml_layers = [mp.PML(1.0*a)]

sim = mp.Simulation(
    cell_size=cell,
    geometry=geometry,
    sources=sources,
    boundary_layers=pml_layers,
    resolution=20
)

# -----------------------------
# Flux regions (S21 measurement)
# -----------------------------
refl_fr = mp.FluxRegion(center=mp.Vector3(-sx/4, 0), size=mp.Vector3(0, sy))
tran_fr = mp.FluxRegion(center=mp.Vector3(sx/4, 0), size=mp.Vector3(0, sy))

refl = sim.add_flux(fcen, df, 500, refl_fr)
tran = sim.add_flux(fcen, df, 500, tran_fr)

# -----------------------------
# Run simulation
# -----------------------------
sim.run(until=300)

# -----------------------------
# Extract frequency spectrum
# -----------------------------
freqs = np.array(mp.get_flux_freqs(refl))

refl_data = np.array(mp.get_fluxes(refl))
tran_data = np.array(mp.get_fluxes(tran))

# -----------------------------
# Normalize S21
# -----------------------------
# (Transmission coefficient)
S21 = tran_data / np.max(tran_data)

# -----------------------------
# Convert normalized freq → Hz
# -----------------------------
freqs_hz = freqs * c / a

# -----------------------------
# Plot S21 (Transmission)
# -----------------------------
plt.figure(figsize=(8,5))
plt.plot(freqs_hz/1e9, S21, label="S21 Transmission")

plt.xlabel("Frequency (GHz)")
plt.ylabel("Transmission (S21)")
plt.title("Photonic Crystal Waveguide Transmission (S21)")
plt.grid(True)
plt.legend()
plt.show()
