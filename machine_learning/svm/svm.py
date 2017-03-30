#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 18:05:25 2017

@author: francisco
"""

from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
import numpy as np

# In[]

def read_csv(filename):
    """
    utility for reading a csv file
    
    :param filename: str representing the file to read
    
    :return data: numpy nd array
    """
    f = open(filename, 'r')
    return np.array([line.strip().split(',') for line in f.readlines()]).astype(int)


if __name__=="__main__":
    
    # - Read In data
    train = read_csv('P4_train.txt')
    test = read_csv('P4_test.txt')
    
    # - Separate data into x and y 
    X_train = train[:,:-1]
    y_train = train[:,-1]
    
    X_test = test[:,:-1]
    y_test = test[-1]
    
    # - Task 1 Compare the results of Quadratic Kernel and Gaussian Kernel (RBF)
    # conduct grid search to find the best hyper parameters using an rbf kernel 
    # then fit and score
    svm_rbf = GridSearchCV(SVC(), param_grid={'C':np.arange(0.1, 10.1, 0.1), 
                                             'gamma':np.arange(0.01, 1.0, 0.1)},
                            scoring='accuracy')
    
    svm_rbf.fit(X_train, y_train)
    print svm_rbf.score(X_test, y_test)
    
    # conduct grid search to find the best hyper parameters using an quadrtic kernel
    # then fit and score
    svm_quad = GridSearchCV(SVC(kernel='poly', degree=2), param_grid={'C':np.arange(0.1, 10.1, 0.1), 
                                             'gamma':np.arange(0.01, 1.0, 0.1)},
                            scoring='accuracy')
    
    svm_quad.fit(X_train, y_train)
    print svm_quad.score(X_test, y_test)
    
    # - Task 2
    # Compare KNN to the previous results
    knn = GridSearchCV(KNeighborsClassifier(), param_grid={'n_neighbors':range(1,11)},
                       scoring='accuracy')
    
    knn.fit(X_train, y_train)
    print knn.score(X_test, y_test)
    
    
