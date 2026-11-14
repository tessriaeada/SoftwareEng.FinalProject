"""
clean_data.py - step 2 of the project plan: clean the used car data.

What this script does:
  1. Reads the original listings straight out of vehicles_github_ready.zip.
  2. Removes listings that are duplicated, outside the US, or have
     unrealistic or missing prices, years, mileage, brands or models.
  3. Tidies the text columns so the same thing is always spelled the same way.
  4. Prints a report of how many listings each rule removed.
  5. Saves the cleaned data as cars_clean.zip, ready for the models.

How to run it (from the project folder, in the Terminal):
  pip install pandas
  python3 clean_data.py
"""

import zipfile

import pandas as pd

ZIP_FILE = "vehicles_github_ready.zip"
CSV_INSIDE_ZIP = "vehicles_compact.csv"
OUTPUT_FILE = "cars_clean.zip"

# The limits we use to decide what counts as a realistic listing.
# They match the rough clean-up in explore_data.py.
MIN_PRICE = 1_000        # below this is usually a fake or placeholder price
MAX_PRICE = 150_000      # above this is usually a typo or a rare supercar
MAX_MILES = 500_000      # almost no car is driven further than this
MIN_YEAR = 2000          # older cars behave like collectibles, not normal used cars
MAX_YEAR = 2027          # a "2027" model can already be on sale in late 2026


# ---------------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------------
with zipfile.ZipFile(ZIP_FILE) as z:
    with z.open(CSV_INSIDE_ZIP) as f:
        cars = pd.read_csv(f, low_memory=False)

# Some prices are stored as text; turn them into numbers.
# Anything that is not a number becomes empty (and is removed below).
cars["price"] = pd.to_numeric(cars["price"], errors="coerce")

print("=" * 60)
print("CLEANING THE USED CAR DATA")
print("=" * 60)
print(f"Listings at the start: {len(cars):,}\n")


# ---------------------------------------------------------------
# 2. Remove bad listings, one rule at a time
# ---------------------------------------------------------------
# Each rule keeps the good rows and reports how many it removed,
# so we can explain every number in the presentation.
report = []


def keep(rows_to_keep, reason):
    """Keep only rows_to_keep and record how many rows were removed."""
    global cars
    removed = len(cars) - rows_to_keep.sum()
    cars = cars[rows_to_keep]
    report.append((reason, removed))


keep(~cars.duplicated(), "Exact duplicate listings")
keep(cars["address_country"] == "US", "Outside the US or no country")
keep(cars["price"].between(MIN_PRICE, MAX_PRICE),
     f"Price missing or outside ${MIN_PRICE:,}-${MAX_PRICE:,}")
keep(cars["year"].between(MIN_YEAR, MAX_YEAR),
     f"Year missing or outside {MIN_YEAR}-{MAX_YEAR}")
keep(cars["odometer"].between(0, MAX_MILES),
     f"Mileage missing or over {MAX_MILES:,}")
keep(cars["manufacturer"].notna() & cars["model"].notna(),
     "Brand or model missing")
keep(cars["title_status"] != "parts only",
     "Sold for parts only (not a working car)")


# ---------------------------------------------------------------
# 3. Tidy the columns
# ---------------------------------------------------------------
# "size" is completely empty, and the country is now always "US".
cars = cars.drop(columns=["size", "address_country"])

# Write brand and model names the same way every time:
# lower case, no extra spaces ("  Ford  F-150 " -> "ford f-150").
for column in ["manufacturer", "model"]:
    cars[column] = (cars[column].str.lower()
                                .str.strip()
                                .str.replace(r"\s+", " ", regex=True))

# Store year, price and mileage as whole numbers (2016, not 2016.0).
cars = cars.astype({"year": int, "price": int, "odometer": int})


# ---------------------------------------------------------------
# 4. Report what happened
# ---------------------------------------------------------------
print("Listings removed by each rule:")
for reason, removed in report:
    print(f"  {reason:<45} {removed:>8,}")

start = len(cars) + sum(removed for _, removed in report)
print(f"\nListings kept:       {len(cars):,} "
      f"({len(cars) / start:.0%} of the original)")
print(f"Typical (median) price:   ${cars['price'].median():,.0f}")
print(f"Typical (median) mileage: {cars['odometer'].median():,.0f} miles")
print(f"Typical (median) year:    {cars['year'].median():.0f}")

print("\nStill missing in the cleaned data (% of listings):")
missing = (cars.isna().mean() * 100).round(1)
print(missing[missing > 0].sort_values(ascending=False).to_string())


# ---------------------------------------------------------------
# 5. Save the cleaned data (zipped, so it fits on GitHub)
# ---------------------------------------------------------------
cars.to_csv(OUTPUT_FILE, index=False,
            compression={"method": "zip", "archive_name": "cars_clean.csv"})
print(f"\nSaved the cleaned data to {OUTPUT_FILE}.")
