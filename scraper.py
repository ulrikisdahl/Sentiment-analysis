#Webste: tripadvisor
#For each resturaunt, find the rating with the lowest amounts and have that as a max number for each rating from that restaurant


import csv
import string
import math
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


class store_info():
    def __init__(self, rating, text_reviews):
        self.rating = rating
        self.text_reviews = text_reviews


class scraper:
    def __init__(self):
        self.arr = []

    def page(self, name):
        count = 1 #the nr of the current restaurant we are scraping in a list of 10 restaurants
        url = ''
        
        options = Options()
        options.headless = False #headless = True removes the visuals
        options.add_experimental_option('detach', True) #makes it so the browser does not close down afterwords, so that we can inspect

        browser = webdriver.Chrome(ChromeDriverManager().install()) #webdrivermanager finds the right verion of chrome for the webdriver
        browser.get(url)

        num_links =  9#len(browser.find_elements_by_class_name("_15_ydu6b")) #The amount of links to restaurants
        i=0
        while True:
            try: #Wrap the code in the page function in a try-except statement becuase some restaurant articles will fail, and we dont want that to stop the whole scrape
                print("COUNT: ", count)
                if count>num_links:
                    break
                
                #get links to each restaurant
                xpath_link = f'//*[@id="component_46"]/div/div[1]/div[2]/div[{count}]/div/div[2]/a[1]'
                            #//*[@id="component_2"]/div/div[2]/span/div[1]/div[2]/div[2]/div/div[1]/span[1]/span/span/a/span[2]
                link = browser.find_element_by_xpath(xpath_link)
                link.click()

                #finding the total amount of reviews on the restaurant page and converting it to an integer
                total_reviews = browser.find_element_by_class_name('_3Wub8auF')
                reviews_int = self.string_to_int(total_reviews, '<')
                print(reviews_int)
                
                #Checking if the restaurant has enough reviews to scrape
                if reviews_int > 500:
                    #collecting the amount of different types of ratings so that we can find the lowest
                    lowest_n_rating = self.lowest_n_rating(browser)
                    if lowest_n_rating < 1:
                        count +=1
                        browser.get(url)
                        break

                    #Find all the rating-links/checkboxes and click them one by one in order to get the reviews of that rating
                    for i in range(1, 6):
                        #un-checking the previous checkbox
                        if i > 1:
                            time.sleep(2)
                            x_path_uncheck = f'//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[{i - 1}]/label'
                            uncheck = browser.find_element_by_xpath(x_path_uncheck)
                            uncheck.click()
                        #Clicking checkbox
                        time.sleep(2)
                        x_path = f'//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[{i}]/label'
                        checkbox = browser.find_element_by_xpath(x_path)
                        checkbox.click()

                        #scraping the text
                        self.press_more_button(browser)
                        time.sleep(2)
                        self.scrape_review_texts(browser, i)

                        #Next button
                        #n_next_buttons_pressed represents how many iterations we have in the foor-loop that will press the next button
                        n_next_buttons_pressed = int(math.floor(lowest_n_rating/10) - 1) if lowest_n_rating % 10 != 0 else int(lowest_n_rating/10 - 1)
                        if n_next_buttons_pressed < 0:
                            n_next_buttons_pressed = 0

                        for _ in range(n_next_buttons_pressed):
                            print("Current B: ", _)
                            next_button = browser.find_element_by_class_name('next')
                            next_button.click()
                            self.press_more_button(browser)
                            time.sleep(2)
                            self.scrape_review_texts(browser, i)
                            browser.execute_script('window.scrollTo(2800, 1400)')

                #final part per itr
                count +=1
                browser.get(url)
                
                #removing a pop-up
                self.remove_popup(browser)
                
            except:
                print("exception")

                if count>num_links:
                    break

                count += 1
                browser.get(url)
                self.remove_popup(browser)

        browser.close()

        return self.arr



    def string_to_int(self, string_1, split_by):
        string_1 = string_1.get_attribute('innerHTML').split(split_by)[0]
        table = str.maketrans('', '', string.punctuation)
        integer = int(string_1.translate(table))
        return integer

    def lowest_n_rating(self, browser):
        n_excellent_rating_xpath = '//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[1]/span[2]'
        n_very_good_rating_xpath = '//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[2]/span[2]'
        n_average_rating_xpath = '//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[3]/span[2]'
        n_poor_rating_xpath = '//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[4]/span[2]'
        n_terrible_rating_xpath = '//*[@id="taplc_detail_filters_rr_resp_0"]/div/div[1]/div/div[2]/div[1]/div/div[2]/div/div[5]/span[2]'
        
        n_excellent_rating = self.string_to_int(browser.find_element_by_xpath(n_excellent_rating_xpath), ' ')
        n_very_good_rating = self.string_to_int(browser.find_element_by_xpath(n_very_good_rating_xpath), ' ')
        n_average_rating = self.string_to_int(browser.find_element_by_xpath(n_average_rating_xpath), ' ')
        n_poor_rating = self.string_to_int(browser.find_element_by_xpath(n_poor_rating_xpath), ' ')
        n_terrible_rating = self.string_to_int(browser.find_element_by_xpath(n_terrible_rating_xpath), ' ')

        return min(n_excellent_rating, n_very_good_rating, n_average_rating, n_poor_rating, n_terrible_rating)

    def scrape_review_texts(self, browser, rating):
        for j in range(4, 11):
            review_texts_xpath = f'/html/body/div[2]/div[2]/div[2]/div[6]/div/div[1]/div[4]/div/div[5]/div/div[{j}]/div[3]/div/div/div/div[2]/div[2]/div/p'
            review_texts = browser.find_element_by_xpath(review_texts_xpath).get_attribute('innerHTML')
            info = store_info(rating, review_texts)
            self.arr.append(info) 
        return self.arr

    def press_more_button(self, browser): #Presses the more button on the review so that the rest of the review loads
        time.sleep(1)
        try:
            more_button = browser.find_elements_by_class_name('ulBlueLinks')[0]
            more_button.click()
        except:
            print("No more-button")

    def remove_popup(self, browser): #Removes pop-ups that would otherwise be in the way of the browser
        time.sleep(1.5)
        pop_up_xpath = '_3VKU_-kL'
        try:
            remove_pop_up = browser.find_element_by_class_name(pop_up_xpath)
            remove_pop_up.click()
        except:
            print("no pop-up")


#Function that removes the "<elements>" that are a part of the scraped text
def clean_text(text):
    cleaned_text = ''
    for x in text.split('<'):
        uncleaned_text = x.split('>')
        if len(uncleaned_text) > 1:
            cleaned_text += uncleaned_text[1]
        else:
            cleaned_text += uncleaned_text[0]
    return cleaned_text 


bot = scraper()
reviews = bot.page('name')

#Adding the reviews and labels to the csv file
with open('review-sentiments.csv', 'a', newline='', encoding='utf-8') as csvfile: 
    review_text_writer = csv.writer(csvfile, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for review_text in reviews:
        review_text_writer.writerow([review_text.rating, clean_text(review_text.text_reviews)])

 
           
