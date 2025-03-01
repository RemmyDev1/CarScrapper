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
import undetected_chromedriver2 as uc
from ui import get_user_input
import os
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains




"copywritten by kariem hassan can be used for personal learning only code cannot be redistributed nor posted online without permission"
"can only share the code cannot claim code is yours thanks!"


scraper = cloudscraper.create_scraper()
# Declare global variables
autotrader = False
carscom = False
carvana = False
cargurus = False



def setup_google():
    chrome_options = webdriver.ChromeOptions()

    # Use Chrome user data to use an existing profile
    chrome_options.add_argument(f"--user-data-dir={os.path.expanduser('~')}/AppData/Local/Google/Chrome/User Data")

    # Detect and use any available profile
    user_data_dir = os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data'
    available_profiles = [f for f in os.listdir(user_data_dir) if f.startswith("Profile ")]

    if available_profiles:
        chrome_options.add_argument(f"--profile-directory={available_profiles[0]}")
    else:
        chrome_options.add_argument("--profile-directory=Default")

    # Other browser settings to bypass detection
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("user-agent=YOUR_USER_AGENT_STRING")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)

    # Apply Selenium Stealth to avoid bot detection
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )

    return driver


def refresh_page(driver, refresh_count, pause_time):
    """Refresh the page multiple times before starting to scrape."""
    for i in range(refresh_count):
        print(f"Refreshing page... {i+1}/{refresh_count}")
        driver.refresh()
        time.sleep(pause_time)

def incremental_scroll(driver, pause_time=3):
    """Scroll incrementally until the end of the page is reached."""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll to the bottom of window the page
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
    data = []
    driver = setup_google()
    for car in cars:
        url = (
            f"https://www.autotrader.com//cars-for-sale/all/{car['make']}/{car['model']}/"
            f"?zip={criteria['postcode']}&startYear={criteria['year_from']}&endYear={criteria['year_to']}"
            f"&priceRange={criteria['price_from']}-{criteria['price_to']}&maxMileage={criteria['mileage']}&searchRadius={criteria['radius']}&vehicleHistoryType=ONE_OWNER&vehicleHistoryType=CLEAN_TITLE&vehicleHistoryType=NO_ACCIDENTS"
        )

        print(f"Scraping {car['make']} {car['model']} from URL: {url}")

        driver.get(url)
        driver.maximize_window()
        refresh_page(driver, refresh_count=20, pause_time=0)
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
                    dealer_logo = article.find("img", alt="Dealer Logo")
                    if dealer_logo:
                        print("Skipping promotional listing with Dealer Logo.")
                        continue

                    # Check if it's a promotional carousel listing
                    carousel = article.find("div", class_="inventory-carousel")
                    if carousel:
                        print("Skipping promotional carousel listing.")
                        continue

                    # Handle listings without name or mileage information
                    name = article.find("h3", class_="text-bold text-size-400 link-unstyled")
                    if not name:
                        print("Skipping listing without a name.")
                        continue

                    mileage = article.find("div", class_="text-bold text-subdued-lighter margin-top-3")
                    if not mileage:
                        print("Skipping listing without mileage information.")
                        continue

                    distance = article.find("span", class_="text-normal")
                    if not distance:
                        distance = '0'
                    price = article.find("div", class_="text-size-600 text-ultra-bold first-price")
                    if not price:
                        price = '0'

                    name_tag = article.find("h3", class_="text-bold text-size-400 link-unstyled")
                    name = name_tag.text.strip() if name_tag else "No name available"
                    if price != '0':
                        price_tag = article.find("div", class_="text-size-600 text-ultra-bold first-price")
                        price = price_tag.text.strip() if price_tag else "Price not available"
                    mileage_tag = article.find("div", class_="text-bold text-subdued-lighter margin-top-3")
                    mileage = mileage_tag.text.strip() if mileage_tag else "Mileage not available"

                    if distance != '0':
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
            time.sleep(10)
            try:
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="Next Page"]')))
                if next_button.get_attribute('disabled'):
                    print("No more pages.")
                    break
                else:
                    print("Moving to the next page...")
                    try:
                        driver.execute_script("arguments[0].click();", next_button)
                    except Exception as e:
                        print(f"JavaScript click failed, trying standard click: {e}")
                        next_button.click()

                    time.sleep(random.uniform(5, 10))  # Random delay between page loads

            except Exception as e:
                print(f"Error finding or clicking next page button: {e}")
                break
    driver.quit()

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