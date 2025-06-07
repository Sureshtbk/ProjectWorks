from bs4 import BeautifulSoup
import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import pandas as pd
import re
import os
import mysql.connector as db
import numpy as np

# Write list of dictionaries to a CSV file 
def write_csv(items, path):
        with open(path, 'w') as f:
            if len(items) == 0:
                return
            # Extract headers from first dict
            headers = ','.join(list(items[0].keys()))
            f.write(headers + '\n')
            
            for item in items:
                values = []
                for value in item.values():
                    # Convert all values to string
                    values.append(str(value))
                f.write(','.join(values) + '\n')
                
# Merge all CSV files in the current directory
def csv_data_merge():
        dataframes = []
        # Get current working directory
        current_folder = os.getcwd()
        for file_name in os.listdir(current_folder):
            # Check for CSV files
            if file_name.endswith(".csv"):
                # Get full path
                file_path = os.path.join(current_folder, file_name)
            # with open (file_path, "r") as rfile:
                #    csv_data = rfile.read()
                #    dataframes.append(csv_data)
                df = pd.read_csv(file_path, encoding="ISO-8859-1")
                dataframes.append(df)
        # Merge all dataframes
        merged_df = pd.concat(dataframes)
        #Remove duplicates based on movie title column
        unique_df = merged_df.drop_duplicates(subset='Title')    
        # Reset index    
        unique_df.reset_index(drop=True, inplace=True)
        print("Total unique movies:", len(unique_df))
        unique_df = unique_df.sort_values(by=["Rating"], ascending=False)
        unique_df = unique_df.sort_values(by=["Votes"], ascending=False)
       
            
        return unique_df

# Connect to MySQL DB and insert data
def db_connection(dataframes):
        db_con = db.connect(
            host = "localhost",
            user = 'root',
            password = "Test#123#",
            database = "imdb"
        )
        # Create cursor
        curr = db_con.cursor()
        # Disable safe updates
        curr.execute("SET SQL_SAFE_UPDATES = 0;")
        # delete existing data
        delqry = """DELETE FROM imdb_genre_2024;"""    
        curr.execute(delqry)    
        # Re-enable safe updates
        curr.execute("SET SQL_SAFE_UPDATES = 1;")
        # Commit deletion
        db_con.commit()
        insert = """insert into imdb_genre_2024 (moviename, genre, rating, votes, duration) values (%s, %s, %s, %s, %s) """
        # Bulk insert
        curr.executemany(insert, list(map(tuple, dataframes.values)))
        db_con.commit()
        time.sleep(20)
        print("delete function calling")
        q1 = """SELECT * FROM imdb_genre_2024"""
        
        curr.execute(q1)
        # Get data from cursor
        data = curr.fetchall()
        #print(db_data.isnull().sum())
        #if data:
            #columns_name = ["Title", "Genre", "Rating", "Votes", "Duration"]
            #data = pd.DataFrame(data, columns=columns_name)

        #data['Votes'] = data['Votes'].astype(int)

        #data['Duration'] = data['Duration'].apply(convert_duration_mins)
        #print(db_data)
        #print(db_data.info())
        #print(db_data.isnull().sum())
        #print(db_data['rating'].mean())
        #data['Rating'] = data['Rating'].fillna(round(data['Rating'].mean()))
        #print(db_data.isnull().sum())
        #print(db_data)
        #print(data)
        return data
    #Main Function
    
# Calculate mean value grouped by specific column
def find_mean(data,group_value,col_name):
    chart_data = data.groupby(group_value)[col_name].mean().reset_index().sort_values(by=col_name, ascending=False)   
    return chart_data

