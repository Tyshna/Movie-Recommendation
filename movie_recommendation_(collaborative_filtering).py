# -*- coding: utf-8 -*-
"""Movie Recommendation (collaborative filtering)
Automatically generated by Colab.
Original file is located at
    https://colab.research.google.com/drive/1NDsbfrf-sJDkMoRhyROBivnhAujIBGhO
# Movie Recommendation
**Problem Statement:**
- building an intelligent recommender that would recommend movies to a customer say **X** based on the customer's watch history.
- need to find other sets of users who have watched same movies along with some other movies and suggest customer **X** the movies which were appreciated by those set of users.
#### Datasets
**1. The `movie_metadata.csv` file:**
- This is the main Movies Metadata file.
- It contains information on 45,000 movies featured in the Full [MovieLens](https://movielens.org) database.
- Below are the features information:
  **Attribute Information:**
  ```
    adult: Indicates if the movie is X-Rated or Adult.
    belongs_to_collection: A stringified dictionary that gives information on the movie series the particular film belongs to.
    budget: The budget of the movie in dollars.
    genres: A stringified list of dictionaries that list out all the genres associated with the movie.
    homepage: The Official Homepage of the move.
    id: The TMDB ID of the movie.
    imdb_id: The IMDB ID of the movie.
    original_language: The language in which the movie was originally shot in.
    original_title: The original title of the movie.
    overview: A brief blurb of the movie.
    popularity: The Popularity Score assigned by TMDB.
    poster_path: The URL of the poster image.
    production_companies: A stringified list of production companies involved with the making of the movie.
    production_countries: A stringified list of countries where the movie was shot/produced in.
    release_date: Theatrical Release Date of the movie.
    revenue: The total revenue of the movie in dollars.
    runtime: The runtime of the movie in minutes.
    spoken_languages: A stringified list of spoken languages in the film.
    status: The status of the movie (Released, To Be Released, Announced, etc.)
    tagline: The tagline of the movie.
    title: The Official Title of the movie.
    video: Indicates if there is a video present of the movie with TMDB.
    vote_average: The average rating of the movie.
    vote_count: The number of votes by users, as counted by TMDB.
 ```
**2. The `links.csv` file:**
- This file contains the TMDB and IMDB IDs of all the movies featured in the Full MovieLens dataset.
- Below are the features information:
  ```
  movieId: A unique identifier for each movie
  imdbId: The IMDB ID of the movie
  tmdbId: The TMDB ID of the movie
  ```
**3. The `ratings_small.csv` file:**
- This file is a subset of 100,000 ratings from 700 users on 9,000 movies.
- Below are the features information:
  ```
  userId: The user ID of the subscriber
  movieId: A unique identifier for each movie
  rating: Rating given by a subscriber (Out of 5)
  timestamp: Time at which the rating was recorded
  ```
**Acknowledgement:** These datasets are an ensemble created by Rounak Banik using the data collected from TMDB and GroupLens.
**Dataset Source:** https://www.kaggle.com/rounakbanik/the-movies-dataset
Dataset link:** https://drive.google.com/uc?id=1rPR-P45M2UWsbXc8vpyCzWcQAYUfgVJX
"""
#importing required modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

#creating dataframe for movies
df = pd.read_csv('https://drive.google.com/uc?id=1rPR-P45M2UWsbXc8vpyCzWcQAYUfgVJX')

#data cleaning
#crating movies_df consisting of columnsid, imdb_id, title
movies_df = df[['id', 'imdb_id', 'title']]

#dropping missing values
movies_df.dropna(inplace = True)
movies_df['id'] = movies_df['id'].astype('float') #converting id to float

#dataframe for links
links_df = pd.read_csv('https://drive.google.com/uc?id=1Hn83CnGeHG6evq274ztIm6VcOrImBOAF')

#merging movies_df and links_df
m_links_df = pd.merge(movies_df, links_df, left_on ='id', right_on ='tmdbId')

#final DataFrame consisting of only movieId and title
m_df = m_links_df[['movieId', 'title']]

#dataframe for ratings
ratings_df = pd.read_csv('https://drive.google.com/uc?id=1DKT6CcjHsdKY9TKKAfk50ic2khf9JbJA')

#dropping timestamp from ratings_df
ratings_df = ratings_df.drop('timestamp', axis=1)

#merging m_df and ratings_df
final_movies_df = pd.merge(m_df, ratings_df, on = 'movieId')

#grouping the DataFrame by title & using mean() function to determine average rating.
final_movies_df.groupby('title')['rating'].mean()

#top 5 movies having highest mean rating.
final_movies_df.groupby('title')['rating'].mean().sort_values(ascending = False).head()

#countting the number of ratings given to each movie.
final_movies_df.groupby('title')['rating'].count()

#top 5 movies having highest count of ratings.
final_movies_df.groupby('title')['rating'].count().sort_values(ascending = False).head()

#creating a DataFrame with average rating and number of ratings for each movie.
all_movies_ratings = pd.DataFrame(final_movies_df.groupby('title')['rating'].mean())
all_movies_ratings['num of ratings'] = pd.DataFrame(final_movies_df.groupby('title')['rating'].count())

#creating a pivot table
user_ratings = final_movies_df.pivot_table(index ='userId', columns ='title', values ='rating')

#calculating correlation coefficient between each pair of movies
similarity_df = user_ratings.corr()

#creating a DataFrame containing the correlation coefficients of other movies with 'Toy Story'
similar_to_toystory = similarity_df["Toy Story"]
similar_to_toystory_df = pd.DataFrame(similar_to_toystory)

