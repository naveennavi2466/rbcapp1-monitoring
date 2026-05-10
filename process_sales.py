import csv

input_file = "sales-data.csv"
output_file = "below-average-sales.csv"

rows = []
f = open(input_file, newline="")
reader = csv.DictReader(f)
col_names = reader.fieldnames
for row in reader:
    rows.append(row)
f.close()

# calculate price per sqft for each row
good_rows = []
for row in rows:
    try:
        price = float(row["SalePrice"])
        sqft = float(row["SqFtTotLiving"])
        if sqft > 0:
            row["price_per_sqft"] = price / sqft
            good_rows.append(row)
    except:
        pass

# get the average
total = 0
for row in good_rows:
    total = total + row["price_per_sqft"]
avg = total / len(good_rows)
print("average price per sqft is: " + str(round(avg, 2)))

# keep only the ones below average
result = []
for row in good_rows:
    if row["price_per_sqft"] < avg:
        result.append(row)

# write to new csv file
out_cols = list(col_names) + ["price_per_sqft"]
outfile = open(output_file, "w", newline="")
writer = csv.DictWriter(outfile, fieldnames=out_cols)
writer.writeheader()
writer.writerows(result)
outfile.close()
print("done. saved to " + output_file)
