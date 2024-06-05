import csv

def find_top_10_cheapest_products():
    products = []  # List to store product information

    # Read data from CSV and store in the products list
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

            products.append({'product name': row['product name'], 'product price': price})

    # Sort the products list based on price in ascending order
    sorted_products = sorted(products, key=lambda x: x['product price'])

    # Select the top 10 cheapest products
    top_10_cheapest = sorted_products[:10]

    return top_10_cheapest

# Main function
def main():
    top_10_cheapest_products = find_top_10_cheapest_products()
    if top_10_cheapest_products:
        print("Top 10 Cheapest Products:")
        for index, product in enumerate(top_10_cheapest_products, start=1):
            print(f"{index}. Product Name: {product['product name']}, Price: {product['product price']} TND")
    else:
        print("No products found.")

if __name__ == "__main__":
    main()
