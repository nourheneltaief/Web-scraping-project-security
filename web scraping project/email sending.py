import csv
import smtplib
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from itertools import zip_longest
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read CSV file
def read_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

# Function to calculate score for each row
def calculate_score(row, price_range, brand_preference, brand_category_preference):
    score = 0

    # Price weight calculation
    price = float(row['product price'])
    if price >= price_range[0] and price <= price_range[1]:
        price_weight = 0.9  # High weight if price falls within user's preferred range
    else:
        price_weight = 0.1  # Low weight if price falls outside user's preferred range

    # Product rate weight calculation
    if row['product rate'] == 'None':
        rate_weight = 0.1
    else:
        rate_weight = float(row['product rate']) / 5  # Assuming rate varies from 1 to 5, converted to percentage

    # Brand weight calculation
    if row['brand'] == brand_preference:
        brand_weight = 0.7  # Higher weight if the row's brand matches user's preference
    else:
        brand_weight = 0.3  # Lower weight if the row's brand doesn't match user's preference

    # Brand category weight calculation
    if row['brand category'] == 'local':
        brand_category_weight = brand_category_preference[0]  # Use user's preference
    elif row['brand category'] == 'international':
        brand_category_weight = brand_category_preference[1]  # Use user's preference for international
    else:
        brand_category_weight = 0.5  # Default weight if brand category is not specified

    # Calculate final score for the row
    score = price_weight * rate_weight * brand_weight * brand_category_weight
    return score

# Main function
def main():
    # Read CSV file
    filename = 'clean output.csv'
    data = read_csv(filename)

    # Get user preferences
    min_price = float(input("Enter minimum price: "))
    max_price = float(input("Enter maximum price: "))
    brand_preference = input("Enter preferred brand (or leave blank if no preference): ")
    brand_category_preference = input("Enter preferred brand category (local/international) (or leave blank if no preference): ").lower()
    if brand_category_preference == 'local':
        brand_category_weight = (0.8, 0.2)
    elif brand_category_preference == 'international':
        brand_category_weight = (0.2, 0.7)
    else:
        brand_category_weight = (0.5, 0.5)

    # Calculate weights
    price_range = (min_price, max_price)

    # Calculate scores for each row
    scores = []
    for row in data:
        score = calculate_score(row, price_range, brand_preference, brand_category_weight)
        scores.append((row['product name'], score))

    # Create dataframe from scores
    df_scores = pd.DataFrame(scores, columns=['Product Name', 'Product Score'])

    # Sort dataframe by score in descending order
    df_scores = df_scores.sort_values(by='Product Score', ascending=False)

    # Display top 5 products based on scores
    top_5_products = df_scores.head(5)

    # Send email
    send_email(top_5_products)

    # Print confirmation message
    print("Top 5 Products have been sent via email.")

def send_email(top_5_products):
    # Email configuration
    sender_email = 'trabelsizeineb@********'
    receiver_email = 'nourltaief399@******'
    password = '*******'

    # Email content
    subject = 'Top 5 Products Based on Score'
    body = "The best 5 products found based on your preferences are:\n\n"
    for index, row in top_5_products.iterrows():
        body += f"{row['Product Name']}\n"


    # Create message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Send email
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    main()
