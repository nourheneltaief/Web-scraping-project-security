import pandas as pd

# Provide the full path to the CSV file
file_path ='output.csv'

# Load the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Remove duplicates (if any)
df.drop_duplicates(inplace=True)

#Price column
# Extract numeric part from price column and convert to numeric
df['product price'] = df['product price'].str.replace('TND', '').astype(float)

#rate column
# Remove "out of 5" string from review column and convert to numeric
df['product rate'] = df['product rate'].str.replace('out of 5', '').astype(float)
# Replace blank values with 'None' as a string
df['product rate'].fillna('None', inplace=True)

#brand name column
# Extract brand name from product name column
df['brand'] = df['product name'].apply(lambda x: x.split()[0])

# Extract brand name from product name column
def extract_brand(product_name):
    # Split the product name by whitespace
    parts = product_name.split()
    brand = parts[0]
    if brand.lower() in ['fruit']:
        brand = 'Fruit Of The Wokali'
    # Check if the brand is in the specified list
    if brand.lower() in ['dr', 'milva', 'proderma', 'pro', 'la']:
        # If yes, add the next word as part of the brand name
        if len(parts) > 1:
            brand += ' ' + parts[1]
    return brand

df['brand'] = df['product name'].apply(extract_brand)

#product category column
# Function to classify products based on keywords in product name
def classify_product(product_name):
    if 'lait' in product_name.lower() or 'lotion' in product_name.lower():
        return 'lotion'
    elif 'spray' in product_name.lower():
        return 'spray'
    elif 'creme' in product_name.lower():
        return 'creme'
    elif 'Ecran' in product_name.lower() or 'sun' in product_name.lower() or 'solaire' in product_name.lower():
        return 'sunscreen'
    else:
        return 'other'

# Create a new column "product_category" by applying the classify_product function to the "product_name" column
df['product category'] = df['product name'].apply(classify_product)

#brand category column
# List of local brands
local_brands = ['Dermacare', 'SunSafe®', 'Proderma Dermalight', 'Milva Olcare', 'Fruit Of The Wokali', 'Arvea']

# Function to classify brands as local or international
def classify_brand(brand):
    if brand in local_brands:
        return 'local'
    else:
        return 'international'

# Create a new column "brand_category" by applying the classify_brand function to the "brands" column
df['brand category'] = df['brand'].apply(classify_brand)

#quantity
import re
# Function to extract quantity and unit from product name
def extract_quantity_and_unit(product_name):
    # Regular expression pattern to extract the quantity and unit before 'ML' or 'GR'
    pattern = r'(\d+)\s*(ML|GR)'
    match = re.search(pattern, product_name, re.IGNORECASE)
    if match:
        quantity = int(match.group(1))
        unit = match.group(2).upper()  # Convert unit to uppercase (ML or GR)
        if unit == 'ML':
            return f'{quantity} ML'
        elif unit == 'GR':
            return f'{quantity} GR'
    else:
        return None

# Create a new column "quantity" by applying the extract_quantity_and_unit function to the "product_name" column
df['quantity'] = df['product name'].apply(extract_quantity_and_unit)
# Remove rows where the quantity column has no value
df = df[df['quantity'].notna()]

# Display the first few rows of the DataFrame to understand its structure
print(df.head(50))

# Export the DataFrame to a CSV file
df.to_csv('clean output.csv', index=False)
df.to_excel('clean_output.xlsx', index=False)