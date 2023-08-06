#!/usr/bin/env python3

import sys
import csv
import matplotlib.pyplot as plt


def summarize_droplet_sizes(csv_file_path):
    # Initialize a dictionary to store the summary
    summary = {}

    # Define the bin size for summarizing in increments of 10 microns
    bin_size = 10

    # Count good and bad ROIs
    good_rois, bad_rois = 0, 0

    # Read the CSV file
    with open(csv_file_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)

        # Process each row in the CSV
        for row in reader:
            # Filter bad ROIs
            # aspect_ratio = float(row["AR"])
            # if aspect_ratio >= 2:
            #     bad_rois += 1
            #     continue
            good_rois += 1

            # Get the Feret diameter value from the current row
            feret_diameter = float(row["Feret"])

            # Calculate the bin for the current value
            bin_number = int(feret_diameter // bin_size)

            # Update the count for the corresponding bin
            summary[bin_number] = summary.get(bin_number, 0) + 1

    # Sort the summary dictionary by bin number
    sorted_summary = dict(sorted(summary.items()))

    # Write the summary to a new CSV file
    output_csv_file = "droplet_summary.csv"
    with open(output_csv_file, "w", newline="") as csvfile:
        fieldnames = ["Bin (microns)", "Count"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for bin_number, count in sorted_summary.items():
            bin_start = bin_number * bin_size
            bin_end = (bin_number + 1) * bin_size
            writer.writerow({"Bin (microns)": f"{bin_start}-{bin_end}", "Count": count})

    print("Droplet size summary has been written to droplet_summary.csv")
    print(f"Recorded {good_rois} good ROIs")
    print(
        f"Skipped {bad_rois} ROIs : {round(bad_rois / (good_rois + bad_rois) * 100, 2)}%"
    )

    # Extract the data for plotting
    bins = [bin_num * bin_size for bin_num in sorted_summary.keys()]
    counts = list(sorted_summary.values())

    # Create the bar graph
    plt.bar(bins, counts, width=bin_size, align="edge", edgecolor="black")
    plt.xlabel("Droplet Feret Diameter (microns)")
    plt.ylabel("Count")
    plt.title(f"Droplet Size Summary {csv_file_path}")
    plt.grid(axis="y")
    plt.show()


if __name__ == "__main__":
    # Check if the user provided the CSV file path in the command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python3 analyze_spraycards.py <csv_file_path>")
        sys.exit(1)

    # Get the CSV file path from command-line arguments
    csv_file_path = sys.argv[1]
    summarize_droplet_sizes(csv_file_path)
