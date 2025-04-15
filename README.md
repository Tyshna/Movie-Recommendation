# Movie Recommendation System

This document describes two movie recommendation systems implemented in Python:

1\. Popularity-Based Recommendation

2\. Collaborative Filtering Recommendation
## Data Sources:
1. movies\_df: Movie metadata (title, genres, popularity, etc.)
1. links\_df: Movie IDs and TMDB IDs mapping.
1. ratings\_df: User movie ratings.
## Dependencies:
1. pandas
1. numpy
1. ast (for literal\_eval)
1. sklearn (for cosine\_similarity)
# **1. Popularity-Based Recommendation**
This system recommends movies based on their popularity and average ratings.
## Data Preprocessing:
1. Load movie metadata.
1. Clean and preprocess the data (remove duplicates, handle missing values, convert data types).
1. Extract genre information from the 'genres' column using literal\_eval and explode the DataFrame.
1. Calculate a weighted rating for each movie, considering both average rating and vote count.
1. Filter movies based on a minimum vote count threshold.
## Functions:
1. weighted\_rating(df): Calculates the weighted rating for a movie.
1. genre\_recommender(fav\_genre): Recommends top 25 movies for a given genre.
## Usage:
- Load the 'movies\_df' dataset.
- Call genre\_recommender(genre) to get recommendations for a specific genre.
## Example:
`       `genre\_recommender('Thriller')

# **2. Collaborative Filtering Recommendation**
This system recommends movies based on user similarity using cosine similarity.
## Data Preprocessing:
1. Load movie metadata, links, and ratings data.
1. Merge dataframes to create a unified movie rating dataset.
1. Create a user-item rating matrix (pivot table).
1. Calculate cosine similarity between users.
1. Identify top similar users for a given user.
1. Calculate weighted ratings based on similarity scores and user ratings.
1. Recommend movies with the highest weighted ratings.
## Functions:
- Data loading
- Merging
- Pivoting
- Similarity calculation
- Recommendation Generation.
## Usage:
1. Load the 'movies\_df', 'links\_df', and 'ratings\_df' datasets.
1. Create a user-item rating matrix.
1. Calculate user similarity using cosine\_similarity.
1. Obtain top similar users.
1. Calculate weighted ratings and generate movie recommendations.
## Implementation Details:
### Popularity-Based Recommendation:
- The weighted rating formula combines average rating and vote count, giving more weight to movies with higher vote counts.
- The genre\_recommender function filters movies by genre and returns the top 25 movies based on weighted rating.
### Collaborative Filtering Recommendation:
- Cosine similarity is used to measure user similarity based on their movie ratings.
- Weighted ratings are calculated by multiplying user similarity scores with movie ratings.
- The system recommends movies that have high cumulative weighted ratings from similar users.
### Data Files:
- movies\_df: Movie metadata.
- links\_df: Movie ID mappings.
- ratings\_df: User movie ratings.
