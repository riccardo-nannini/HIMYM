import pandas as pd
import numpy as np
import sklearn
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


class Dataset:
    def __init__(self, path: str):
        raw_dataset = pd.read_csv(path)
        self.dataset = raw_dataset.drop(['Name', 'TimeDateStamp', 'CheckSum', 'Machine', 'Malware'], axis=1)
        self.label = raw_dataset['Malware']
        scaler = preprocessing.StandardScaler().fit(self.dataset)
        self.std_dataset = scaler.transform(self.dataset)


def train_and_validate(X_train, Y_train, X_test, Y_test, classifier, hyperparams, printables, folds=5):
    print(printables['ASCII'])
    cv_res = {}
    method = printables['method']
    param = printables['param']
    for i in hyperparams:
        c = classifier(i)
        cv_mean = cross_val_score(c, X_train, Y_train, cv=folds).mean()
        print("# {method} - Cross validation accuracy using {param} = {param_val}: {mean}".
              format(method=method, param=param, param_val=i, mean=cv_mean))
        cv_res[i] = cv_mean

    optimal = max(cv_res, key=cv_res.get)
    print("# {method} - Optimal {param}: {opt}\n".
          format(method=method, param=param, opt=optimal))

    c = classifier(optimal)

    start_training = time.time()
    c.fit(X_train, Y_train)
    stop_training = time.time()

    start_testing = time.time()
    score = c.score(X_test, Y_test)
    stop_testing = time.time()

    print("# {method} - training time: {t}".format(method=method, t=stop_training - start_training))
    print("# {method} - testing time: {t}".format(method=method, t=stop_testing - start_testing))
    print("# {method} - prediction accuracy: {t}".format(method=method, t=score))


if __name__ == "__main__":
    dataset = Dataset("dataset_malwares.csv")
    X_train, X_test, Y_train, Y_test = train_test_split(dataset.std_dataset, dataset.label, test_size=0.2,
                                                        random_state=20)

    knn_ascii = """\
    
     _        _        _       
    | \    /\( (    /|( (    /|
    |  \  / /|  \  ( ||  \  ( |
    |  (_/ / |   \ | ||   \ | |
    |   _ (  | (\ \) || (\ \) |
    |  ( \ \ | | \   || | \   |
    |  /  \ \| )  \  || )  \  |
    |_/    \/|/    )_)|/    )_)

        """
    knn = lambda x: KNeighborsClassifier(n_neighbors=x, weights='uniform', p=2)
    knn_printables = {'method': 'KNN', 'param': 'NN', 'ASCII': knn_ascii}
    train_and_validate(X_train, Y_train, X_test, Y_test, knn, range(1, 10, 2), knn_printables)

    svm = lambda x: SVC(C=x, kernel='linear')
    svm_printables = {'method': 'SVM', 'param': 'C', 'ASCII': '\nSVM ASCII PLACEHOLDER'}
    svm_hypeparams = [1.0e-2, 1.0e-1, 1.0, 5.0, 1.0e1]
    train_and_validate(X_train, Y_train, X_test, Y_test, svm, svm_hypeparams, svm_printables)