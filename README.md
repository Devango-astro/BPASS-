# BPASS Spectral Templates Preparation

This repository provides scripts to process BPASS model output files (spectral and starmass .dat files) into a compressed `.npz` template suitable for scientific analysis.

## Workflow

- Searches for `spectra-bin-imf135_300*.dat` and `starmass-bin-imf135_300*.dat` files in the current directory.
- Loads spectra (removing first column), and stacks all files into a 3D array.
- Extracts metallicity information from filenames.
- Builds a wavelength grid (`lam`), ages array, and creates a FWHM array of zeros.
- Loads "starmass" files, extracts the second column, and stacks as stellar mass history.
- Saves all arrays into a compressed numpy archive (`bpass_templates.npz`).

## Output

- `bpass_templates.npz` contains:
  - `templates`: Stacked spectra, shape (wavelengths, ages, metallicities)
  - `masses`: Stellar masses, shape (ages, metallicities)
  - `lam`: Wavelength grid
  - `ages`: Age grid
  - `metals`: Metallicity array
  - `fwhm`: FWHM array (zeros)

## Usage

1. Place all relevant BPASS `.dat` files in the script's directory.
2. Run the script:
   ```
   python Template_creating.py
   ```
3. The output file `bpass_templates.npz` will be created in the same folder.

## Requirements

- Python 3
- Numpy

For scientific details on BPASS models, see: [BPASS project](https://bpass.auckland.ac.nz/)