#renaming the column
similar_to_toystory_df.rename(columns={similar_to_toystory_df.columns[0]: 'correlation'}, inplace = True)

#sorting the above DataFrame by correlation to find top 10 highly correlated movies.
similar_to_toystory_df.sort_values('correlation',ascending=False).head(10)

#obtaining the number of ratings of each movie along with the correlation coefficients by joining 'all_movies_ratings['num of ratings']' DataFrame with the corr_toystory
corr_toystory = similar_to_toystory_df.join(all_movies_ratings['num of ratings'])

#keeping only those movies whose number of ratings are greater than 100.
#sorting them in descending order
corr_toystory[corr_toystory['num of ratings'] > 100].sort_values('correlation',ascending=False).head(10)

#recommend_movies()
def recommend_movies(movie_name):
  similar_movies = similarity_df[movie_name]
  similar_movies_df = pd.DataFrame(similar_movies)
  similar_movies_df.rename(columns = {similar_movies_df.columns[0]: 'correlation'}, inplace = True)
  corr_num_ratings = similar_movies_df.join(all_movies_ratings['num of ratings'])
  return corr_num_ratings[corr_num_ratings['num of ratings'] > 100].sort_values('correlation',ascending = False).head(10)

# Calling recommend_movies()w/ test input as: Star Wars
recommend_movies('Star Wars')

#predefined user watch history (random)
user_history = [
            {'title':'Hotel Transylvania 2', 'rating':4},
            {'title':"Indiana Jones and the Temple of Doom", 'rating':4.5},
            {'title':"Indiana Jones and the Kingdom of the Crystal Skull", 'rating':4},
            {'title':'Men in Black II', 'rating':4}
         ]
user_history_df = pd.DataFrame(user_history)
user_history_df

#obtaining the list of movie titles the user has watched
watch_list = user_history_df['title'].tolist()
watch_list

#obtaining a DataFrame consisting of movieId based on user watch history
user_history_id = m_links_df[m_links_df['title'].isin(watch_list)]
user_history_id

#obtaining the movieId and rating DataFrame for the user watch history
watched_movies_df = pd.merge(user_history_id, user_history_df)
watched_movies_df

#creating subset of users that has watched movies from the user watched movies dataframe
watch_list_movieid = watched_movies_df['movieId'].tolist()
users_subset_df = ratings_df[ratings_df['movieId'].isin(watch_list_movieid)]
print('Shape of the users_subset_df DataFrame: ',users_subset_df.shape)
users_subset_df.head(10)

#creating users subset group based on userId and sort on base of highest number of common movies watched
users_subset_group = users_subset_df.groupby(by='userId')
users_subset_group = sorted(users_subset_group, key=lambda a: len(a[1]), reverse=True)
users_subset_group

#dictionary to store the similarity scores of users subset with respect to target user X
from sklearn.metrics.pairwise import cosine_similarity
#empty dictionary
cosine_similarity_dict = {}

#iterating through individual users and the movie corresponding user has watched from the user subset group
for user, group in users_subset_group:
    #sorting the target user and current user group to prevent mismatch in movieId field
    group = group.sort_values(by='movieId')
    input_movies = watched_movies_df.sort_values(by='movieId')
    #rating for the movies that they both have in common
    temp_df = input_movies[input_movies['movieId'].isin(group['movieId'].tolist())]
    #temporary buffer list for similarity calculations
    temp_rating_list = temp_df['rating'].tolist()
    #corresponding user group rating in a temporary buffer list for similarity calculations
    temp_group_list = group['rating'].tolist()
    #similarity scores
    similarity = cosine_similarity([temp_rating_list], [temp_group_list])
    cosine_similarity_dict[user] = similarity.reshape(1)

#key value pairs of the similarity score dictionary
cosine_similarity_dict.items()

#DataFrame from the similarity score dictionary
cosine_similarity_df = pd.DataFrame.from_dict(cosine_similarity_dict, orient='index')
cosine_similarity_df.columns = ['similarity score']
cosine_similarity_df

#appending a column for userId and reset the index of the DataFrame
cosine_similarity_df['userId'] = cosine_similarity_df.index
cosine_similarity_df.reset_index(inplace=True)
cosine_similarity_df.head()

#new DataFrame for top users by sorting the users based on similarity scores
top_users = cosine_similarity_df.sort_values(by='similarity score', ascending=False)
top_users.head()

#final movies DataFrame
final_movies_df.head()

#obtaining the movies watched and ratings provided by users of top users DataFrame
top_users_rating = pd.merge(top_users, final_movies_df, on='userId', how='inner')
top_users_rating.head()

#weighted rating by combining the similarity score and movie rating for top users
top_users_rating['weighted rating'] = top_users_rating['similarity score']*top_users_rating['rating']
top_users_rating.head()

#cumulative similarity scores and weighted rating for similar movies
temp_top_users_rating = top_users_rating.groupby(by='movieId').sum()[['similarity score', 'weighted rating']]
temp_top_users_rating.columns = ['cumulative similarity score', 'cumulative weighted rating']
temp_top_users_rating.head()

#movies recommended from the cumulative ratings obtained from the top users
recommendation_df = temp_top_users_rating.copy()
recommendation_df['Id'] = recommendation_df.index
recommendation_df = recommendation_df.sort_values(by = 'cumulative weighted rating' , ascending=False)
recommendation_df.head(15)

# movie title for recommended movies
df = pd.merge(recommendation_df, m_links_df, left_on='Id', right_on='movieId')
df.head()

#displaying recommended movies sorted by our recommendation engine
df.head()