# Main function to start scraping
def imdb_scraper_main():
    print("Main Function Start")
    page_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
    # read html tag by using class
    find_tag = 'sc-11de333b-0 bkthLW'
    # open page and read the genre tag
    get_genre_tag_info = open_page(page_url,find_tag)
    
    genre_lists = driver.find_elements("xpath","//div[contains(@id, 'accordion-item-genreAccordion')]")
        #looping Genre list     
        
        #films_data = []
        
    #hided for Dashboard page repeat to do the process Ganesh
    
   # for genre_detail in genre_lists:
    #                 click_specific_genre = genre_detail.find_elements(By.TAG_NAME, "button")                 
    #                 for genre in click_specific_genre:
    #                      genre_name = get_genre_details(genre)
                          #films_data = get_movie_details(genre_name)
                          #write_csv(films_data,f"{genre_name}.csv")
                          
    # call CSV file merge function
    data = csv_data_merge()
    # call db function ang get details
    Merged_movie_data = db_connection(data) 
    #print("Main Function End")

    return Merged_movie_data

#Read and get Genre details item by item
def get_genre_details(get_genre_info):
        #print("Genre Function Start")
        try:
            # since we can directly get the hided tag values so we hidden this for loop and if condition
            #for find_genre in get_genre_info:
                # Check if it is Genre then click the link
            #   if "Genre" in genre.get_attribute("innerHTML"):         
            #      time.sleep(2)
                    #find and click the Genre link
                #    driver.execute_script("arguments[0].scrollIntoView(true);", find_genre)            
            #     driver.execute_script("arguments[0].click();", find_genre)
                #    print('sak1')
                    #Read and get all Genre list     
                #    genre_lists = driver.find_elements("xpath","//div[contains(@id, 'accordion-item-genreAccordion')]")
                    #looping Genre list since we can get hidden details so we hide these
                #    for genre_detail in genre_lists:
                #        click_specific_genre = genre_detail.find_elements(By.TAG_NAME, "button")                 
                #        for index, genre in enumerate(click_specific_genre):
                            # Find the parent span with class ipc-chip__text
                            
                            # Print the full HTML content of the genre element
                            print(get_genre_info.get_attribute("innerHTML"))
                            # Find the parent span element containing the genre text
                            parent_span = get_genre_info.find_element(By.XPATH, ".//span[contains(@class, 'ipc-chip__text')]")

                            # Find the child span with count
                            count_span = parent_span.find_element(By.XPATH, "./span[contains(@class, 'ipc-chip__count')]")
                            genre_text = parent_span.get_attribute("textContent")             
                            genre_count = count_span.get_attribute("textContent")  
                            genre_name = genre_text.replace(genre_count, '').strip()
                            #print("Genre:", genre_name)
                            #print("Count:", genre_count)
                            total_movie_Count = re.sub(r'[^0-9.]', '', genre_count)
                            #print(total_movie_Count)
                            movie_Count = int(round(float(total_movie_Count), 0))
                            #print(movie_Count)
                            # if condition is testing purpose
                            #if "War" in genre_name or "Western" in genre_name:
                            
                            # Only proceed if the movie count is more than 0
                            if int(movie_Count) > 0:                            
                                #print('sakthi')
                                time.sleep(2)
                                # Scroll to the genre element and click it
                                driver.execute_script("arguments[0].scrollIntoView(true);", get_genre_info)
                                driver.execute_script("arguments[0].click();", get_genre_info)    
                                #wait.until(EC.element_to_be_clickable(genre))
                                page_info = wait.until(
                                            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'dPzhgh')]"))
                                )
                            
                                # Check if CSV already exists for this genre
                                if not os.path.exists(f"{genre_name}.csv"):
                                    click_more_button("//button[contains(@class,'ipc-see-more__button')]")
                                    time.sleep(5)
                                    
                                    # Write data to CSV if available
                                    films_data = get_movie_details(genre_name)
                                    if films_data:                                
                                            write_csv(films_data,f"{genre_name}.csv")
                                    else:
                                        print("No data for writing CSV")
                                    # Click genre again to collapse panel
                                    driver.execute_script("arguments[0].scrollIntoView(true);", get_genre_info)
                                    driver.execute_script("arguments[0].click();", get_genre_info)    
                                else:
                                    print(f"No data for this genre:{genre_name}") 
                                    driver.execute_script("arguments[0].scrollIntoView(true);", get_genre_info)
                                    driver.execute_script("arguments[0].click();", get_genre_info)  
                
        except Exception as ex:
            print (ex)
            
        return genre_name
        #print("Genre Function end")

