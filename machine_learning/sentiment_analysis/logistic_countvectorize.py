from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold
import pandas as pd

def read_csv(filename):
    """
    read a csv with tweets in it. some edge case handling is necessary to
    preprocess the data correctly

    :param filename: str
    :return dataframe: pandas.DataFrame
    """
    f = open(filename, 'r')
    target = []
    data = []
    for line in f.readlines():
        y, x = line.split(',', 1)
        target.append(y)
        data.append(x.replace("\n", "").strip().decode('utf-8', 'ignore').encode('utf-8'))
    f.close()
    return pd.DataFrame({"sentiment": target, "tweet": data})

def cross_validate(estimator, X, n_folds):
    """
    this cross validation function uses count vectorizer to create the features
    for training and validation

    :param estimator: sklearn estimator object
    :param n_foles: the number of folds to use - int
    :return average misclassification: float
    """
    score_sum = 0.0
    kf = KFold(n_splits=n_folds, shuffle=True)

    #- Main Loop
    # for each split into training and validation data
    # then use the training portion to fit the CountVectorizer and transform
    # both the train_X and val_X sets.
    for train_index, val_index in kf.split(X):
        train_x, train_y = X.loc[train_index, 'tweet'], X.loc[train_index, 'sentiment']
        val_x, val_y = X.loc[val_index, 'tweet'], X.loc[val_index, 'sentiment']

        # - CountVectorize
        # make sure to fit only on the training portion so as to not leak any
        # information from the validation portion
        vect = CountVectorizer().fit(train_x)
        X_train = vect.transform(train_x)
        X_val = vect.transform(val_x)

        estimator.fit(X_train, train_y)
        score_sum += estimator.score(X_val, val_y)

    return 1-score_sum/n_folds

if __name__=="__main__":
    """
    predict the sentiment of tweets using countVectorization from sklearn
    """
    data = read_csv('tweets-train.csv')

    folds = 10 # number of folds to use in cross validation

    lr = LogisticRegression(C=0.1)

    print cross_validate(lr, data, folds)
