import os
import json
import random
import statistics
from typing import List

from ml_model.model import eval_reviews, eval_weights, make_model

model, tokenizer = None, None

def train():
    """
    Train the model
    """
    global model, tokenizer

    # # Get the absolute path of the project root directory
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # # Construct the absolute path
    data_file_path = os.path.join(root_dir, "data", "model_data.json")

    with open(data_file_path, "r") as f:
        data = json.load(f)

    model, tokenizer = make_model(data)
    
class Restaurant:
    def __init__(self, name) -> None:
        self.name: str = name
        self.location: str = ""
        self.reviews: List[str] = []
        self.ratings: List[int] = []
        self.rating_score: int = 0
        self.review_score: int = 0
        self.final_score: int = 0

    def set_scores(self):
        """
        update all the scores of a restaurant
        """
        self.__set_review_score()
        self.__set_rating_score()
        self.__set_final_score()

    def __set_review_score(self):
        """
        update review_score as the score calculated from eval_reviews()
        """
        self.review_score = eval_reviews(self.reviews, model, tokenizer)

    def __set_rating_score(self):
        """
        Normalize ratings and take average. Set the result to rating_score.
        """
        total = sum(self.ratings)
        norm_ratings = (r / total for r in self.ratings)
        self.rating_score = statistics.mean(norm_ratings) if self.ratings else 0

    def __set_final_score(self):
        """
        Calculate final score from rating and review scores and their weights, which is from eval_weights.
        """
        global model, tokenizer

        rating_weight, review_weight = eval_weights(self.ratings, self.reviews, model, tokenizer)

        # print(f"\nPCA weights\n rating weight: {rating_weight}, review weight: {review_weight}\n")

        self.final_score = (rating_weight * self.rating_score) + (
            review_weight * self.review_score
        )


class Recommendations:
    def __init__(self, restaurants) -> None:
        self.restaurants:list = restaurants
        self.best = []

    def set_top_N(self, n):
        """
        sort in descending order of each restaurant's final score and and get the top N
        """
        n = min(n, len(self.restaurants))
        
        self.best = sorted(
            self.restaurants, key=lambda r: r.final_score, reverse=True
        )[:n]
