import os.path
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import csv

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)

maintable = Table.read(
    "COSMOS_PSdetection_filter2.fits", format="fits"
)  # Reads in the table directly from the .fits file

# maintable.write("COSMOS_PSdetection_filter2.csv", format="ascii.csv", overwrite=True)

# maintable numpy conversion
maintable_structured = np.lib.recfunctions.structured_to_unstructured(
    maintable.as_array()
)

# retrive object ids with more than 5/10 datapoints
obj_IDS = np.array(maintable["objID"])
unique_ids, counts = np.unique(obj_IDS, return_counts=True)
more_than_5_datapoints = unique_ids[np.where(counts >= 5)]
more_than_10_datapoints = unique_ids[np.where(counts >= 10)]

# magnitude evaulation factors
m_r = 1
F_r = 1


def plot_data():
    mag_rms = []
    avg_mags = []
    n = len(more_than_10_datapoints)
    for unique_id in more_than_10_datapoints:
        n -= 1
        data = maintable_structured[np.where(maintable_structured[:, 0] == unique_id)]
        # avg mags
        magnitudes = []
        flux_values = data[:, 11]
        magnitudes = -2.5 * np.log10(flux_values / F_r) + m_r
        average_mag = np.mean(magnitudes)
        avg_mags.append(average_mag)
        # rms
        diffs = (magnitudes - average_mag) ** 2
        rms = (np.mean(np.array(diffs))) ** 0.5
        mag_rms.append(rms)
        print(n, "datapoints to go")
    return mag_rms, avg_mags


def plot_data_from_file():
    data_file = np.genfromtxt("plotting_data.csv", delimiter=",", names=True)
    avg_mags = data_file["avg_mags"]
    mag_rms = data_file["mag_rms"]
    return mag_rms, avg_mags


plot_data()
# plot_data_from_file()

plt.figure()
plt.scatter(np.array(avg_mags), np.array(mag_rms), marker=".", color="black", s=1)
plt.xlim(0, 16)
plt.ylim(bottom=0)
plt.xlabel("Average magnitude (mag)")
plt.ylabel("r.m.s deviation (mag)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

data = zip(avg_mags, mag_rms)
header = ["avg_mags", "mag_rms"]
with open("plotting_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(data)

plt.show()
