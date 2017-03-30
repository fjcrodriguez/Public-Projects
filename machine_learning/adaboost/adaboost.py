import numpy as np
import argparse
from sklearn.tree import DecisionTreeClassifier

def parse_argument():
    """
    Code for parsing arguments
    """
    parser = argparse.ArgumentParser(description='Parsing a file.')
    parser.add_argument('--train', nargs=1, required=True)
    parser.add_argument('--test', nargs=1, required=True)
    parser.add_argument('--numTrees', nargs=1, required=True)
    args = vars(parser.parse_args())
    return args


def adaboost(X, y, num_iter, max_dep=1):
    """Given an numpy matrix X, a array y and num_iter return trees and weights

    Input: X, y, num_iter
    Outputs: array of trees from DecisionTreeClassifier
             trees_weights array of floats
    Assumes y is in {-1, 1}^n
    """
    trees = []
    trees_weights = []
    feature_weights = []

    w = np.repeat(1.0/len(y), len(y))
    for _iter in range(num_iter):
        # fit the tree
        tree_m = DecisionTreeClassifier(max_depth=max_dep)
        tree_m.fit(X, y , sample_weight=w)

        # compute the error
        pred = tree_m.predict(X)
        err = sum(w * (pred != y).astype(int) )/sum(w)

        trees.append(tree_m)
        if err == 0.0:
            trees_weights.append(1)
            break

        # compute tree weight
        alpha = np.log( (1 - err)/ err )
        trees_weights.append(alpha)
        feature_weights.append(tree_m.feature_importances_)

        # update weights
        w = w * np.exp(alpha * (pred != y).astype(int) )

    return trees, trees_weights, feature_weights


def adaboost_predict(X, trees, trees_weights):
    """Given X, trees and weights predict Y

    assume Y in {-1, 1}^n
    """
    sums = np.zeros(X.shape[0])
    for t, w in zip(trees, trees_weights):
        sums += w * t.predict(X)

    Yhat = np.sign(sums)
    return Yhat


def parse_spambase_data(filename):
    """ Given a filename return X and Y numpy arrays

    X is of size number of rows x num_features
    Y is an array of size the number of rows
    Y is the last element of each row.
    """

    f = open(filename, 'r')
    X = []
    Y = []
    for line in f:
        row = line.strip().split(',')
        try:
            X.append([ round(float(val),4) for val in row[:-1] ])
            Y.append(int(row[-1]))
        except:
            continue
    f.close()

    X = np.array(X)
    Y = np.array(Y)
    return X, Y


def new_label(Y):
    """ Transforms a vector of 0s and 1s in -1s and 1s.
    """
    return [-1. if label==0 else 1 for label in Y]


def old_label(Y):
    return [0. if label==-1 else 1 for label in Y]


def accuracy(y, pred):
    return np.sum(y == pred) / float(len(y))


def main():
    """
    This code is called from the command line via

    python adaboost.py --train [path to filename] --test [path to filename] --numTrees
    """
    args = parse_argument()
    train_file = args['train'][0]
    test_file = args['test'][0]
    num_trees = int(args['numTrees'][0])

    print train_file, test_file, num_trees


    X, Y = parse_spambase_data(train_file)
    X_test, Y_test = parse_spambase_data(test_file)

    Y_new = new_label(Y)

    trees, tree_weights, feature_weights = adaboost(X, Y_new, num_trees, max_dep=None)

    Yhat = adaboost_predict(X, trees, tree_weights)
    Yhat_test = adaboost_predict(X_test, trees, tree_weights)

    Yhat = old_label(Yhat)
    Yhat_test = old_label(Yhat_test)

    ## here print accuracy and write predictions to a file
    acc_test = accuracy(Y_test, Yhat_test)
    acc = accuracy(Y, Yhat)
    print("Train Accuracy %.4f" % acc)
    print("Test Accuracy %.4f" % acc_test)

    f = open("predictions.txt", "w")

    for i in range(len(Y_test)):
        # concatenates a string of values
        f.write(",".join([str(val) for val in np.append( X_test[i], [Y_test[i], Yhat_test[i]] ) ] ) + "\n" )

    f.close()

    f = open("feature_weights", "w")

    for i in range(len(feature_weights)):
        f.write(",".join([str(val) for val in feature_weights[i]]) + "\n")

    f.close()

if __name__ == '__main__':
    main()
