#!/usr/bin/env python
# coding: utf-8

# ### Project 1: Task Manager

# In[ ]:


"""
Problem: You're working for an online marketplace. Users often search for products using keywords. Given 
a list of product names and their corresponding IDs, design a function that allows users to input a keyword 
and quickly find the product they are looking for. Implement a linear search algorithm to search for the 
keyword in the list of product names and return the corresponding product ID
- Display whether the target item was found or not in the list. 
- Return a closing/welcome message
- Apply object-oriented programming principles to design classes for tasks and users.
- Practice working with data structures like lists and dictionaries for task management.
- Implement decorators to add additional functionality to tasks.
- Gain experience in implementing a command-line application with functions and classes.
"""


# ### SOLUTION

# In[2]:


class ProductSearch:
    def __init__(self):
        # Initialize an empty dictionary to store products (name -> ID)
        self.products = {}

    def add_product(self, product_name, product_id):
        # Add a product to the dictionary
        self.products[product_name] = product_id

    def search_product(self, keyword):
        # Search for a product by keyword
        if keyword in self.products:
            return self.products[keyword]
        else:
            return None

    def welcome_message(self):
        # Display a welcome message
        print("Welcome to the Product Search System!")

    def closing_message(self):
        # Display a closing message
        print("Thank you for using the Product Search System. Goodbye!")

def search_and_display(product_search, keyword):
    def decorator(func):
        def wrapper(product_search, keyword):
            print("Searching for the product...")
            result = func(product_search, keyword)
            if result:
                print(f"Product found! Product ID: {result}")
            else:
                print("Product not found.")
        return wrapper
    
    @decorator
    def perform_search(product_search, keyword):
        return product_search.search_product(keyword)

    perform_search(product_search, keyword)

product_search = ProductSearch()

# Add some products to the system, You can add more product here
product_search.add_product("books", "id - 1")
product_search.add_product("phone", "id - 2")
product_search.add_product("boot", "id - 3")
product_search.add_product("Tablet", "id - 4")

product_search.welcome_message()

while True:
    user_input = input("Enter a keyword to search for a product (or 'exit' to quit): ")
    if user_input.lower() == 'exit':
        break
    search_and_display(product_search, user_input)

product_search.closing_message()


# ### Project 2: Movie recommender system

# In[ ]:


"""
Problem: Build a movie recommendation system that suggests movies to users based on their preferences. 
Create a class-based system where each user can rate movies. Use a dictionary to store movie ratings, and 
implement a recommendation algorithm that suggests movies similar to those the user has liked. The 
program should allow users to:
i. Add new movies to the system.
ii. Rate movies on a scale of 1 to 5.
iii. Get recommendations based on the user's 
highest-rated movies using a 
recommendation decorator.
Implement a function to find movies with the highest and lowest average ratings
- Display recommended movies based on user’s highly-rated movies
- Show average ratings for movies
- Display movies with the highest & lowest ratings
- Design and implement classes for movies and users to manage data effectively.
- Practice working with dictionaries and lists to store and organize movie ratings.
- Apply lambda expressions and list comprehension for filtering and processing movie data.
- Gain experience in creating a recommendation system based on user preferences
"""


# ### SOLUTION

# In[5]:


