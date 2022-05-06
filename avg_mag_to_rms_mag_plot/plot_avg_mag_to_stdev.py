from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import csv

plt.rc("text", usetex=True)
plt.rc("font", family="serif", size=12)


def plot_data():
    maintable = Table.read(
        "../COSMOS_PSdetection_filter2.fits", format="fits"
    )  # Reads in the table directly from the .fits file

    maintable.write("COSMOS_PSdetection_filter2.csv", format="ascii.csv", overwrite=True)

    # maintable numpy conversion
    maintable_structured = np.lib.recfunctions.structured_to_unstructured(
        maintable.as_array()
    )

    # retrive object ids with more than a define number datapoints
    obj_IDS = np.array(maintable["objID"])
    unique_ids, counts = np.unique(obj_IDS, return_counts=True)
    min_data_points = 10
    datapoint_data = unique_ids[np.where(counts >= min_data_points)]

    mag_rms = []
    avg_mags = []
    n = len(datapoint_data)
    for unique_id in datapoint_data:
        n -= 1
        data = maintable_structured[np.where(maintable_structured[:, 0] == unique_id)]
        # avg mags
        magnitudes = []
        flux_values = data[:, 11]
        magnitudes = -2.5 * np.log10(flux_values / 3631)
        average_mag = np.mean(magnitudes)
        avg_mags.append(average_mag)
        # rms
        diffs = (magnitudes - average_mag) ** 2
        rms = (np.mean(np.array(diffs))) ** 0.5
        mag_rms.append(rms)
        print(n, "datapoints to go")

    # export data
    data = zip(avg_mags, mag_rms)
    header = ["avg_mags", "mag_rms"]
    with open("plotting_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

    return mag_rms, avg_mags



def plot_data_from_file():
    data_file = np.genfromtxt("plotting_data.csv", delimiter=",", names=True)
    avg_mags = data_file["avg_mags"]
    mag_rms = data_file["mag_rms"]
    return mag_rms, avg_mags
  
# mag_rms, avg_mags = plot_data()
mag_rms, avg_mags = plot_data_from_file()

plt.figure()
plt.scatter(np.array(avg_mags), np.array(mag_rms), marker=".", color="black", s=1)
plt.xlim(0, 16)
plt.ylim(bottom=0)
plt.xlabel("Average magnitude (mag)")
plt.ylabel("r.m.s deviation (mag)")
ax = plt.gca()
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax = plt.subplots()
ax.plot(avg_mags, mag_rms, 'o-', label='line plot')
mag_rms_avg = [np.mean(avg_mags)] * len(avg_mags)
ax.plot(avg_mags, mag_rms_avg, color='black', lw=6, ls='--', label="average plot")

plt.show()
