"""
explore_data.py - first look at the used car dataset.

What this script does:
  1. Reads the CSV straight out of vehicles_github_ready.zip (no need to unzip).
  2. Prints a short summary: how many cars, which columns, how much is missing.
  3. Counts the data problems we will need to clean (fake prices, fake mileage...).
  4. Saves 4 charts into a "charts" folder, for our presentation.

How to run it (from the project folder, in the Terminal):
  pip install pandas matplotlib
  python3 explore_data.py
"""

import os
import zipfile

import matplotlib
matplotlib.use("Agg")  # save charts to files instead of opening windows
import matplotlib.pyplot as plt
import pandas as pd

ZIP_FILE = "vehicles_github_ready.zip"
CSV_INSIDE_ZIP = "vehicles_compact.csv"
CHART_FOLDER = "charts"


# ---------------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------------
# The zip holds two files (the CSV and a README.txt), so we open
# the zip ourselves and tell pandas which file to read.
with zipfile.ZipFile(ZIP_FILE) as z:
    with z.open(CSV_INSIDE_ZIP) as f:
        cars = pd.read_csv(f, low_memory=False)

# Some prices are stored as text; turn them into numbers.
cars["price"] = pd.to_numeric(cars["price"], errors="coerce")

print("=" * 60)
print("DATASET SUMMARY")
print("=" * 60)
print(f"Number of cars (rows): {len(cars):,}")
print(f"Number of columns:     {cars.shape[1]}")
print("Columns:", ", ".join(cars.columns))


# ---------------------------------------------------------------
# 2. Missing values: what % of each column is empty?
# ---------------------------------------------------------------
print("\n% of values missing in each column:")
missing = (cars.isna().mean() * 100).round(1).sort_values(ascending=False)
print(missing.to_string())


# ---------------------------------------------------------------
# 3. Data problems we will need to clean
# ---------------------------------------------------------------
print("\nDATA PROBLEMS FOUND")
print("-" * 60)
print(f"Cars listed at $0:                {(cars['price'] == 0).sum():,}")
print(f"Cars listed under $1,000:         {(cars['price'] < 1000).sum():,}")
print(f"Cars listed over $150,000:        {(cars['price'] > 150000).sum():,}")
print(f"Cars with over 500,000 miles:     {(cars['odometer'] > 500000).sum():,}")
print(f"Cars older than 2000:             {(cars['year'] < 2000).sum():,}")
print(f"Listings outside the US:          {(cars['address_country'] != 'US').sum():,}")
print(f"Different model spellings:        {cars['model'].nunique():,}")


# ---------------------------------------------------------------
# 4. A roughly cleaned copy, just so the charts make sense.
#    (The real cleaning step comes later in the project.)
# ---------------------------------------------------------------
clean = cars[
    (cars["address_country"] == "US")
    & cars["price"].between(1000, 150000)
    & cars["odometer"].between(0, 500000)
    & (cars["year"] >= 2000)
]
print(f"\nCars left after a rough clean-up: {len(clean):,}")
print(f"Typical (median) price:           ${clean['price'].median():,.0f}")
print(f"Typical (median) mileage:         {clean['odometer'].median():,.0f} miles")
print(f"Typical (median) year:            {clean['year'].median():.0f}")


# ---------------------------------------------------------------
# 5. Charts for the presentation
# ---------------------------------------------------------------
os.makedirs(CHART_FOLDER, exist_ok=True)
sample = clean.sample(5000, random_state=1)  # 5,000 dots is enough for scatter plots

# Chart 1: how prices are spread out
plt.figure(figsize=(8, 5))
plt.hist(clean["price"], bins=60, color="#4C78A8")
plt.title("How used car prices are spread out")
plt.xlabel("Asking price ($)")
plt.ylabel("Number of cars")
plt.tight_layout()
plt.savefig(f"{CHART_FOLDER}/1_price_distribution.png", dpi=150)
plt.close()

# Chart 2: newer cars cost more
plt.figure(figsize=(8, 5))
plt.scatter(sample["year"], sample["price"], s=5, alpha=0.3, color="#4C78A8")
plt.title("Newer cars cost more")
plt.xlabel("Year")
plt.ylabel("Asking price ($)")
plt.tight_layout()
plt.savefig(f"{CHART_FOLDER}/2_price_vs_year.png", dpi=150)
plt.close()

# Chart 3: more miles, lower price
plt.figure(figsize=(8, 5))
plt.scatter(sample["odometer"], sample["price"], s=5, alpha=0.3, color="#4C78A8")
plt.title("Cars with more miles are cheaper")
plt.xlabel("Mileage (odometer, miles)")
plt.ylabel("Asking price ($)")
plt.tight_layout()
plt.savefig(f"{CHART_FOLDER}/3_price_vs_mileage.png", dpi=150)
plt.close()

# Chart 4: the 10 most common brands
plt.figure(figsize=(8, 5))
clean["manufacturer"].value_counts().head(10).sort_values().plot.barh(color="#4C78A8")
plt.title("10 most common brands in the data")
plt.xlabel("Number of cars")
plt.tight_layout()
plt.savefig(f"{CHART_FOLDER}/4_top_brands.png", dpi=150)
plt.close()

print(f"\nSaved 4 charts in the '{CHART_FOLDER}' folder.")
