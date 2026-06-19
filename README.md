# Immunofluorescence image red area quantification
This repository contains Python code to quantify the percentage of red area in immunofluorescence images.

This repository contains Python code to quantify the percentage of red area in immunofluorescence images.

The script processes all images in an input folder, identifies red pixels using an RGB threshold, calculates the red area percentage, and saves the results to an Excel file.

## Method

A pixel is classified as red when:

```python
R > G + 20
R > B + 20
R > 20
```

## Repository structure
```text
Immunofluorescence-image-red-area-quantification/
├── scripts/
│   └── quantify_red_area.py
├── data/
│   ├── README.md
│   └── example_images/
├── results/
├── figures/
├── README.md
├── LICENSE
├── CITATION.cff
├── requirements.txt
└── .gitignore
```

## Installation

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage
To run the analysis:
```bash
python scripts/quantify_red_area.py
```
By default, the script reads images from:

```bash
data/
```
and saves the output Excel file as:

```bash
results/red_area_results.xlsx
```
To display the original images and their red masks:
```bash
python scripts/quantify_red_area.py --show
```
