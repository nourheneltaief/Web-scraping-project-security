import csv

# Function to clean the product rate column
def clean_product_rate(rate_str):
    # Extract the first character which represents the rating number
    return rate_str.split()[0]

# Function to clean the product rate column in the CSV file
def clean_csv_product_rate(file_path):
    cleaned_data = []
    # Read data from the CSV file and clean the product rate column
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Clean the product rate data
            row['product rate'] = clean_product_rate(row['product rate'])
            cleaned_data.append(row)

    # Write the cleaned data back to the CSV file
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['product name', 'product price', 'product rate']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_data)

# Function to extract and print all products with a rating of 5
def print_products_with_rating_5(file_path):
    top_products = []

    # Read data from the CSV file and filter products with a rating of 5
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['product rate'] == '5':
                top_products.append(row)

    # Print all products with a rating of 5
    print("Products with Rating of 5 (out of 5):")
    for index, product in enumerate(top_products, start=1):
        print(f"{index}. Product Name: {product['product name']}, Rating: {product['product rate']} out of 5")

    return top_products

# Function to select the top 10 cheapest products
def select_top_10_cheapest_products(products):
    # Sort the products by price in ascending order
    products.sort(key=lambda x: float(x['product price'].replace('TND', '').strip()))

    # Select the top 10 cheapest products
    top_10_cheapest = products[:10]

    # Print the top 10 cheapest products
    print("\nTop 10 Cheapest Products with Rating of 5:")
    for index, product in enumerate(top_10_cheapest, start=1):
        print(f"{index}. Product Name: {product['product name']}, Price: {product['product price']} TND")

# Clean the product rate column in the output.csv file
clean_csv_product_rate('output.csv')

# Extract products with a rating of 5
top_rated_products = print_products_with_rating_5('output.csv')

# Select the top 10 cheapest products with a rating of 5
select_top_10_cheapest_products(top_rated_products)

