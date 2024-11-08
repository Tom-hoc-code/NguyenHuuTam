import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class DataAnalyzing:

    def __init__(self, df):
        self.df = df

    def preprocess_data(self):
        self.movies_and_shows = self.df[(self.df['type'] == 'Movie') | (self.df['type'] == 'TV Show')]
        self.tv_shows = self.df[self.df['type'] == 'TV Show']
        self.movies = self.df[self.df['type'] == 'Movie']
        self.added_year = self.df['date_added'].dt.year 
        self.df['genres'] = self.df['genres'].str.split(', ')
        self.df = self.df.explode('genres')

    def count_movies(self):
        temporary = self.movies['country'].str.split(', ')
        all_movies = temporary.explode()
        return all_movies.value_counts().sort_index()
    
    def count_tv_shows(self):
        temporary = self.tv_shows['country'].str.split(', ')
        all_tv_shows = temporary.explode()
        return all_tv_shows.value_counts().sort_index()
    
    def count_movies_and_shows_by_country(self):
        temporary = self.movies_and_shows['country'].str.split(', ')
        all_movies_and_shows = temporary.explode() 
        return all_movies_and_shows.value_counts().sort_index() 


    def average_duration_by_year(self):
        return self.movies_and_shows.groupby('release_year')['minutes'].mean()


    def exclusive_movies_count(self):
        exclusive_movies = self.df[(self.df['type'] == 'Movie') & (self.df['release_year'] == self.df['date_added'].dt.year)]
        return exclusive_movies['release_year'].value_counts().sort_index()


    def count_by_year_added(self):
        return self.added_year.value_counts().sort_index()


    def top_5_actors_by_genre(self):
        genre_counts = self.df['genres'].value_counts()
        top_genres = genre_counts.head(5).index
        top_actors = {}

        for genre in top_genres:
            actors_count = self.df[self.df['genres'] == genre]['cast'].str.split(', ').explode().value_counts().head(5)
            top_actors[genre] = actors_count
    
        return top_actors

    def top_5_directors_by_rating(self):
        top_directors = {}
        for rating, group in self.df.groupby('rating'):
            directors_count = group['director'].str.split(', ').explode().value_counts().head(5)
            top_directors[rating] = directors_count
        return top_directors


    def print_summary(self):
        print("Các hàng có cột 'type' là 'TV show':")
        print(self.count_tv_shows())

        print("Các hàng có cột 'type' là 'Movie':")
        print(self.count_movies())

        print("Số lượng phim và show TV theo quốc gia:")
        print(self.count_movies_and_shows_by_country())

        print("Thời gian trung bình phim và show TV theo năm phát hành:")
        print(self.average_duration_by_year())

        print("Thống kê số lượng phim độc quyền bởi Netflix:")
        print(self.exclusive_movies_count())

        print("Thống kê số lượng phim và show TV theo năm được thêm vào Netflix:")
        print(self.count_by_year_added())
        
        print("Top 5 diễn viên đóng nhiều phim nhất theo thể loại:")
        for genre, actors in self.top_5_actors_by_genre().items():
            print(f"Thể loại {genre}:")
            print(actors)
            print()

        print("Top 5 đạo diễn có nhiều phim nhất theo loại đánh giá:")
        for rating, directors in self.top_5_directors_by_rating().items():
            print(f"Rating {rating}:")
            print(directors)
            print()

        stats = self.calculate_duration_statistics()
        print("Thống kê thời gian:")
        for key, value in stats.items():
            print(f"{key}: {value}")
