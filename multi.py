import csv

# Open a new CSV file to write the table
with open("multiplication_grid.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)

    # 1. Write the header row: an empty corner cell followed by numbers 1 to 9
    header = [""] + [str(i) for i in range(1, 10)]
    writer.writerow(header)

    # 2. Write the data rows (1 to 9)
    for i in range(1, 10):
        # Start each row with the current row number as the first column
        row = [str(i)]
        
        # Calculate and append the product for each column (1 to 9)
        for j in range(1, 10):
            row.append(str(i * j))
            
        writer.writerow(row)
        writer.writerow(row)

print("The multiplication grid has been successfully saved to 'multiplication_grid.csv'!")