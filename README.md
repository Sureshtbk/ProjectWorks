# IMDb 2024 Data Scraping and Visualizations

This project extracts, processes, and visualizes IMDb's 2024 feature film data. It provides genre-wise analysis, interactive filters, and graphical insights using **Selenium, Pandas, Streamlit, MySQL**, and **Matplotlib/Seaborn**.

## Table of Contents
- [Project Objective](#-project-objective)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [How to Run](#-how-to-run)
- [Features](#-features)
- [Dataset Overview](#-dataset-overview)
- [Code Highlights](#-code-highlights)
- [Deliverables](#-deliverables)

## Project Objective

To scrape IMDb 2024 movie data and build an interactive Streamlit dashboard that enables users to:
- Explore top-rated movies
- Analyze genre trends
- Understand duration and voting patterns
- Interactively filter movies by rating, genre, duration, and vote count


## Tech Stack

 Tool        - Usage                          
----------------------------------------------
 Python               - Core language                  
 Selenium             - Web scraping                   
 Pandas               - Data handling                  
 MySQL                - Data storage                   
 Streamlit            - Web app UI                     
 Matplotlib / Seaborn - Data visualization    


## Project Structure

```
├── Home.py                # Streamlit app UI and visualizations
├── main.py                # Web scraping, CSV management, DB storage
├── *.csv                  # Genre-wise scraped data
├── README.md              # This file
```

## How to Run

1. **Install requirements**  
  
   pip install selenium pandas streamlit seaborn matplotlib mysql-connector-python webdriver-manager
   

2. **Run Streamlit App**  
  
   streamlit run Home.py
  

3. **Ensure MySQL is running** and your DB config in `main.py` is valid.



## Features

- **Data Scraping** – Scrapes 2024 IMDb feature films by genre
- **CSV Export** – Stores genre-wise CSVs
- **SQL Storage** – Merges and stores all movie data in MySQL
- **Data Cleaning** – Converts durations, handles missing data
- **Top Movies Viewer** – Lists top 10 by rating & votes
- **Genre-wise Analysis** – Distribution, voting, duration stats
- **Interactive Filters** – Filter movies by genre, duration, rating, votes
- **Correlation & Heatmaps** – Rating-vote correlation and genre rating heatmap

---

## Dataset Overview

 Column Name  - Description                  
--------------------------------------------
 Title       - Movie Title                   
 Genre       - Genre (e.g., Action, Drama)   
 Rating      - IMDb Rating                   
 Votes       - Vote count                    
 Duration    - Duration (in minutes)         

---

## Code Highlights

- `get_genre_details()` - Extracts genre names and movie counts
- `get_movie_details()` - Scrapes movie info (title, rating, votes, duration)
- `write_csv()` - Stores movies by genre in individual CSV files
- `csv_data_merge()` - Merges all CSVs and removes duplicates
- `db_connection()` - Uploads data to MySQL and retrieves cleaned dataset
- `Home.py` - Full-featured Streamlit dashboard with page navigation, filtering, and plots

---

## Deliverables

- Genre-wise CSV files
- SQL table `imdb_genre_2024`
- Streamlit dashboard for data visualization
- Clean and modular Python code
- README and documentation
