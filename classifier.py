import pandas as pd
import time
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt


class Dataset:
    def __init__(self, path: str):
        raw_dataset = pd.read_csv(path)
        self.dataset = raw_dataset.drop(['Name', 'TimeDateStamp', 'CheckSum', 'Machine', 'Malware'], axis=1)
        self.label = raw_dataset['Malware']
        scaler = preprocessing.StandardScaler().fit(self.dataset)
        self.std_dataset = scaler.transform(self.dataset)


def print_graphs(X_test, Y_test, classifier, printables):
    titles_options = [
        (printables['method'] + ": Confusion matrix", None),
        (printables['method'] + ": Normalized confusion matrix", "true"),
    ]
    for title, normalize in titles_options:
        disp = ConfusionMatrixDisplay.from_estimator(
            classifier,
            X_test,
            Y_test,
            display_labels=['benign', 'malicious'],
            cmap=plt.cm.Blues,
            normalize=normalize,
        )
        disp.ax_.set_title(title)

        print(title)
        print(disp.confusion_matrix)

    plt.show()


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

    start_training = time.time_ns() / 1000000
    c.fit(X_train, Y_train)
    stop_training = time.time_ns() / 1000000

    start_testing = time.time_ns() / 1000000
    score = c.score(X_test, Y_test)
    stop_testing = time.time_ns() / 1000000

    print("# {method} - training time: {t}ms".format(method=method, t=stop_training - start_training))
    print("# {method} - inference time: {t}ms".format(method=method, t=stop_testing - start_testing))
    print("# {method} - prediction accuracy: {t}%".format(method=method, t=score * 100))
    return c, (stop_testing - start_testing), (score * 100)


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
    knn_model, knn_inference, knn_accuracy = train_and_validate(X_train, Y_train, X_test, Y_test, knn, range(1, 10, 2),
                                                                knn_printables)
    print_graphs(X_test, Y_test, knn_model, knn_printables)

    svm_ascii = """\n\

     _______           _______ 
    (  ____ \|\     /|(       )
    | (    \/| )   ( || () () |
    | (_____ | |   | || || || |
    (_____  )( (   ) )| |(_)| |
          ) | \ \_/ / | |   | |
    /\____) |  \   /  | )   ( |
    \_______)   \_/   |/     \|
                           

        """

    svm = lambda x: SVC(C=x, kernel='poly', degree=3)  # TODO - define kernel choice
    svm_printables = {'method': 'SVM', 'param': 'C', 'ASCII': svm_ascii}
    svm_hypeparams = [1.0e-2, 1.0e-1, 1.0, 5.0, 1.0e1]
    svm_model, svm_inference, svm_accuracy = train_and_validate(X_train, Y_train, X_test, Y_test, svm, svm_hypeparams,
                                                                svm_printables)
    print_graphs(X_test, Y_test, svm_model, svm_printables)

    lr_ascii = """\n\

     _        _______ 
    ( \      (  ____ )
    | (      | (    )|
    | |      | (____)|
    | |      |     __)
    | |      | (\ (   
    | (____/\| ) \ \__
    (_______/|/   \__/
                

            """

    lr = lambda x: LogisticRegression(C=x, tol=1e-6, max_iter=1e10)
    lr_printables = {'method': 'Logistic Regression', 'param': 'C', 'ASCII': lr_ascii}
    lr_hypeparams = [1.0e-3, 1.0e-2, 1.0e-1, 1.0, 1.0e1, 1.0e2, 1.0e3, 1.0e4]
    lr_model, lr_inference, lr_accuracy = train_and_validate(X_train, Y_train, X_test, Y_test, lr, lr_hypeparams,
                                                             lr_printables)
    print_graphs(X_test, Y_test, lr_model, lr_printables)

    t = {'KNN': knn_accuracy, 'SVM': svm_accuracy, 'LR': lr_accuracy}
    # plt.bar(0, knn_accuracy)
    # plt.bar(1, svm_accuracy)
    # plt.bar(2, lr_accuracy)
    plt.ylim(94, 98)
    colors = ['darkorange', 'dodgerblue', 'limegreen']
    plt.title("Accuracy percentage (%)")
    plt.bar(t.keys(), t.values(), color=colors)
    plt.show()

    inference_times = {'KNN': knn_inference, 'SVM': svm_inference, 'LR': lr_inference}
    colors = ['darkorange', 'dodgerblue', 'limegreen']
    plt.title("Inference time (ms)")
    plt.bar(inference_times.keys(), inference_times.values(), color=colors)
    plt.show()