class MovieRecommendationSystem:
    def __init__(self):
        # Initialize an empty dictionary to store movie ratings
        self.user_ratings = {}
        self.movies = {}

    def add_user(self, user_id):
        # Create an entry for a new user with an empty dictionary of movie ratings
        self.user_ratings[user_id] = {}

    def add_movie(self, movie_name):
        # Add a new movie to the system
        self.movies[movie_name] = []

    def rate_movie(self, user_id, movie_name, rating):
        # Rate a movie on a scale of 1 to 5
        if rating < 1 or rating > 5:
            print("Invalid rating. Please rate the movie on a scale of 1 to 5.")
            return

        if movie_name not in self.movies:
            print("Movie not found.")
            return

        if user_id not in self.user_ratings:
            print("User not found.")
            return

        self.user_ratings[user_id][movie_name] = rating
        self.movies[movie_name].append(rating)

    def get_recommendations(self, user_id):
        # Generate movie recommendations for a user using collaborative filtering
        user_ratings = self.user_ratings[user_id]

        # Create a dictionary to store user similarities
        user_similarities = {}

        for other_user_id, other_user_ratings in self.user_ratings.items():
            if other_user_id != user_id:
                # Calculate similarity between users based on common movie ratings
                common_movies = set(user_ratings.keys()) & set(other_user_ratings.keys())
                if common_movies:
                    numerator = sum(user_ratings[movie] * other_user_ratings[movie] for movie in common_movies)
                    denominator_user = sum(user_ratings[movie] ** 2 for movie in common_movies) ** 0.5
                    denominator_other_user = sum(other_user_ratings[movie] ** 2 for movie in common_movies) ** 0.5

                    similarity = numerator / (denominator_user * denominator_other_user)

                    user_similarities[other_user_id] = similarity

        # Sort users by similarity and get top recommendations
        sorted_users = sorted(user_similarities.items(), key=lambda x: x[1], reverse=True)
        most_similar_user_id = sorted_users[0][0]

        recommendations = []
        for movie in self.user_ratings[most_similar_user_id]:
            if movie not in user_ratings:
                recommendations.append(movie)

        return recommendations

    def find_highest_rated_movie(self):
        # Find the movie with the highest average rating
        if not self.movies:
            return None

        highest_rated_movie = max(self.movies, key=lambda movie: sum(self.movies[movie]) / len(self.movies[movie]))
        return highest_rated_movie

    def find_lowest_rated_movie(self):
        # Find the movie with the lowest average rating
        if not self.movies:
            return None

        lowest_rated_movie = min(self.movies, key=lambda movie: sum(self.movies[movie]) / len(self.movies[movie]))
        return lowest_rated_movie

    @staticmethod
    def recommendation_decorator(user_id):
        # Decorator to provide recommendations based on user's highest-rated movies
        def decorator(func):
            def wrapper(movie_system):
                user_ratings = movie_system.user_ratings[user_id]
                highest_rated_movies = [movie for movie in user_ratings if user_ratings[movie] == 5]

                if highest_rated_movies:
                    recommendations = func(movie_system)
                    return [movie for movie in recommendations if movie in highest_rated_movies]
                else:
                    print("You need to rate some movies with 5 stars to get recommendations.")
                    return []

            return wrapper

        return decorator

# Create an instance of the MovieRecommendationSystem class
movie_system = MovieRecommendationSystem()

# Add users, movies, and ratings
movie_system.add_user("User 1")
movie_system.add_user("User 2")
movie_system.add_movie("Movie A")
movie_system.add_movie("Movie B")
movie_system.add_movie("Movie C")

movie_system.rate_movie("User 1", "Movie A", 4)
movie_system.rate_movie("User 1", "Movie B", 5)
movie_system.rate_movie("User 2", "Movie A", 3)
movie_system.rate_movie("User 2", "Movie C", 4)

# Decorate the get_recommendations method for User 1 to get recommendations based on highly rated movies
@movie_system.recommendation_decorator("User 1")
def get_recommendations_based_on_similar_users(movie_system):
    return movie_system.get_recommendations("User 1")

# Get movie recommendations for User 1 based on highly rated movies
user_id = input("Enter the user, 'user 1' or 'user 2': ")
recommended_movies = get_recommendations_based_on_similar_users(movie_system)
print(f"Recommended movies for {user_id}: {recommended_movies}, recommendation depending on the user's highest rated movie")

# Find the highest and lowest rated movies
highest_rated_movie = movie_system.find_highest_rated_movie()
lowest_rated_movie = movie_system.find_lowest_rated_movie()
print(f"Highest rated movie: {highest_rated_movie}")
print(f"Lowest rated movie: {lowest_rated_movie}")


# In[ ]:




