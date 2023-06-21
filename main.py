import time

from selenium import webdriver
from selenium.webdriver import Keys

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

service = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=service)
wait = WebDriverWait(driver, 10)


# Visit https://useinsider.com/ and check Insider home page is opened or not

driver.get("https://useinsider.com/")

driver.maximize_window()
link = driver.current_url

assert "useinsider.com" in link, "Not on expected page!"

# Select “More” menu in navigation bar, select “Careers” and check Career page,
# its Locations, Teams and Life at Insider blocks are opened or not

driver.find_element(By.ID, "wt-cli-accept-all-btn").click()

more = driver.find_element(By.XPATH, "/html/body/nav/div[2]/div/ul[1]/li[6]/a")
more.click()

career = driver.find_element(By.XPATH, "/html/body/nav/div[2]/div/ul[1]/li[6]/div/div[1]/div[3]/div/a")
career.click()

locations_section = wait.until(EC.presence_of_element_located(
    (By.XPATH, "//*[@id=\"career-our-location\"]/div/div/div/div[1]/h3")))

assert locations_section.is_displayed(), "locations section is not displayed!"

life_at_insider_section = wait.until(EC.presence_of_element_located(
    (By.XPATH, "/html/body/div[1]/div/div/section[4]/div/div/div/div/div/div[1]/div/h2")))

assert life_at_insider_section.is_displayed(), "life at insider section is not displayed!"

# Click “See All Teams”, select Quality Assurance, click “See all QA jobs”,
# filter jobs by Location - Istanbul, Turkey and department - Quality Assurance, check presence of jobs list

driver.get("https://useinsider.com/careers/quality-assurance/")
time.sleep(2)

see_all_qa_jobs_button = driver.find_element(By.CSS_SELECTOR,
                                    "#page-head > div > div > div.col-12.col-lg-7.order-2.order-lg-1 > div > div > a")
see_all_qa_jobs_button.click()

time.sleep(1)

filter_by_location_open_list = driver.find_element(By.XPATH,
                                    "/html/body/section[2]/div/div/div[2]/div/form/div[1]/span/span[1]/span/span[2]")
filter_by_location_open_list.click()

dropdown = driver.find_element(By.XPATH, '/html/body/span/span/span[2]/ul')
list_of_locations = dropdown.find_elements(By.TAG_NAME, "li")
desired_value = "Istanbul, Turkey"

for location in list_of_locations:
    if location.text == desired_value:
        location.click()
        break

# Check that all jobs’ Position contains “Quality Assurance”, Department contains
# “Quality Assurance”, Location contains “Istanbul, Turkey” and “Apply Now” button

jobs_list = driver.find_element(By.XPATH, "/html/body/section[3]/div/div/div[2]")
jobs_list_item = jobs_list.find_elements(By.TAG_NAME, "div")

job_list_xpath = "/html/body/section[3]/div/div/div[2]"

try:
    element = driver.find_element(By.XPATH, f"{job_list_xpath}/div[1]")
    jobs_exist = True
except Exception as ex:
    jobs_exist = False

assert jobs_exist, "Job listing could not be found!"

wait = WebDriverWait(driver, 10)

time.sleep(2)

element_department_job_list = driver.find_element(By.ID, "jobs-list")
position_list = element_department_job_list.find_elements(By.CLASS_NAME, "position-list-item")

# Click “Apply Now” button and check that this action redirects us to Lever Application form page

button = None

for position in position_list:
    department_position = position.find_element(By.CLASS_NAME, "position-department").get_attribute('innerText')
    location_position = position.find_element(By.CLASS_NAME, "position-location").get_attribute('innerText')
    if department_position == 'Quality Assurance' and location_position == 'Istanbul, Turkey':
        button = position.find_element(By.CLASS_NAME, "btn")
        break

assert button, "Button for Quality Assurance position could not be found!"

button.send_keys(Keys.ENTER)

driver.switch_to.window(driver.window_handles[1])

assert "jobs.lever.co/useinsider" in driver.current_url, "Not on expected page!"

apply_button = driver.find_element(By.XPATH,"/html/body/div[3]/div/div[1]/div/div[2]/a")
apply_button.send_keys(Keys.ENTER)

driver.close()
