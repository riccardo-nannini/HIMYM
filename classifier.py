import pandas as pd
import numpy as np
import sklearn
import time
from sklearn import preprocessing, svm
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier


class Dataset:
    def __init__(self, path):
        raw_dataset = pd.read_csv(path)
        self.dataset = raw_dataset.drop(['Name', 'TimeDateStamp', 'CheckSum', 'Machine', 'Malware'], axis=1)
        self.label = raw_dataset['Malware']
        scaler = preprocessing.StandardScaler().fit(self.dataset)
        self.std_dataset = scaler.transform(self.dataset)


if __name__ == "__main__":
    dataset = Dataset("dataset_malwares.csv")
    X_train, X_test, Y_train, Y_test = train_test_split(dataset.std_dataset, dataset.label, test_size=0.2,
                                                        random_state=20)

    print("""\
    
     _        _        _       
    | \    /\( (    /|( (    /|
    |  \  / /|  \  ( ||  \  ( |
    |  (_/ / |   \ | ||   \ | |
    |   _ (  | (\ \) || (\ \) |
    |  ( \ \ | | \   || | \   |
    |  /  \ \| )  \  || )  \  |
    |_/    \/|/    )_)|/    )_)

        """)

    cv_res = {}
    print("# KNN - 5-fold cross validation\n")
    for i in range(1, 10, 2):
        knn = KNeighborsClassifier(n_neighbors=i, weights='uniform', p=2)
        cv_mean = cross_val_score(knn, X_train, Y_train, cv=5).mean()
        print("# KNN - Cross validation accuracy using ", i, "NN: ", cv_mean)
        cv_res[i] = cv_mean

    optimal = max(cv_res, key=cv_res.get)
    print("# KNN - Optimal K:", optimal, "\n")

    knn = KNeighborsClassifier(n_neighbors=optimal, weights='uniform', p=2)

    knnStartTraining = time.time()
    knn.fit(X_train, Y_train)
    knnStopTraining = time.time()

    knnStartTesting = time.time()
    knnScore = knn.score(X_test, Y_test)
    knnStopTesting = time.time()

    print("# KNN - training time: ", knnStopTraining - knnStartTraining)
    print("# KNN - testing time: ", knnStopTesting - knnStartTesting)
    print("# KNN - prediction accuracy: ", knnScore)


    '''SVM ASCII ART PLACEHOLDER'''
    cv_res = {}
    print("# SVM - 5-fold cross validation\n")
    for i in [1.0e-2, 1.0e-1, 1.0, 1.0e1, 1.0e2]:
        svc = svm.SVC(C=i, kernel='linear')
        cv_mean = cross_val_score(svc, X_train, Y_train, cv=5).mean()
        print("# SVM - Cross validation accuracy using ", i, "NN: ", cv_mean)
        cv_res[i] = cv_mean

    optimal = max(cv_res, key=cv_res.get)
    print("# SVM - Optimal C:", optimal, "\n")

    svc = svm.SVC(C=optimal, kernel='linear')

    svmStartTraining = time.time()
    svc.fit(X_train, Y_train)
    svmStopTraining = time.time()

    svmStartTesting = time.time()
    svmScore = svc.score(X_test, Y_test)
    svmStopTesting = time.time()

    print("# SVM - training time: ", svmStopTraining - svmStartTraining)
    print("# SVM - testing time: ", svmStopTesting - svmStartTesting)
    print("# SVM - prediction accuracy: ", svmScore)