def get_movie_details(genre_name):
        try:
            films_data = []
            print("movie details start")
            get_movie_ul = driver.find_elements("xpath","//ul[contains(@class, 'ipc-metadata-list')]") 
            #get_movie_li = driver.find_elements(By.XPATH, "//li[contains(@class, 'ipc-metadata-list-summary-item')]")
            get_movie_li = driver.find_elements(By.XPATH, "//li[contains(@class, 'ipc-metadata-list-summary-item')]")
            #movie_names = [movie_details.text.split('\n')[0] for movie_details in get_movie_li]  # First line is usually title

            for get_movie_inf in get_movie_li:
                                print('siv')
                                try:
                                    movieName = get_movie_inf.find_element(By.XPATH, ".//h3").text.split('.')
                                    movie_with_rank = get_movie_inf.find_element(By.XPATH, ".//h3").text.strip()
                                    movie_name = movie_with_rank.split('.', 1)[1].strip() if '.' in movie_with_rank else movie_with_rank
                                    # Clean commas to avoid Excel misalignment
                                    movie_name = movie_name.replace(',', '')

                                    
                                except:
                                    movie_name = "N/A"
                                    
                                try:
                                    movie_rating = get_movie_inf.find_element(By.XPATH, ".//span[contains(@class, 'ipc-rating-star--rating')]").text 
                                                                
                                except:
                                    movie_rating = "N/A"
                                
                                try:
                                    movie_voting = get_movie_inf.find_element(By.XPATH, ".//span[contains(@class, 'ipc-rating-star--voteCount')]").text
                                    #movie_voting = re.sub(r'[^\w\s]', '', movie_voting)  
                                    print(movie_voting)
                                    voting_count = movie_voting.strip().lower().replace(',', '').replace('(','')
                                    voting_count = voting_count.replace(')','')
                                    print(voting_count)
                                    if 'k' in voting_count:
                                        voting_count = int(float(voting_count.replace('k','')) * 1000)
                                        print(voting_count)                                                            
                                except:
                                    movie_voting = "N/A"
                                    
                                try:
                                    movie_duration = get_movie_inf.find_element(By.XPATH, ".//span[contains(@class, 'dli-title-metadata-item')][2]").text                               
                                except:
                                    movie_duration = "N/A"
                                
                                films_data.append(
                                {
                                "Title": movie_name,
                                "Genre": genre_name,
                                "Rating": movie_rating,
                                "Votes": voting_count,
                                "Duration": movie_duration,                            
                                }
                                )    
                                # Print all movie names
            #print(movie_names)  
            print("movie details end")
            return films_data
        except Exception as ex:
            print(ex)
    #click 50 more page navigation link until the full items are loaded
def click_more_button(get_clickable_tag_info):
        try:
            while True:
                                    try:
                                        # Wait until the button is present
                                        load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"{get_clickable_tag_info}")))
                                        
                                        print("Clicking 'Load 50 more' button...")
                                        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.90);", load_more_button)
                                        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", load_more_button)
                                        time.sleep(1)  # Optional small delay
                                        load_more_button.click()
                                        
                                        # Wait for content to load
                                        time.sleep(3)

                                    except (TimeoutException, NoSuchElementException):
                                        print("No more 'Load 50 more' button found.")
                                        break
                                    except ElementClickInterceptedException:
                                        print("Click intercepted, retrying...")
                                        time.sleep(2)
                                    print("All data loaded.") 
        except Exception as ex:
            print (ex)
                                    
    #Initialize chrome driver and open web page.
def open_page(page_url,find_tag):
        print("OpenPage Function Start")
        
        #driver  
        try:
            
            driver.get(page_url)
            driver.maximize_window()
        
            #Read all left-side Accordion menu details
            find_genre_tag = driver.find_elements(By.XPATH,f"//div[contains(@class, '{find_tag}')]")
            #films_data = []
            return find_genre_tag
        except Exception as ex:
            print(ex)
            
        print("OpenPage Function End")

# Initialize browser and wait logic       
options = Options()
options.add_experimental_option("detach",True)
# Create driver and wait object
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
wait = WebDriverWait(driver, 10)
# Trigger the main function
imdb_scraper_main()



