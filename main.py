from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import csv
import time
import os

# initial browser setup
options = Options()
options.headless = True
driver = Firefox(options=options,
                 executable_path=r'/home/stefke/Desktop/sidehusssle/polovni_scrapper/driver/geckodriver')

pages_golf = 7
pages_plus = 3

# process dependencies
fileName = 'all_cars_id.csv'
seenCarsIds = list()
carsIds = list()

# counters
new_cars_amount = 0
old_cars_amount = 0
errors = 0

def load_seen_list():
    with open(fileName) as file_cars:
        reader_cars = csv.reader(file_cars, delimiter=",")
        for row in reader_cars:
            seenCarsIds.append(row[0])


def bookmark_seen_cars(seen_car):
    with open(fileName, 'a', newline='') as output:
        writer = csv.writer(output)
        writer.writerow([seen_car])


def process_golf_plus():
    # access global counts and lists
    global new_cars_amount
    global old_cars_amount
    global errors
    global seenCarsIds
    global carsIds

    # iterate 10 pages get all results and notify if any new
    for page in range(1, pages_plus):
        url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?page=" + str(
            page) + "&sort=basic&brand=volkswagen&model%5B1%5D=golf-plus&city=Subotica%7C46.097281%7C19.669620&city_distance=75&showOldNew=all&without_price=1"

        # fetch data from the website
        driver.get(url)

        # count items present
        for item in driver.find_elements_by_class_name('single-classified'):
            if item.get_attribute('data-classifiedid') is None or item.get_attribute(
                    'data-price') is None or item.find_element_by_class_name(
                'ga-title') is None or item.find_element_by_class_name('ga-title') is None:
                errors += 1
                continue
            elif item.get_attribute('data-price') == 'Po dogovoru':
                errors += 1
                continue
            else:
                # fetch all relevant data i need
                ad_id = item.get_attribute('data-classifiedid')
                ad_price = int(item.get_attribute('data-price').replace('€', '').replace('.', '').strip())
                ad_title = item.find_element_by_class_name('ga-title').get_attribute('title')
                ad_link = item.find_element_by_class_name('ga-title').get_attribute('href')

                # if ad was not seen by me yet (new) yell found and output to csv
                if ad_id not in seenCarsIds and ad_price < 3500:
                    new_cars_amount += 1

                    print('Bingo! ===> ' + str(ad_id) + " ==> " + str(ad_title) + " ==> " + str(ad_price))

                    # ad the new car to the list, now seen
                    bookmark_seen_cars(ad_id)

                    # write the full details to the csv file, for further inspection
                    with open('new_cars.csv', 'a', newline='') as new_cars_output:
                        writer_new_cars = csv.writer(new_cars_output)
                        writer_new_cars.writerow(
                            [ad_id, ad_title, ad_price, ad_link])
                else:
                    old_cars_amount += 1

def process_golf_5():
    # access global counts and lists
    global new_cars_amount
    global old_cars_amount
    global errors
    global seenCarsIds
    global carsIds

    # iterate 10 pages get all results and notify if any new
    for page in range(1, pages_golf):
        url = "https://www.polovniautomobili.com/auto-oglasi/pretraga?page=" + str(
            page) + "&sort=basic&brand=volkswagen&model%5B0%5D=golf-5&city=Subotica%7C46.097281%7C19.669620&city_distance=75&showOldNew=all&without_price=1"

        # fetch data from the website
        driver.get(url)

        # count items present
        for item in driver.find_elements_by_class_name('single-classified'):
            if item.get_attribute('data-classifiedid') is None or item.get_attribute(
                    'data-price') is None or item.find_element_by_class_name(
                'ga-title') is None or item.find_element_by_class_name('ga-title') is None:
                errors += 1
                continue
            elif item.get_attribute('data-price') == 'Po dogovoru':
                errors += 1
                continue
            else:
                # fetch all relevant data i need
                ad_id = item.get_attribute('data-classifiedid')
                ad_price = int(item.get_attribute('data-price').replace('€', '').replace('.', '').strip())
                ad_title = item.find_element_by_class_name('ga-title').get_attribute('title')
                ad_link = item.find_element_by_class_name('ga-title').get_attribute('href')

                # if ad was not seen by me yet (new) yell found and output to csv
                if ad_id not in seenCarsIds and ad_price < 3500:
                    new_cars_amount += 1

                    print('Bingo! ===> ' + str(ad_id) + " ==> " + str(ad_title) + " ==> " + str(ad_price))

                    # ad the new car to the list, now seen
                    bookmark_seen_cars(ad_id)

                    # write the full details to the csv file, for further inspection
                    with open('new_cars.csv', 'a', newline='') as new_cars_output:
                        writer_new_cars = csv.writer(new_cars_output)
                        writer_new_cars.writerow(
                            [ad_id, ad_title, ad_price, ad_link])
                else:
                    old_cars_amount += 1


if __name__ == '__main__':
    # global new_cars_amount
    # global old_cars_amount
    # global errors

    start_time = time.time()
    while True:
        # clear previous results
        os.system('cls' if os.name == 'nt' else 'clear')

        # clear previous results
        new_cars_amount = 0
        old_cars_amount = 0
        errors = 0

        print("==== Lets load the seen cars first ====" + '\n \n')
        load_seen_list()

        print("==== Starting golf 5 scrapper ... ====" + '\n \n')
        process_golf_5()

        print("==== Starting golf plus scrapper ... ====" + '\n \n')
        process_golf_plus()

        print("==== found cars => " + str(new_cars_amount) + " errors => " + str(errors) + '\n \n')
        print("==== See you in the next run i do ====")


        time.sleep(1200 - ((time.time() - start_time) % 1200))
