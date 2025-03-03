import time
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import cloudscraper
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import OutputData as od
from webdriver_manager.chrome import ChromeDriverManager
from ui import get_user_input



"copywritten by kariem hassan can be used for personal learning only code cannot be redistributed nor posted online without permission"
"can only share the code cannot claim code is yours thanks!"


scraper = cloudscraper.create_scraper()
# Declare global variables
autotrader = False
carscom = False
carvana = False
cargurus = False






def setup_google():
    scraper = cloudscraper.create_scraper()

    # Create ChromeOptions object for custom Chrome setup
    chrome_options = webdriver.ChromeOptions()

    # Optional: Get a random user-agent (if desired)
    def get_random_user_agent():
        ua = UserAgent()
        return ua.random

    # Add random user-agent to Chrome options
    chrome_options.add_argument(f"user-agent={get_random_user_agent()}")


    # Use WebDriverManager to automatically get the appropriate ChromeDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)


    return driver
def incremental_scroll(driver, pause_time=3):
    """Scroll incrementally until the end of the page is reached."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom of the page
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait for new content to load
        time.sleep(pause_time)

        # Calculate new scroll height after scrolling
        new_height = driver.execute_script("return document.body.scrollHeight")

        # If the scroll height hasn't changed, we are at the end of the page
        if new_height == last_height:
            print("Reached the bottom of the page.")
            break

        last_height = new_height
    return None

def FindCarsFromAutotrader(criteria, cars):
    first_record = 0
    data = []
    driver = setup_google()
    for car in cars:
        url = (
            f"https://www.autotrader.com//cars-for-sale/all/cars-between-{criteria['price_from']}-and-{criteria['price_to']}/{car['make']}/{car['model']}/"
            f"?zip={criteria['postcode']}&startYear={criteria['year_from']}&endYear={criteria['year_to']}"
            f"&maxMileage={criteria['mileage']}&searchRadius={criteria['radius']}"
        )

        print(f"Scraping {car['make']} {car['model']} from URL: {url}")

        driver.get(url)
        driver.maximize_window()

        while True:
            page_source = driver.page_source
            content = BeautifulSoup(page_source, "html.parser")

            incremental_scroll(driver)

            # Find both normal and boosted articles
            normal_articles = content.findAll("div", attrs={"data-cmp": "inventoryListing"})
            boost_articles = content.findAll("div", attrs={"data-cmp": "boostInventoryListing"})
            spotlight_articles = content.findAll("div", attrs={"data-cmp": "inventorySpotlightListing"})

            all_articles = normal_articles + boost_articles + spotlight_articles

            print(f"Found {len(all_articles)} car listings on this page.")

            for article in all_articles:
                try:
                    # Check if the listing contains a promotional 'Dealer Logo' image
                    dealer_logo = article.find("img", alt="Dealer Logo")
                    if dealer_logo:
                        print("Skipping promotional listing with Dealer Logo.")
                        continue

                    name_tag = article.find("h2", class_="text-bold text-size-400 link-unstyled")
                    name = name_tag.text.strip() if name_tag else "No name available"
                    price_tag = article.find("div", class_="text-size-500 text-ultra-bold first-price")
                    price = price_tag.text.strip() if price_tag else "Price not available"
                    mileage_tag = article.find("div", class_="text-bold text-subdued-lighter margin-top-3")
                    mileage = mileage_tag.text.strip() if mileage_tag else "Mileage not available"
                    distance_tag = article.find("span", class_="text-normal")
                    distance = distance_tag.text.strip() if distance_tag else "Distance not available"
                    link_tag = article.find("a", href=True)
                    link = link_tag["href"] if link_tag else "No link available"

                    details = {"name": name, "price": price, "mileage": mileage, "distance": distance, "link": link}
                    data.append(details)

                    print(
                        f"Processed car: {name}, Price: {price}, Mileage: {mileage}, Distance: {distance}, Link: {link}")

                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue

            try:
                first_record += 25
                url = (
             f"https://www.autotrader.com/cars-for-sale/all/cars-between-{criteria['price_from']}-and-{criteria['price_to']}/"
            f"{car['make']}/{car['model']}/"
            f"?zip={criteria['postcode']}&startYear={criteria['year_from']}&endYear={criteria['year_to']}"
            f"&maxMileage={criteria['mileage']}&searchRadius={criteria['radius']}&firstRecord={first_record}"
            )
                driver.get(url)

            except Exception as e:
                print(f"Error finding or clicking next page button: {e}")
                break
    driver.quit()
    if not data:
        print("No data retrieved. The website may be down or there are no results.")
        return []
    return data

def FindCarsFromCars(criteria, cars):

    data = []
    driver = setup_google()

    for car in cars:
        url = (
            f"https://www.cars.com/shopping/results/?clean_title=true&dealer_id=&include_shippable=false"
            f"&keyword=&list_price_max={criteria['price_to']}&list_price_mihon={criteria['price_from']}"
            f"&makes[]={car['make']}&maximum_distance={criteria['radius']}&mileage_max={criteria['mileage']}"
            f"&models[]={car['make']}-{car['model']}&page_size=20&sort=best_match_desc&stock_type=all"
            f"&year_max={criteria['year_to']}&year_min={criteria['year_from']}&zip={criteria['postcode']}"
        )

        driver.get(url)
        driver.maximize_window()
        while True:
            # Scroll down to load more cars
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)

            # Extract page content
            page_source = driver.page_source
            content = BeautifulSoup(page_source, "html.parser")

            # Find all car listings
            all_articles = content.find_all("div", class_="vehicle-card")

            for article in all_articles:
                try:
                    # Extract car name
                    name_tag = article.find("h2", class_="title")
                    name = name_tag.text.strip() if name_tag else "No name available"

                    # Extract price
                    price_tag = article.find("span", class_="primary-price")
                    price = price_tag.text.strip() if price_tag else "Price not available"

                    # Extract mileage
                    mileage_tag = article.find("div", class_="mileage")
                    mileage = mileage_tag.text.strip() if mileage_tag else "Mileage not available"

                    # Extract distance
                    distance_tag = article.find("div", class_="miles-from")
                    distance = distance_tag.text.strip() if distance_tag else "Distance not available"

                    # Extract link
                    link_tag = article.find("a", class_="vehicle-card-link", href=True)
                    link = link_tag["href"] if link_tag else "No link available"

                    # Prepare the car details
                    details = {"name": name, "price": price, "mileage": mileage, "distance": distance, "link": link}
                    data.append(details)

                    # Print out the processed car details
                    print(f"Processed car: {name}, Price: {price}, Mileage: {mileage}, Distance: {distance}, Link: {link}")

                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue

            try:
                # Wait for the next button to be clickable
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'spark-button[aria-label="Next page"]'))
                )

                # Check if the button is disabled
                if next_button.get_attribute('disabled'):
                    print("No more pages.")
                    break
                else:
                    print("Moving to the next page...")
                    try:
                        # Execute JavaScript click if the normal click fails
                        driver.execute_script("arguments[0].click();", next_button)
                    except Exception as e:
                        print(f"JavaScript click failed, trying standard click: {e}")
                        next_button.click()

                    time.sleep(10)  # Wait for the next page to load

            except Exception as e:
                print(f"Error finding or clicking next page button: {e}")
                break

    driver.quit()
    carscom = True
    return data


def main():
    # Call the user input function and get the returned data
    user_inputs = get_user_input()

    # Prepare criteria for scraping
    criteria = {
        "postcode": user_inputs["zipcode"],  # Correct key
        "radius": user_inputs["radius"],
        "year_from": user_inputs["min_year"],
        "year_to": user_inputs["max_year"],
        "price_from": user_inputs["min_price"].replace('$', ''),  # Remove $ for numerical comparisons
        "price_to": user_inputs["max_price"].replace('$', ''),  # Remove $ for numerical comparisons
        "mileage": user_inputs["mileage"]
    }

    cars = [
        {
            "make": user_inputs["make"],
            "model": user_inputs["model"]
        }
    ]

    # Proceed with scraping
    data = FindCarsFromAutotrader(criteria, cars)
    autotrader = True
    od.output_data_to_excel(data, criteria, "autotrader")

    data2 = FindCarsFromCars(criteria, cars)
    carscom = True
    od.output_data_to_excel(data2, criteria, "cars")

if __name__ == "__main__":
    main()
