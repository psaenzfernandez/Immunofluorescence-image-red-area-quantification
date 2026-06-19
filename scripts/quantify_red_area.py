"""
Quantification of red area in images.

This script processes all images in an input folder, identifies red pixels using
an RGB threshold, calculates the percentage of red area in each image, and saves
the results to an Excel file.

Red pixel criterion:
    R > G + red_offset
    R > B + red_offset
    R > min_red_value
"""

from pathlib import Path
import argparse

import cv2
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import Workbook


# Image extensions accepted by the script
EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"}


def calculate_red_area(image_path, red_offset=20, min_red_value=20):
    """
    Calculate the red area of an image.

    Parameters
    ----------
    image_path : pathlib.Path
        Path to the image file.

    red_offset : int
        Minimum difference required between the red channel and the green/blue
        channels.

    min_red_value : int
        Minimum value required for the red channel.

    Returns
    -------
    result : dict
        Dictionary containing the image name, red area, total area and red
        percentage.

    img_rgb : numpy.ndarray
        Image converted from BGR to RGB.

    red_mask : numpy.ndarray
        Boolean mask where True indicates pixels classified as red.
    """

    # Read image using OpenCV
    img = cv2.imread(str(image_path))

    # Check that the image was correctly read
    if img is None:
        raise ValueError(f"Could not read image: {image_path}")

    # Convert from BGR, used by OpenCV, to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Separate RGB channels
    R = img_rgb[:, :, 0].astype(np.int16)
    G = img_rgb[:, :, 1].astype(np.int16)
    B = img_rgb[:, :, 2].astype(np.int16)

    # Define red mask
    red_mask = (
        (R > G + red_offset)
        & (R > B + red_offset)
        & (R > min_red_value)
    )

    # Calculate areas
    red_area = int(np.sum(red_mask))
    total_area = int(red_mask.size)
    red_percentage = round((red_area / total_area) * 100, 2)

    result = {
        "image_name": image_path.name,
        "red_area_pixels": red_area,
        "total_area_pixels": total_area,
        "red_percentage": red_percentage,
    }

    return result, img_rgb, red_mask


def save_results_to_excel(results, output_file):
    """
    Save the analysis results to an Excel file.

    Parameters
    ----------
    results : list of dict
        List containing the results for each processed image.

    output_file : pathlib.Path
        Path where the Excel file will be saved.
    """

    # Create output folder if it does not exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Create new Excel workbook
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"

    # Write headers
    ws.append([
        "image_name",
        "red_area_pixels",
        "total_area_pixels",
        "red_percentage"
    ])

    # Write results
    for result in results:
        ws.append([
            result["image_name"],
            result["red_area_pixels"],
            result["total_area_pixels"],
            result["red_percentage"],
        ])

    # Save Excel file
    wb.save(output_file)


def plot_image_and_mask(img_rgb, red_mask, image_name):
    """
    Display the original image and the red mask.

    Parameters
    ----------
    img_rgb : numpy.ndarray
        Original image in RGB format.

    red_mask : numpy.ndarray
        Boolean mask identifying red pixels.

    image_name : str
        Name of the image file.
    """

    plt.figure(figsize=(20, 10))

    plt.subplot(1, 2, 1)
    plt.imshow(img_rgb)
    plt.title(f"Original image: {image_name}")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(red_mask, cmap="gray")
    plt.title("Red mask")
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def main():
    """
    Main function.
    """

    parser = argparse.ArgumentParser(
        description="Quantify red area percentage in image files."
    )

    parser.add_argument(
        "--input",
        default="data",
        help="Path to the folder containing the input images."
    )

    parser.add_argument(
        "--output",
        default="results/red_area_results.xlsx",
        help="Path to the output Excel file."
    )

    parser.add_argument(
        "--red-offset",
        type=int,
        default=20,
        help="Minimum difference between the red channel and the green/blue channels."
    )

    parser.add_argument(
        "--min-red-value",
        type=int,
        default=20,
        help="Minimum value required for the red channel."
    )

    parser.add_argument(
        "--show",
        action="store_true",
        help="Display the original image and the red mask for each image."
    )

    args = parser.parse_args()

    input_dir = Path(args.input)
    output_file = Path(args.output)

    # Check that input folder exists
    if not input_dir.exists():
        raise FileNotFoundError(f"Input folder does not exist: {input_dir}")

    # Get image files
    image_files = sorted([
        file for file in input_dir.iterdir()
        if file.suffix.lower() in EXTENSIONS
    ])

    # Check that images were found
    if not image_files:
        raise ValueError(f"No image files found in: {input_dir}")

    results = []

    # Process each image
    for image_path in image_files:
        result, img_rgb, red_mask = calculate_red_area(
            image_path,
            red_offset=args.red_offset,
            min_red_value=args.min_red_value,
        )

        results.append(result)

        print(f"Processed image: {result['image_name']}")
        print(f"Red area: {result['red_area_pixels']} pixels")
        print(f"Total area: {result['total_area_pixels']} pixels")
        print(f"Red percentage: {result['red_percentage']}%")
        print("-" * 50)

        if args.show:
            plot_image_and_mask(
                img_rgb=img_rgb,
                red_mask=red_mask,
                image_name=result["image_name"]
            )

    # Save all results at the end
    save_results_to_excel(results, output_file)

    print(f"Results saved to: {output_file}")


if __name__ == "__main__":
    main()