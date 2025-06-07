import streamlit as st
import pandas as pd
from main import imdb_scraper_main,find_mean
import matplotlib.pyplot as plt
import glob
import seaborn as sns
from scipy import stats

# Function to convert duration string to total minutes
def convert_duration_mins(data):
    #if 'h' in data:
    # Handle None, NaN, or empty string
    if not isinstance(data, str) or data.strip() == '':
        return 0 
    # Remove extra spaces
    data = data.replace(' ', '').strip()
    
    # Extract hours
    duration_hrs = int(data.split('h')[0]) if 'h' in data else 0
    # Extract minutes after hours
    duration_mins = 0
    if 'h' in data and 'm' in data:
        duration_mins = int(data.split('h')[1].split('m')[0])
    elif 'm' in data:
        # Extract only minutes if no hours
        duration_mins = int(data.split('m')[0])
    #convert duration to mins and add mins   
    tot_mins = duration_hrs * 60 + duration_mins
    return tot_mins

# Call function to load scraped movie data
data = imdb_scraper_main()
if len(data) > 0:
    # Define expected columns
    columns_name = ["Title", "Genre", "Rating", "Votes", "Duration"]
    # Create DataFrame
    data = pd.DataFrame(data, columns=columns_name)
    # Convert votes to integer
    data['Votes'] = data['Votes'].astype(int)
   
    # Convert duration
    data['Duration'] = data['Duration'].apply(convert_duration_mins)
    # Fill missing ratings
    data['Rating'] = data['Rating'].fillna(round(data['Rating'].mean()))
    
    
# --- Header ---
st.markdown("""
    <h1 style='text-align: center; background-color: #222; color: white; padding: 1rem;'>
        IMDB 2024 Data Scraping and Visualizations
    </h1>
""", unsafe_allow_html=True)
if st.button("🔄 Refresh"):
    st.rerun()
# --- Sidebar Navigation ---
st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Home", "Top 10", "Genres", "Average Duration by Genre","Voting Trends by Genre","Rating Distribution","Genre-Based Rating Leaders","Most Popular Genres by Voting","Duration Extremes","Ratings by Genre","Correlation Analysis"])

# --- Page content rendering based on selected navigation ---
if page == "Home":
    st.write("Welcome to the IMDb Movie Explorer!")
    # Convert minutes to hours ranges
    def duration_category(minutes):
        if minutes < 120:
            return '< 2 hrs'
        elif 120 <= minutes <= 180:
            return '2–3 hrs'
        else:
            return '> 3 hrs'

    print(data)
    print(data['Duration'])
    # Apply category labels
    data['DurationCategory'] = data['Duration'].apply(duration_category)

     # Sidebar filters
    st.sidebar.title("Interactive Filtering Functionality")

    # Get unique genres
    genre_options = sorted(data['Genre'].unique())
    selected_genre = st.sidebar.multiselect("Select Genre(s):", genre_options, default=genre_options)

    # Genre filter
    min_rating = st.sidebar.slider("Minimum IMDb Rating:", min_value=0.0, max_value=10.0, step=0.1, value=7.0)

    # Vote count filter
    min_votes = st.sidebar.number_input("Minimum Number of Votes:", min_value=0, value=100000)

    # Duration filter
    duration_options = ['< 2 hrs', '2–3 hrs', '> 3 hrs']
    selected_durations = st.sidebar.multiselect("Select Duration Range(s):", duration_options, default=duration_options)

    # Apply all selected filters to the dataset
    filtered = data[
    (data['Genre'].isin(selected_genre)) &
    (data['Rating'] >= min_rating) &
    (data['Votes'] >= min_votes) &
    (data['DurationCategory'].isin(selected_durations))
    ]
    # Show the filtered movies
    st.markdown("Filtered Movies:")
    st.dataframe(filtered[['Title', 'Genre', 'Rating', 'Votes', 'Duration']].reset_index())
#Top 10 movies based on Votes and Ratings
elif page == "Top 10":
    st.subheader("Top 10 Movies by Rating and Voting Counts")  
    # Filter high vote movies
    data = data[data['Votes'] > 100000]
    top_movies = data.sort_values(by=['Votes', 'Rating'], ascending=[False, False]).head(10)
    # Filter high vote movies
    st.write(top_movies)
