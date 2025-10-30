import numpy as np
import glob
import re

# Find all .dat files starting with the given prefix
filenames = sorted(glob.glob("spectra-bin-imf135_300*.dat"))

if not filenames:
    print("No files found matching pattern 'spectra-bin-imf135_300*.dat'")
    exit(1)

print(f"Found {len(filenames)} files")

# Read each file into a 2D array (excluding the first column) and put in a list
arrays = []
for fname in filenames:
    try:
        data = np.loadtxt(fname)
        # Remove the first column
        data = data[:, 1:]
        arrays.append(data)
        print(f"Loaded {fname}: shape {data.shape}")
    except Exception as e:
        print(f"Error loading {fname}: {e}")
        continue

if not arrays:
    print("No valid files could be loaded")
    exit(1)
# Stack along the third axis to get shape (10000, 52, N)
templates = np.stack(arrays, axis=2)
print(templates.shape)

# Assign lam array: same size as first axis of templates, values from 1 to 100000
lam = np.linspace(1, 100000, templates.shape[0])
print(f"lam array created with shape {lam.shape} and range {lam[0]} - {lam[-1]}")
print(lam)

# Assign fwhm array: same size as first axis of templates, all values 0.0
fwhm = np.zeros(templates.shape[0])
print(f"fwhm array created with shape {fwhm.shape} and all values {fwhm[0]}")
print(fwhm.shape)

# Extract metallicity values from filenames
metals = []
for f in filenames:
    # Find the substring starting with 'z' followed by numbers (and possibly 'em' for very low Z)
    match = re.search(r"z([em\d]+)", f)
    if match:
        code = match.group(1)
        if code.startswith("em"):
            # e.g. zem5 -> 1e-5
            metals.append(float("1e-" + code[2:]))
        else:
            # e.g. z020 -> 0.02, z030 -> 0.03, z002 -> 0.002
            # Remove leading zeros, but keep at least two digits for the decimal
            # So z020 -> 0.02, not 0.2
            # We'll pad to 3 digits, then convert: z020 -> 020 -> 0.020
            num = code
            # Remove any non-digit characters just in case
            num = "".join(filter(str.isdigit, num))
            if len(num) == 0:
                metals.append(np.nan)
            else:
                # Pad to at least 3 digits for safety
                num = num.zfill(3)
                metals.append(float("0." + num))
    else:
        print(
            f"Warning: No metallicity code found in filename '{f}'. Assigning np.nan."
        )
        metals.append(np.nan)
metals = np.array(metals)
print(metals)

# Create ages array: from 6 to 11 (inclusive) in 0.1 increments
ages = np.arange(6, 11.1, 0.1)
# print(f"ages array created with shape {ages.shape} and range {ages[0]} - {ages[50]}")
print(ages.shape)

# --- New addition: process starmass-bin-imf135_300*.dat files ---

# Find all .dat files starting with the given prefix for starmass
starmass_filenames = sorted(glob.glob("starmass-bin-imf135_300*.dat"))

if not starmass_filenames:
    print("No files found matching pattern 'starmass-bin-imf135_300*.dat'")
else:
    print(f"Found {len(starmass_filenames)} starmass files")

    # Read each file, extract only the second column, and collect in a list
    starmass_columns = []
    for fname in starmass_filenames:
        try:
            data = np.loadtxt(fname)
            # Extract the second column (index 1)
            col = data[:, 1]
            starmass_columns.append(col)
            print(f"Loaded {fname}: extracted column shape {col.shape}")
        except Exception as e:
            print(f"Error loading {fname}: {e}")
            continue

    if not starmass_columns:
        print("No valid starmass files could be loaded")
    else:
        # Stack columns together into a 2D array of shape (51, N_files)
        starmass_array = np.column_stack(starmass_columns)
        print(f"Stacked starmass array shape: {starmass_array.shape}")

        # Save the starmass_array as a compressed numpy file with relevant arrays
        # The convention is to use keys: templates, masses, lam, ages, metals, fwhm
        # Here, starmass_array is 'masses', and we save the previously defined arrays as well

np.savez_compressed(
    "bpass_templates.npz",
    templates=templates,
    masses=starmass_array,
    lam=lam,
    ages=ages,
    metals=metals,
    fwhm=fwhm,
)
print("Saved BPASS templates to bpass_starmass_templates.npz")
