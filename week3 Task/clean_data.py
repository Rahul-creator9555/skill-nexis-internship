"""
Assignment: Clean a messy dataset in Pandas
Dataset: data.csv (fitness tracker log - duration, date, pulse, maxpulse, calories)

Goal: handle missing values, fix bad rows, remove duplicates,
filter out unrealistic entries, and add a couple of new columns.
"""

import pandas as pd

# ---------------------------------------------------------
# 1. Load the data
# ---------------------------------------------------------
df = pd.read_csv("data.csv")

print("Original shape:", df.shape)
print(df.head(10))
print()

# quick look at what's wrong with it
print(df.info())
print("\nMissing values per column:")
print(df.isnull().sum())
print("\nDuplicate rows:", df.duplicated().sum())

# ---------------------------------------------------------
# 2. Fix the Date column
# ---------------------------------------------------------
# dates are stored as strings like '2020/12/01' (with quotes) but one
# row (2020/12/26) got entered as a plain number 20201226, and one row
# is just missing. Convert everything properly first.
df["Date"] = df["Date"].astype(str).str.replace("'", "", regex=False)

# row 20201226 doesn't match the 'YYYY/MM/DD' pattern, so fix it manually
df["Date"] = df["Date"].replace("20201226", "2020/12/26")

df["Date"] = pd.to_datetime(df["Date"], format="%Y/%m/%d", errors="coerce")

# drop the one row where the date is completely missing/unfixable
df = df.dropna(subset=["Date"])

# ---------------------------------------------------------
# 3. Handle missing values in Calories
# ---------------------------------------------------------
# Calories has 2 missing values. Instead of dropping those rows,
# fill them with the column mean so we don't lose the workout data.
mean_calories = df["Calories"].mean()
df["Calories"] = df["Calories"].fillna(round(mean_calories, 1))

# ---------------------------------------------------------
# 4. Remove duplicate rows
# ---------------------------------------------------------
df = df.drop_duplicates()

# ---------------------------------------------------------
# 5. Filter out rows with unrealistic values
# ---------------------------------------------------------
# Duration of 450 minutes for a workout is clearly a typo (probably
# meant 45), and Pulse of 130 with Maxpulse of 101 doesn't make sense
# (max pulse should be higher than resting pulse). Filter these out.
df = df[df["Duration"] <= 120]
df = df[df["Maxpulse"] >= df["Pulse"]]

# ---------------------------------------------------------
# 6. Create new columns
# ---------------------------------------------------------
# Calories burned per minute of exercise
df["Calories_per_min"] = round(df["Calories"] / df["Duration"], 2)

# simple intensity label based on max pulse reached
def intensity(mp):
    if mp < 120:
        return "Low"
    elif mp < 140:
        return "Medium"
    else:
        return "High"

df["Intensity"] = df["Maxpulse"].apply(intensity)

# reset the index since we've dropped/filtered rows along the way
df = df.reset_index(drop=True)

# ---------------------------------------------------------
# 7. Final check + save
# ---------------------------------------------------------
print("\nCleaned shape:", df.shape)
print(df.head(10))
print("\nMissing values after cleaning:")
print(df.isnull().sum())

df.to_csv("cleaned_data.csv", index=False)
print("\nSaved cleaned_data.csv")
