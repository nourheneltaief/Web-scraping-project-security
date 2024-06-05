import csv

def clean_product_rate(rate_str):
    # Extract the first character which represents the rating number
    return rate_str.split()[0]

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

# Clean the product rate column in the output.csv file
clean_csv_product_rate('output.csv')

# Function to extract and print the top 10 products with the highest rating
def print_top_20_highest_rated_products(file_path):
    top_products = []

    # Read data from the CSV file and filter products with a rating of 5
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['product rate'] == '5':
                top_products.append(row)

    # Sort the top products by rating in descending order
    top_products.sort(key=lambda x: int(x['product rate']), reverse=True)

    # Print the top 20 products with the highest rating
    print("Top 20 Products with Highest Rating (5 out of 5):")
    for index, product in enumerate(top_products[:20], start=1):
        print(f"{index}. Product Name: {product['product name']}, Rating: {product['product rate']} out of 5")

# Clean the product rate column in the output.csv file
clean_csv_product_rate('output.csv')

# Extract and print the top 10 products with the highest rating
print_top_20_highest_rated_products('output.csv')





