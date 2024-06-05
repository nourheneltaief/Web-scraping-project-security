import csv

def find_best_product():
    best_product = None
    min_price = float('inf')

    with open('output.csv', 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                price = float(row['product price'].replace('TND', ''))  # Assuming price is in TND
            except ValueError:
                # Handle the case where price cannot be converted to float
                # For example, if price contains non-numeric characters
                print(f"Ignoring row with invalid price: {row}")
                continue

            if price < min_price:
                min_price = price
                best_product = row['product name']

    return best_product

# Main function
def main():
    best_product_name = find_best_product()
    if best_product_name:
        print(f"The best product is: {best_product_name}")
    else:
        print("No products found.")

if __name__ == "__main__":
    main()


