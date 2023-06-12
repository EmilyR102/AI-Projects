import json
import os

from classes.restaurant import Restaurant, train, Recommendations
from query import main

restaurants = []


def init_restaurants(n):
    """
    Initialize the restaurants list with Restaurant objects made from all_restaurants.json.

    n = number of items to iterate through in all_restaurants.json
    """
    global restaurants

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    restaurant_file_path = os.path.join(root_dir, "src", "data", "all_restaurants.json")

    with open(restaurant_file_path, "r") as f:
        restaurant_data = json.load(f)

    i = 0
    for k, v in restaurant_data.get("data").items():
        if i == n:
            break
        i += 1
        rest = Restaurant(name=k)
        rest.location = v["location"]
        for item in v["reviews_and_ratings"]:
            rev, rat = item["Review"], item["Rating"]
            rest.reviews.append(rev)
            rest.ratings.append(rat)
        restaurants.append(rest)


import io
import sys


def make_restaurants(n=100, display=False):
    """
    set scores for each item in restaurants list

    n = number of Restaurant objects to make in restaurants
    display = display scores to console for each Restaurant
    """
    global restaurants

    # for example, you can do make_restaurants(1, True) to display the results of set_score for one restaurant

    init_restaurants(n)

    sys.stdout = io.StringIO()
    train()
    [r.set_scores() for r in restaurants]
    sys.stdout = sys.__stdout__

    if display:
        for r in restaurants:
            print(f"SCORES FOR {r.name}\n")
            print(
                f"\nreview score is {r.review_score}\n rating score is {r.rating_score}\n final score is {r.final_score}"
            )
            print("\n----------------------------\n")


def make_recommendations(n):
    """
    Get the top-N recommendations
    """
    global restaurants

    recs = Recommendations(restaurants=restaurants)
    recs.set_top_N(n)

    print(
        f"\n\nHere is a list of the top {n} places we recommend based on reviews and rating by customers:"
    )

    for i in range(len(recs.best)):
        r = recs.best[i]
        print(f"\n{i+1}. {r.name}\n")
        print(f"final score is {r.final_score}")
        print("\n----------------------------\n")

    return recs


if __name__ == "__main__":
    go = "y"
    while go == "y":
        main()
        n = int(input("\nChoose how many recommendations you want: "))
        make_restaurants()
        recs = make_recommendations(n)

        go2 = "y"
        while go2 == "y":
            rank = int(input("\nGive the rank of the recommendation you want: "))
            r = recs.best[rank - 1]
            print(f"\nHere's the location of {r.name}:\n{r.location}")
            go2 = input("\nDo you want another restaurant's location? say (y/n): ")

        go = input("\nDo you want to do this again? say (y/n): ")
        go = input("\nDo you want to do this again? say (y/n): ")
