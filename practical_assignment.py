from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from datetime import timedelta, date, datetime
from time import sleep

# Open airbnb webpage
driver = webdriver.Chrome(r'C:\Program Files\Google\Chrome\chromedriver_win32\chromedriver.exe')
driver.get('https://www.airbnb.com/')
driver.maximize_window()
action = webdriver.common.action_chains.ActionChains(driver)
driver.implicitly_wait(10)

class AirbnbTest():

    def click_on_anywhere(self, anywhere_btn):
        anywhere_btn.click()

    def checkstaysbtn(self, stays_btn):
        attribute_btn = stays_btn.get_attribute('aria-selected')
        if attribute_btn == 'true':
            return '\n"Stays" option is selected on the webpage.'
        else:
            stays_btn.click()
            return '\n"Stays" option is not selected.'

    def country_input(self, where_field):
        where_field.send_keys('Spain')

    def choose_county(self, select_country):
        select_country.click()

    def select_date(self, check_in_date):
        future_date = date.today() + timedelta(4)
        future_date = future_date.strftime('%m/%d/%Y')
        check_out_date = driver.find_element(By.XPATH, f'//td[contains(@aria-label,"Available")]/div[contains(@data-testid,"{future_date}")]')
        check_in_date.click()
        check_out_date.click()

    def getselected_interval(self, selected_dates):
        current_date = date.today()
        future_date = date.today() + timedelta(4)
        for dates in selected_dates:
            selected_info = dates.get_attribute("aria-label")
            selected_date = selected_info.split(', ')
            selected_date = selected_date[0] + ' ' + selected_date[2]
            selected_date = selected_date.split('.')[0]
            converted_date = datetime.strptime(selected_date, '%d %B %Y').date()
            if selected_dates.index(dates) == 0 and converted_date == current_date:
                print(f'The today\'s date: {converted_date} is selected')
            if selected_dates.index(dates) == 4 or selected_dates.index(dates) == 1 and converted_date == future_date:
                print(f'The today\'s date + 4 days: {converted_date} is selected')

    def previous_date_disabled(self, previous_date):
        check_disabled = previous_date.get_attribute('aria-disabled')
        if check_disabled == 'true':
            return '\nThe date before the interval is disabled.'
        else:
            return '\nThe date before the interval is enabled.'

    def flexible_option(self, flexible_btn):
        flexible_btn.click()

    def weekend_option(self, weekend_btn):
        weekend_btn.click()

    def any_weekend_option(self, any_weekend_section):
        assert any_weekend_section.text == 'Any weekend', "When section should state: Any weekend"

    def choose_dates_option(self, choose_dates_btn):
        choose_dates_btn.click()

    def search_option(self, search_btn):
        search_btn.click()

    def first_card_selection(self, first_card):
        hover = ActionChains(driver).move_to_element(first_card)
        hover.perform()

    def check_highlighted_price(self, card_price, map_price):
        card_price = card_price.get_attribute('innerHTML')
        card_price = card_price.split(";")[1]
        map_price = map_price.get_attribute('innerHTML').split(';')[1]
        if card_price == map_price:
            assert card_price == map_price, "The price is not hovered for the selected element"

    def price_tag(self, price_tag_button):
        price_tag_button.click()

    def check_listing_details(self, listing_name, listing_price, listing_rating):
        listing_name = listing_name.get_attribute('innerHTML')
        print(f'\nThe name of the location is: {listing_name}')

        listing_price = listing_price.get_attribute('innerHTML')
        corrected_price = listing_price.replace('&nbsp;', ' ')
        print(f'\nThe price of the location is: {corrected_price}')

        listing_rating = listing_rating.get_attribute('aria-label')
        listing_rating = listing_rating.split(', ')[0]
        print(f'\nThe rating is: {listing_rating}')

    def close_listing(self, close_btn):
        action.move_to_element(close_btn).perform()
        close_btn.click()

    def filters_section(self, filters_btn):
        filters_btn.click()

    def filters_options(self, entire_place, private_room, host_language):
        entire_place.click()
        private_room.click()
        action.move_to_element(host_language).perform()
        host_language.click()
        sleep(5)

    def show_stays_option(self, show_stays_btn):
        action.move_to_element(show_stays_btn)
        show_stays_btn.click()

    def number_of_applied_filters(self, applied_filters):
        applied_filters = applied_filters.get_property('innerHTML')
        applied_filters = int(applied_filters.split(' ')[1])
        if applied_filters == 3:
            return f'\nFilters status is correct: {applied_filters}'
        else:
            return f'\nFilters status is not correct: {applied_filters} instead of 3'

    def number_of_displayed_stays(self, header_displayed_stays):
        header_displayed_stays = header_displayed_stays.get_attribute('innerHTML')
        self.header_displayed_stays = int(header_displayed_stays.split(' ')[0])

    def gettotal_listed_stays(self):
        number_of_results = 0
        while True:
            next_page = driver.find_elements(By.XPATH, '//a[@aria-label="Next"]')
            results = driver.find_elements(By.XPATH, '//div[@class="c4mnd7m dir dir-ltr"]')
            number_of_results += len(results)
            if len(next_page) != 0:
                next_page_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
                next_page_btn.click()
            elif len(next_page) == 0:
                break

        if number_of_results == self.header_displayed_stays:
            return f'\nThe number of stays matches the listed stays - {number_of_results} '
        else:
            return f'\nThe number of stays does not match the listed stays - nr of stays= {self.header_displayed_stays} & listed stays = {number_of_results}:'