#Genre-wise movie count
elif page == "Genres":
    st.subheader("Genre Distribution") 
    if 'Genre' in data.columns:         
        genre_value = data['Genre'].value_counts().reset_index()
        genre_value.columns = ['Genre', 'Count']
        plt.figure(figsize=(26,8))
        sns.barplot(data=genre_value,
                    x='Genre',
                    y='Count')
        st.pyplot(plt)
    else:
        st.error("⚠️ 'Genre' column not found in the dataset.")
#Bar chart of average duration by genre
elif page == "Average Duration by Genre":
     st.subheader("Average Duration by Genre")  
     #bar_chart = data.groupby(['Genre']).agg({"duration_mins":"mean"}).reset_index().sort_values("duration_mins", ascending=False)
     bar_chart = find_mean(data,'Genre','Duration')
     plt.figure(figsize=(16, 8))
     sns.barplot(data=bar_chart,
        x = "Duration",
        y = "Genre",
           palette='viridis')     
     st.pyplot(plt)
#Bar chart of average votes by genre
elif page == "Voting Trends by Genre":
     st.subheader("Voting Trends by Genre")   
     data['votes_in'] = data['Votes'].astype(int)
     voting_barchart = find_mean(data,'Genre','Votes')
     plt.figure(figsize=(21,8))
     sns.barplot(data=voting_barchart,
           x="Genre",
           y="Votes",
           palette='viridis')
     st.pyplot(plt)
# Boxplot for rating distribution
elif page == "Rating Distribution":
     st.subheader("Rating Distribution")   
     
     box_cox_values, lambda_ = stats.boxcox(data['Votes'])  # <-- only this line returns float
     data['Box_cox'] = box_cox_values

    # Show the data
     
     #st.write(data.head(10))
     #st.pyplot(plt.gcf())
     box, sts = stats.boxcox(data['Votes'])
     data['Box_cox'] = box
     sns.boxplot(data['Box_cox'])     
     st.pyplot(plt)
# Top-rated movies per genre
elif page == "Genre-Based Rating Leaders":
     st.subheader("Genre-Based Rating Leaders")   
     genre_based_rating = data.sort_values(by=['Genre', 'Rating'], ascending=[True, False])
     st.write(genre_based_rating)
# Pie chart of most voted genres
elif page == "Most Popular Genres by Voting":
     st.subheader("Most Popular Genres by Voting")   
     highest_voting = data.groupby('Genre').agg({'Votes': 'sum'}).reset_index().sort_values('Votes', ascending=False)
     plt.figure(figsize=(8,8))
     plt.pie(highest_voting['Votes'],labels=highest_voting['Genre'], autopct="%.2f%%")
     st.pyplot(plt)
# Shortest and longest movie display
elif page == "Duration Extremes":
     st.subheader("Duration Extremes")   
     longest_movie = data.loc[data['Duration'].idxmax()]
    
     shortest_movie = data[data['Duration'] > 0]
     shortest_movie = data.loc[shortest_movie['Duration'].idxmin()]

     minmax_movielist = pd.DataFrame([
    {
    "Type" : "Shortest movie",
    "Title" : shortest_movie['Title'],
    "Genre": shortest_movie['Genre'],
    "Rating": shortest_movie['Rating'],
    "Votes": shortest_movie['Votes'],
    "Duration in Mins" : shortest_movie['Duration']
    },
    {
    "Type" : "longest movie",
    "Title" : longest_movie['Title'],
    "Genre": longest_movie['Genre'],
    "Rating": longest_movie['Rating'],
    "Votes": longest_movie['Votes'],
    "Duration in Mins" : longest_movie['Duration']
    }
    ])
     st.write(minmax_movielist)
# Heatmap of average rating by genre    
elif page == "Ratings by Genre":
     st.subheader("Ratings by Genre")   
    
     avg_rating = data.groupby(['Genre']).agg({'Rating':'mean'}).reset_index().sort_values('Rating',ascending=False)
     heat_mapdata = avg_rating.pivot_table(index='Genre',values='Rating')
     plt.figure(figsize=(16,8))
     sns.heatmap(heat_mapdata,annot=True)
     st.pyplot(plt)
# Correlation plot between votes and rating    
elif page == "Correlation Analysis":
     st.subheader("Correlation Analysis")    
     plt.figure(figsize=(26,8))
     sns.scatterplot(data=data,x='Votes',y='Rating')   
     st.pyplot(plt)



# --- Footer ---
st.markdown("""
    <hr>
    <p style='text-align: center; font-size: 0.9em; color: gray;'>
        © 2025 IMDb Viewer · Built by Suresh using Streamlit
    </p>
""", unsafe_allow_html=True)
    

# Clear the cache    
st.cache_data.clear()


