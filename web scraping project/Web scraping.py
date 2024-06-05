from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html # type: ignore
import csv

def scrape_product_data(url):
    try:
        # Initialize a Chrome webdriver
        options = webdriver.ChromeOptions()  
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems

        # Initialize the Chrome webdriver with options
        driver = webdriver.Chrome(options=options)

        # Open the URL in the browser
        driver.get(url)

        # Wait for the page to load (You might need to adjust this depending on your internet speed)
        wait = WebDriverWait(driver, 300)
        wait.until(EC.presence_of_element_located((By.XPATH, "//h3[@class='name']")))

        # Get the page source after JavaScript rendering
        html_content = driver.page_source

        # Close the browser
        driver.quit()

        # Parse the HTML content using lxml
        tree = html.fromstring(html_content)

        # Extract product names and prices using XPath
        product_names = tree.xpath("//h3[@class='name']/text()")
        product_prices = tree.xpath("//div[@class='prc']/text()")
        svr_product_names = [name.strip() for name in product_names if name.strip().startswith("SVR")]

        print("Number of product names:", len(product_names))
        print("Number of product prices:", len(product_prices))
        print("Number of SVR product names:", len(svr_product_names))

        # Write the output to a CSV file
        output_file_path = 'output.csv'
        with open(output_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['product name', 'product price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for name, price in zip(product_names , product_prices):
                writer.writerow({'product name': name, 'product price': price.strip()})

        print("Output has been written to:", output_file_path)

    except Exception as e:
        print("An error occurred:", e)

# Example usage:
url = "https://www.jumia.com.tn/catalog/?q=ecran+solaire&page=2#catalog-listing"
scrape_product_data(url)

