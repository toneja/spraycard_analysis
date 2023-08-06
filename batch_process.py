#!/usr/bin/env python3
#
# This file is part of the spraycard analysis scripts.
#
# Copyright (c) 2023 Jason Toney
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

"""docstring goes here"""

import os
import subprocess
import sys
import time

import analyze_spraycards


def batch_process(image_folder):
    """docstring goes here"""
    # Start the timer
    start_time = time.time()
    # Count how many images are processed
    processed = 0
    # Iterate through the images
    for image_name in os.listdir(image_folder):
        # Full path to the current image
        current_image = os.path.join(image_folder, image_name)

        # Check if the current item is a file
        if os.path.isfile(current_image):
            # Check if the image has already been processed
            if os.path.exists(f"spraycards/images/{os.path.basename(current_image)}"):
                if os.path.exists(
                    f"spraycards/results/Results_{os.path.splitext(os.path.basename(current_image))[0]}.csv"
                ):
                    print(f"Skipping image: {current_image}, already processed.")
                    continue
            print(f"Processing image: {current_image}")
            print(f"DEBUG - {os.path.basename(current_image)}")
            processed += 1
            print(f"{current_image}")
            # Execute the ImageJ macro for the current folder
            command = [
                "./ImageJ.exe",
                "-macro",
                "spraycards/AnalyzeSprayCard.ijm",
                current_image,
            ]

            try:
                subprocess.run(command, capture_output=True, text=True, check=True)
            except subprocess.CalledProcessError as exception:
                print(f"Error executing the macro: {exception}")

    # Process the ImageJ results
    os.chdir(os.path.dirname(sys.argv[0]))
    for file in os.listdir("ImageJ/spraycards/results"):
        if file.endswith(".csv"):
            analyze_spraycards.summarize_droplet_sizes(f"ImageJ/spraycards/results/{file}")

    # Calculate the elapsed time
    elapsed_time = time.time() - start_time
    # Print elapsed time in H:M:S format
    print(
        f"\nElapsed time: {time.strftime('%H:%M:%S', time.gmtime(elapsed_time))}"
    )
    print(f"Images processed: {processed}")
    input("Batch processing complete. Press ENTER.\n")


if __name__ == "__main__":
    os.chdir(f"{os.path.dirname(sys.argv[0])}/ImageJ")
    if len(sys.argv) > 1:
        IMAGE_FOLDER = sys.argv[1]
    else:
        IMAGE_FOLDER = "../Spraycard Images"
    batch_process(IMAGE_FOLDER)