test = AirbnbTest()
test.click_on_anywhere(driver.find_element(By.XPATH, '//div[contains(text(),"Anywhere")]/parent::button'))
print(test.checkstaysbtn(driver.find_element(By.XPATH, '//span[contains(text(),"Stays")]/../parent::button')))
test.country_input(driver.find_element(By.XPATH, '//div[contains(text(),"Where")][1]/following-sibling::input'))
test.choose_county(driver.find_element(By.XPATH, '//div[text()="Spain"][1]/ancestor-or-self::div[@role="option"]'))
test.select_date(driver.find_element(By.XPATH, '//td[contains(@aria-label,"Today")]'))
test.getselected_interval(driver.find_elements(By.XPATH, '//td[contains(@aria-label, "Selected")]'))
print(test.previous_date_disabled(driver.find_element(By.XPATH, '//td[contains(@aria-label,"Today")]/preceding::td[1]')))
test.flexible_option(driver.find_element(By.XPATH, '//button[contains(text(),"I\'m flexible")]'))
test.weekend_option(driver.find_element(By.XPATH, '//div[contains(text(),"Stay for a") and contains(.,"week")] /following-sibling::div[1]//button[text()="Weekend"]'))
test.any_weekend_option(driver.find_element(By.XPATH, '//div[text()="When"]/following-sibling::div[1]'))
test.choose_dates_option(driver.find_element(By.XPATH, '//button[text()="Choose dates"]'))
test.getselected_interval(driver.find_elements(By.XPATH, '//td[contains(@aria-label, "Selected")]'))
test.search_option(driver.find_element(By.XPATH, '//button[@data-testid="structured-search-input-search-button"]'))
test.first_card_selection(driver.find_element(By.XPATH, '//div[@itemprop="itemListElement"]//a[1]'))
test.check_highlighted_price(card_price=driver.find_element(By.XPATH, '//div[@itemprop="itemListElement"]//a[1]/following-sibling::div[2]//span[contains(text(),"lei")][1]'), map_price=driver.find_element(By.XPATH, '//span[contains(text(),"selected")]/preceding::span[1]'))
test.price_tag(driver.find_element(By.XPATH, '//span[contains(text(),"selected")]/ancestor-or-self::button[1]'))
test.check_listing_details(listing_name=driver.find_element(By.XPATH, '//div[@class="gkzpgws cb4nyux dir dir-ltr"]/div[1]'), listing_price=driver.find_element(By.XPATH, '//div[@class="gkzpgws cb4nyux dir dir-ltr"]/div[3]//span[contains(text(),"lei")]'), listing_rating=driver.find_element(By.XPATH, '//div[@class="gkzpgws cb4nyux dir dir-ltr"]/div[3]/following-sibling::span[1]'))
test.close_listing(driver.find_element(By.XPATH, '//div[@class="gkzpgws cb4nyux dir dir-ltr"]//preceding::button[contains(@aria-label,"Close")][1]'))
test.filters_section(driver.find_element(By.XPATH, '//span[text()="Filters"]/ancestor-or-self::button[1]'))
test.filters_options(entire_place=driver.find_element(By.NAME, 'Entire place'), private_room=driver.find_element(By.NAME, 'Private room'), host_language=driver.find_element(By.NAME, 'Japanese'))
test.show_stays_option(driver.find_element(By.XPATH, '//a[contains(text(),"Show") and contains(text(),"stays")]'))
print(test.number_of_applied_filters(driver.find_element(By.XPATH, '//span[contains(text(),"Filters")]/following-sibling::span[contains(.,"filters")][1]')))
test.number_of_displayed_stays(driver.find_element(By.XPATH, '//h1[contains(.,"stays")]/span[1]'))
print(test.gettotal_listed_stays())
