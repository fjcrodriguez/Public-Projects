import argparse
import re
import os
import csv
import math
import itertools
import collections as coll
import numpy as np

def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def read_csv(filename):
    """
    read one line at time to avoid nested for loops during prediction
    """

    f = open(filename, 'r')

    # create a list of strings that is each row
    rows = f.read().strip().split('\n')

    # create a list of tuples where each tuple is a row
    data = [tuple(row.split(',')) for row in rows]
    data = [ (int(m), int(u), float(r)) for (m,u,r) in data]

    return data


def parse_file(filename):
    """
    Given a filename outputs user_ratings and movie_ratings dictionaries

    Input: filename

    Output: user_ratings, movie_ratings
        where:
            user_ratings[user_id] = {movie_id: rating}
            movie_ratings[movie_id] = {user_id: rating}
    """
    f = open(filename, 'r')

    # create a list of strings where each string is a row
    rows = f.read().strip().split('\n')

    # create a list of tuples where each tuple is a row
    data = [tuple(row.split(',')) for row in rows]
    data = [ (int(m), int(u), float(r)) for (m,u,r) in data]

    # intialize nested dictionaries to store data in
    # easily accessible containers
    user_ratings = coll.defaultdict(dict)
    movie_ratings = coll.defaultdict(dict)

    for movie_id, user_id, rating in data:
        user_ratings[user_id][movie_id] = float(rating)
        movie_ratings[movie_id][user_id] = float(rating)

    return user_ratings, movie_ratings


def compute_average_user_ratings(user_ratings):
    """ Given a the user_rating dict compute average user ratings
    Input: user_ratings (dictionary of user, movies, ratings)
    Output: ave_ratings (dictionary of user and ave_ratings)
    """

    ave_ratings = {}
    for user in user_ratings:
        ratings = [float(r) for (m, r) in user_ratings[user].items()]
        avg = sum(ratings) / len(ratings)
        ave_ratings[user] = avg

    return ave_ratings


def compute_user_similarity(d1, d2, ave_rat1, ave_rat2):
    """ Computes similarity between two users

        Uses a modified Pearson's correlation coeficient

        Input: d1, d2, (dictionary of user ratings per user)
            ave_rat1, ave_rat2 average rating per user (float)
        Ouput: user similarity (float)
    """

    # compute the similarity based only movies found in both
    movies_d1 = set(d1.keys())
    movies_d2 = set(d2.keys())
    common_set = movies_d1.intersection(movies_d2)

    if len(common_set) == 0:
        return 0.0


    numerators = [(d1[m] - ave_rat1) * (d2[m] - ave_rat2) for m in common_set]
    denominator1 = [(d1[m] - ave_rat1)**2 for m in common_set]
    denominator2 = [(d2[m] - ave_rat2)**2 for m in common_set]

    if np.sqrt( sum(denominator1) * sum(denominator2)) == 0.0:
        return 0.0

    w = sum(numerators) / np.sqrt( sum(denominator1) * sum(denominator2))

    return w


def main():
    """
    This function is called from the command line via

    python cf.py --train [path to filename] --test [path to filename]
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    print train_file, test_file

    # parse train/test files and create dictionaries of ratings
    userRatings_train, movieRatings_train = parse_file(train_file)
    userRatings_test = read_csv(test_file)

    userRatings_pred = []

    # compute the users average for easy accessbility later
    avg_ratings = compute_average_user_ratings(userRatings_train)

    # write the predictions to a file
    f = open('predictions.txt', 'w')

    for mov, user_id, rating in userRatings_test:

        avgR_i = avg_ratings[user_id]
        ratings_otherUsers = movieRatings_train[mov]

        other_users = [u for (u, r) in movieRatings_train[mov].items() if u != user_id]

        simils = [(u, compute_user_similarity(userRatings_train[user_id], userRatings_train[u], avg_ratings[user_id], avg_ratings[u]) ) for u in other_users]
        simils = dict(simils)

        numers = [simils[u] * (ratings_otherUsers[u] - avg_ratings[u]) for u in other_users]
        denos = [abs(simils[u]) for u in other_users]


        if sum(denos) == 0.0:
            prediction = avgR_i
        else:
            prediction = avgR_i + ( sum(numers) / sum(denos) )

        userRatings_pred.append( (user_id, mov, rating , prediction ) )
        f.write(",".join( [str(mov), str(user_id), str(rating), str(prediction)] ) + "\n" )


    f.close()

    # compute RMSE and MAE
    error = [(row[2] - row[3])**2 for row in userRatings_pred]
    abs_error = [abs(row[2] - row[3]) for row in userRatings_pred]

    mae = sum(abs_error) / len(error)
    mse = sum(error) / len(error)
    rmse = np.sqrt(mse)

    print "RMSE:", "%2.4f" % (rmse)
    print "MAE:", "%2.4f" % (mae)


if __name__ == '__main__':
    main()
