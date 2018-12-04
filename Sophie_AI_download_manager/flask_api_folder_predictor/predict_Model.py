import pandas as pd
import numpy as np
import os
import glob
import random
import string
import html
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.exceptions import NotFittedError

def ModelIt(file_names_input, root_dir, downloads_dir):
    print(root_dir, downloads_dir)
    root_dir = root_dir
    downloads_dir = downloads_dir


    if root_dir[-1] != '/':
        root_dir = root_dir + '/'
    if downloads_dir[-1] != '/':
        downloads_dir = downloads_dir + '/'

    if os.path.exists('root_dir'):
        root_dir_pickled = pickle.load(open('root_dir', 'rb'))
        if root_dir_pickled != root_dir:
            model_train(root_dir)
            symbolic_link_create(root_dir,downloads_dir)
    else:
        model_train(root_dir)


    if os.path.exists('downloads_dir'):
        downloads_dir_pickled = pickle.load(open('downloads_dir', 'rb'))
        if downloads_dir_pickled != downloads_dir:
            symbolic_link_create(root_dir,downloads_dir)
    else:
        symbolic_link_create(root_dir,downloads_dir)


    pickle.dump(root_dir, open('root_dir', 'wb'))
    pickle.dump(downloads_dir, open('downloads_dir', 'wb'))

    path_pred = model_predict(file_names_input)
    return path_pred




def symbolic_link_create(root_dir, downloads_dir):
    dst = downloads_dir + 'symlink_folder'
    if os.path.exists(dst):
        os.unlink(dst)
    os.symlink(root_dir, dst)
    print(root_dir,'\n',dst)
    return



def model_train(root_dir):
    if root_dir == '':
        return

    root_dir = root_dir
    data = []
    for filename in glob.iglob(root_dir + '**/*', recursive=True):
         data.append(os.path.relpath(filename, root_dir))
    #print(data)
    data_split = list(map(lambda x: os.path.normpath(x).split(os.sep), data))
    data_drop_single = list(filter(lambda x: len(x)>1, data_split)) #change to len(x)>1 since solver needs >=2 classes!!!!
    file_name = list(map(lambda x: x[-1], data_drop_single))
    file_name_html = [html.unescape(x) for x in file_name]
    file_name_underscore = [x.lower().replace("_", " ") for x in file_name_html]
    file_name_word_split = [re.findall(r"[\w']+", x) for x in file_name_underscore]
    file_name_final = [' '.join(x) for x in file_name_word_split]

    file_labels = list(map(lambda x: x[:-1], data_drop_single))
    df_labels = pd.DataFrame(data = file_labels)
    df_paths = pd.DataFrame(data = df_labels[0])
    for i in range(1, df_labels.shape[1]):
        df_paths[i] = df_labels[i]

        df_paths.loc[pd.notna(df_labels[i]), i] = df_paths[i-1].map(str) + '/' + df_paths[i]

    df_paths.replace('None', np.nan, inplace=True)
    df_paths[-1] = 'dummy'
    df_paths = df_paths.astype('category', copy = False)

    # count_vect = CountVectorizer(min_df=8, encoding='latin-1', \
    #                 ngram_range=(1, 2), stop_words='english')
    #
    # X_train_counts = count_vect.fit_transform(file_name_final)
    # features = X_train_counts.toarray()

    tfidf = TfidfVectorizer(sublinear_tf=True, min_df=8, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
    features = tfidf.fit_transform(file_name_final).toarray()

    depth = df_paths.shape[1]
    folder_each_level = [df_paths[x].cat.categories.tolist() for x in range(-1,df_paths.shape[1]-1)]

    #print(folder_each_level)

    clf = [[LogisticRegression(random_state = 0) for _ in range(len(folder_each_level[x]))] \
           for x in range(len(folder_each_level))]

    for i in range(len(folder_each_level)-1):
        for j in range(len(folder_each_level[i])):

            # input control
            ind = ((df_paths[i-1] == folder_each_level[i][j]) & (df_paths[i].notna())) # remove NAN paths at the same time

            # category / labels control: next col of df_paths
            features_level = features[ind] # just pick the corresponding entries
            labels_level = np.asarray(df_paths[i][ind], dtype="str")

            if len(np.unique(labels_level)) > 1 and len(labels_level)>5:
                clf[i][j] = LogisticRegression(random_state = 0)
                clf[i][j].fit(features_level, labels_level)

    pickle.dump(clf, open('clf_folder_picker', 'wb'))
    #pickle.dump(count_vect, open('count_vect', 'wb'))
    pickle.dump(folder_each_level, open('folder_each_level', 'wb'))
    pickle.dump(tfidf, open('tfidf', 'wb'))

def model_predict(file_names_input):
    prob_threshold = 0.8

    clf = pickle.load(open('clf_folder_picker', 'rb'))
    #count_vect = pickle.load(open('count_vect', 'rb'))
    tfidf = pickle.load(open('tfidf','rb'))
    folder_each_level = pickle.load(open('folder_each_level', 'rb'))



#     folder_each_level = [df_paths[x].cat.categories.tolist() for x in range(-1,df_paths.shape[1]-1)]

    preds = []
    for file_name_input in [file_names_input]:
        #vect_name = count_vect.transform([file_name_input])
        vect_name = tfidf.transform([file_name_input])
        y_pred =  ['' for _ in range(len(folder_each_level)-1)]
        prob = [0 for _ in range(len(folder_each_level)-1)]
        prob_total = 1

        current_folder = 'dummy'
        for i in range(len(folder_each_level)-1):
            for j in range(len(folder_each_level[i])):
#                 print(i,j)

                if current_folder != folder_each_level[i][j]: #make sure it is the right subfolder
                    continue

#                 print('folder_each_level:',folder_each_level[i][j])
#                 print('current_folder:', current_folder)

                try:
                    clf[i][j].predict(vect_name)
                except NotFittedError as e:
                    #print('error')
                    break

                y_pred[i] = clf[i][j].predict(vect_name)[0]
                current_folder = y_pred[i]
                prob[i] = np.max(clf[i][j].predict_proba(vect_name))
                prob_total *= prob[i]

#                     print(y_pred[i], prob[i], prob_total,'\n')



            if prob_total < prob_threshold:
                break

        # if i > 0 and back up a level if prob_total < prob_threshold:
        if (i > 0) and (prob_total < prob_threshold):
            pred_folder = y_pred[i-1]
            level = i
        else:
            pred_folder = y_pred[i]
            level = i+1

        # when there is no pretrained clf available at this level
        if pred_folder == '':
            #print(i, j, current_folder,'\n', y_pred[i-2], y_pred[i-1])
            pred_folder = current_folder
        preds.append((pred_folder, level))
    print(file_name_input)
    path_pred = preds[0][0]
    return 'symlink_folder' + '/' +path_pred + '/' + file_name_input
