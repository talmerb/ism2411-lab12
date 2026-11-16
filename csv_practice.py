# Reflection 1: Both Python and Excel can read sales data, calculate totals,
# and filter orders. Python makes it easier to repeat the same steps across
# many files automatically, while Excel makes quick visual checks, cell edits,
# and charts easier without writing code.
#
# Reflection 2: An online store could append a log entry each time its daily
# sales report runs, recording the timestamp and total revenue. Append mode
# keeps earlier entries so employees can review past runs instead of losing
# the history whenever a new report is generated.

import csv
from datetime import datetime
from decimal import Decimal
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent / "data"
SALES_FILE = DATA_DIR / "sales.csv"

# Exercise 1: Verify the downloaded file's header and 12 data rows.
print("Exercise 1: Check the source file")
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    rows = list(reader)
assert header == ["product", "price", "quantity"]
assert len(rows) == 12
print(f"Header: {header}; data rows: {len(rows)}")

# Exercise 2: Print raw rows, including the header. CSV values are strings.
print("\nExercise 2: Raw rows")
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
        assert all(isinstance(value, str) for value in row)

# Exercise 3: Store and print the header separately, then print data rows.
print("\nExercise 3: Skip the header")
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)

# Exercise 4: Convert strings to numeric values and compute revenue.
# Decimal keeps currency arithmetic exact; int converts the unit counts.
print("\nExercise 4: Order totals")
total_revenue = Decimal("0")
order_totals = []
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        product = row[0]
        price = Decimal(row[1])
        quantity = int(row[2])
        total = price * quantity
        order_totals.append(total)
        total_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")
print(f"Total revenue: ${total_revenue:.2f}")

# Exercise 5: Regenerate cleaned.csv with only orders above $100.
print("\nExercise 5: Filter and write")
original_count = 0
written_count = 0
with open(SALES_FILE, newline="", encoding="utf-8") as source:
    with open(DATA_DIR / "cleaned.csv", "w", newline="", encoding="utf-8") as output:
        reader = csv.reader(source)
        next(reader)
        writer = csv.writer(output)
        writer.writerow(["Product", "Price", "Qty", "Total"])
        for row in reader:
            original_count += 1
            product = row[0]
            price = Decimal(row[1])
            quantity = int(row[2])
            total = price * quantity
            if total > Decimal("100"):
                writer.writerow([product, f"{price:.2f}", quantity, f"{total:.2f}"])
                written_count += 1
print(f"Wrote {written_count} of {original_count} original rows to data/cleaned.csv")

# Exercise 6: Prefer csv.reader for simple files with a fixed column order.
# Prefer DictReader for readable named fields, especially if column order changes.
print("\nExercise 6: DictReader totals")
dict_total = Decimal("0")
dict_order_totals = []
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["product"]
        price = Decimal(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_order_totals.append(total)
        dict_total += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")
assert dict_order_totals == order_totals
assert dict_total == total_revenue
print(f"DictReader total revenue: ${dict_total:.2f} (matches Exercise 4)")

# Exercise 7: Accumulate repeated products and print in alphabetical order.
print("\nExercise 7: Sales summary by product")
summary = {}
with open(SALES_FILE, newline="", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        product = row["product"]
        revenue = Decimal(row["price"]) * int(row["quantity"])
        summary[product] = summary.get(product, Decimal("0")) + revenue
for product in sorted(summary):
    print(f"{product}: ${summary[product]:.2f}")

# Exercise 8: Append one entry per execution without replacing earlier runs.
print("\nExercise 8: Append a run log")
with open(DATA_DIR / "run_log.txt", "a", encoding="utf-8") as log:
    timestamp = datetime.now().astimezone().isoformat(timespec="microseconds")
    log.write(f"{timestamp} | Total revenue: ${total_revenue:.2f}\n")
print("Appended one entry to data/run_log.txt")
