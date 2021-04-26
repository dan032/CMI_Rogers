import pandas as pd
import os
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, GridSearchCV

from sklearn.preprocessing import MultiLabelBinarizer


data = []
outputs_dir = os.path.join(os.getcwd(), "outputs")


for file in os.listdir(outputs_dir):
    df = pd.read_csv(os.path.join(outputs_dir, file))
    df = df.dropna()
    df = df.drop(["Frame Number", "time_relative"], axis=1)

    df['IMSI'] = df['IMSI'].astype(str)
    df['enb_ue_s1ap_id'] = df['enb_ue_s1ap_id'].astype(str)
    df['mme_ue_s1ap_id'] = df['mme_ue_s1ap_id'].astype(str)

    df = pd.concat([df.drop('protocols', 1), df['protocols'].str.get_dummies(sep="|")], 1)
    df = pd.concat([df.drop('cellidentity', 1), df['cellidentity'].str.get_dummies()], 1)
    df = pd.concat([df.drop('enb_ue_s1ap_id', 1), df['enb_ue_s1ap_id'].str.get_dummies()], 1)
    df = pd.concat([df.drop('mme_ue_s1ap_id', 1), df['mme_ue_s1ap_id'].str.get_dummies()], 1)
    df = pd.concat([df.drop('IMSI', 1), df['IMSI'].str.get_dummies()], 1)
    print('')

    clf_params = [
        # Models and Parameters go here
    ]

    pipeline = Pipeline(steps=[('clf', )]) # Add initial classifier when done

    # The code below is for if we end up using supervised learning models, need to research how to use GSV
    # with unsupervised learning

    # gscv = GridSearchCV(pipeline, param_grid=clf_params, verbose=2, n_jobs=20, scoring="f1", cv=3)
    # gscv.fit(X_train, y_train)
    #
    # best_estimator = gscv.best_estimator_
    # best_params = gscv.best_params_
    # y_pred = best_estimator.predict(X_test)
    #
    # training_accuracy_score = accuracy_score(y_train, best_estimator.predict(X_train))
    # testing_accuracy_score = accuracy_score(y_test, y_pred)
    # plot_confusion_matrix(best_estimator, X_test, y_test, display_labels=[], normalize="true")
    # plt.show()
    #
    # print(f"Training Score: {training_accuracy_score}")
    # print(f"Test Score: {testing_accuracy_score}")
    # print(classification_report(y_test, y_pred))
    # print(f"Best Estimator: {best_estimator}")

