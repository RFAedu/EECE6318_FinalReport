import meep as mp
import meep.mpb as mpb
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Physical scaling (IMPORTANT)
# -----------------------------
a = 0.01   # 1 cm lattice constant
c = 3e8

# conversion factor: normalized -> Hz
Hz_per_norm = c / a

# -----------------------------
# Lattice definition
# -----------------------------
geometry_lattice = mp.Lattice(
    size=mp.Vector3(1, 1),
    basis1=mp.Vector3(1, 0),
    basis2=mp.Vector3(0, 1)
)

eps = 10
r = 0.25

geometry = [
    mp.Cylinder(
        radius=r,
        height=mp.inf,
        material=mp.Medium(epsilon=eps)
    )
]

# -----------------------------
# k-path (Brillouin zone)
# -----------------------------
num_k = 30
k_points = mp.interpolate(30, [
    mp.Vector3(),              # Γ
    mp.Vector3(0.5, 0),       # X
    mp.Vector3(0.5, 0.5),     # M
    mp.Vector3()              # Γ
])

# -----------------------------
# Solve eigenmodes
# -----------------------------
ms = mpb.ModeSolver(
    geometry_lattice=geometry_lattice,
    geometry=geometry,
    resolution=32,
    k_points=k_points,
    num_bands=8
)

ms.run_tm()

# -----------------------------
# Extract normalized frequencies
# -----------------------------
freqs_norm = np.array(ms.all_freqs)
bands_norm = freqs_norm.reshape(len(k_points), -1)

# -----------------------------
# Convert to real frequency (Hz → GHz)
# -----------------------------
bands_hz = bands_norm * Hz_per_norm
bands_ghz = bands_hz / 1e9

# -----------------------------
# Plot band diagram (NOW IN GHz)
# -----------------------------
plt.figure(figsize=(8,5))

for b in range(bands_ghz.shape[1]):
    plt.plot(bands_ghz[:, b], 'b')

plt.xticks(
    [0, len(k_points)//3, 2*len(k_points)//3, len(k_points)-1],
    ['Γ', 'X', 'M', 'Γ']
)

plt.ylabel("Frequency (GHz)")
plt.title("Photonic Crystal Band Structure")
plt.grid(True)

plt.show()
