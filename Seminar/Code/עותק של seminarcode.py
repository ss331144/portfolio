# -*- coding: utf-8 -*-
"""seminarCode.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/116PBLq_DPGIJou9obSOIlSw5MrQym7CG
"""

# @title Default title text
import numpy as np
import pandas
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords

"""הפונקציות-

טעינת נתונים

יצירת וקטור מרשימה

ניקוי מילים לא טובות
"""

def load_data(path):
  data = pandas.read_csv(path)
  data = pd.DataFrame(data)
  return data
########################################################################################################################

#change to vector
def create_vector_from_list(col_values):
  vectorizer = TfidfVectorizer()
  X = vectorizer.fit_transform(col_values)
  X = X.toarray()
  return X
########################################################################################################################

#delete unimprotant words
nltk.download('stopwords')
def clear_stopWord(col_val):
  stop_words = set(stopwords.words('english'))
  filtered_text = [word for word in col_val if word not in stop_words] # מוחק את המילים אם לא חשובות
  txt = " ".join(filtered_text)
  return txt
########################################################################################################################

sen = "I love coding with Python because it allows me to quickly build powerful."
print(f'convert try : \n {sen}')
print("="*180)
trySen=create_vector_from_list([clear_stopWord(sen.split())])
print(f'Vector of sentences : \n{trySen}')
print("="*180)
# חישוב מדדים שונים
try_mean = np.mean(trySen)           # ממוצע
try_median = np.median(trySen)       # חציון
try_std = np.std(trySen)             # סטיית תקן
try_var = np.var(trySen)             # שונות
try_min = np.min(trySen)             # ערך מינימלי
try_max = np.max(trySen)             # ערך מקסימלי
try_range = try_max - try_min        # טווח ערכים

# הדפסת התוצאות
print("Mean (ממוצע):", try_mean)
print("Median (חציון):", try_median)
print("Standard Deviation (סטיית תקן):", try_std)
print("Variance (שונות):", try_var)
print("Minimum Value (מינימום):", try_min)
print("Maximum Value (מקסימום):", try_max)
print("Range (טווח):", try_range)
print('='*180)
########################################################################################################################
"""העמודות הרלוונטיות"""
#in my data got column name - {'reviews.text'} , this column has more word uspite of {'reviews.title'}
text_col = 'reviews.title'
rating_col = 'reviews.rating'
########################################################################################################################


"""קריאת קובץ וטיפול בערכים חסרים וסינון"""

paths = [r'/Users/shryqb/PycharmProjects/PythonProject/some_running/my_seminal_code/עותק של Product Review Large Data.csv']
for path in paths:
  data = load_data(path)

first_df = pd.DataFrame(data) # df with all datas
columns = [#got the column i need from the data
    rating_col,   # דירוג המוצר
    text_col,   # כותרת הביקורת
]
df = first_df[columns] # create new df with choosen column
df = df.dropna(subset=[text_col]) #clean new df
#df = df.drop_duplicates()
rating_group = df.groupby(rating_col).count()
df = df[df[rating_col]<=3] # 3 rate is bad review - got proximity 2200 data
row , col = df.shape
cur_col_title = df[text_col]
cur_col_rating = df[text_col]
print(f'shape : {df.shape}')
print(rating_group)
print('='*180)
########################################################################################################################

"""גודל הנתונים הרלווטים"""

import numpy as np

# הצגת מידע כללי על הנתונים
print(f'נתונים: {df.shape[0]} שורות, {df.shape[1]} עמודות')

"""מדדים שונים של המצגת"""

rating_summary = df.describe()
print(rating_summary)


"""תדירות דירוגים"""

rating_frequencies = df[rating_col].value_counts().sort_index()
print("\nתדירות הדירוגים:")
print(rating_frequencies)
print('='*180)
########################################################################################################################

"""דוגמא של יצירת וקטור מהנתונים ואי שיוויון הוקטור"""

#example first 3 data
print(df.sample(3))
print('='*222)
vector_length = {}
for ii in range (3):
  i = df[text_col].iloc[(ii*4)%12]
  print(f'vector of title {ii+1} - {i}:')
  vecs = create_vector_from_list([clear_stopWord(i.split())])
  vector_length[ii+1] = len(vecs[0])
  print(vecs)
  print('='*222)
for i ,lenV in vector_length.items():
  print(f'vector {i} has len : {lenV} ')
print('=' * 180)
########################################################################################################################

"""שמירת הנתונים להצגה של הממוצע בדאטהפריים

"""

l = [] # new list for organize my specific data
help_l = [] # help for specific data

l.append (cur_col_title) # my first line
#clear and organize the review
for i,rev in enumerate(cur_col_title):
  clr = clear_stopWord(rev.split()) #clear
  vec = create_vector_from_list([clr]) # change vector
  help_l.append( np.mean(vec)) # add the mean of vector

l.append(help_l) # add the second line
########################################################################################################################

"""הצגת דאטה פריים של הממוצע"""

np_arr_proData = np.array(l).transpose()
pro_df_with_sentences = pd.DataFrame(np_arr_proData , columns=['sentences' , 'mean vector']).transpose()
print(pro_df_with_sentences)
print('='*180)
########################################################################################################################

"""יצירת וקטור דו ממדי כהכנה למודל"""

meanvec = np.array(l[1]) # got only the avg reviews data
meanvec_reshape = meanvec.reshape(-1,1) # organize data for kMean model
print(meanvec_reshape ) # print my data for kMean
print('='*180)
########################################################################################################################

"""המודל כמתודה"""

from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, classification_report, silhouette_score
import pandas as pd
import numpy as np

def kMean_model(n_class, new_ob , RandState):
    n_class = n_class
    rand_state = RandState

    # יצירת מודל KMeans
    kMean = KMeans(n_clusters=n_class, random_state=rand_state)
    my_k_mean = kMean.fit(meanvec_reshape)  # אימון המודל על הווקטורים
    sse = kMean.inertia_  # חישוב SSE (סכום ריבועים של שגיאות)

    # יצירת מילון עם תוצאות האשכולות
    dict_cluster = {}
    dict_cluster['mean vector'] = meanvec
    dict_cluster['cluster'] = my_k_mean.labels_
    dict_cluster_df = pd.DataFrame(dict_cluster)

    # מיזוג תוצאות האשכולות עם נתוני הביקורות
    final_dataClustering_whith_sen = pd.merge(pro_df_with_sentences.transpose(), dict_cluster_df, on='mean vector')
    copy_f = final_dataClustering_whith_sen.copy()

    # אם יש לך עמודת דירוג או קטגוריות אמיתיות להשוואה (כמו 'reviews.rating')
    if 'reviews.rating' in pro_df_with_sentences.columns:  # אם יש עמודת דירוג
        true_labels = pro_df_with_sentences['reviews.rating'].values
        cm = confusion_matrix(true_labels, my_k_mean.labels_)  # חישוב מטריצת בלבול
        report = classification_report(true_labels, my_k_mean.labels_)  # חישוב דוח
        print("Confusion Matrix:\n", cm)  # הצגת מטריצת בלבול
        print("\nClassification Report:\n", report)  # הצגת דוח

    # חישוב Silhouette Score - מדד פנימי לקיבוץ
    silhouette_avg = silhouette_score(meanvec_reshape, my_k_mean.labels_)
    print(f"\nSilhouette Score: {silhouette_avg:.4f}")

    # הצגת התוצאה הסופית
    print("\nFinal Data with Clusters:")
    print(final_dataClustering_whith_sen.head())

    new_pre = new_ob
    new_pre = clear_stopWord(new_pre.split())
    new_pre_vec = create_vector_from_list([new_pre])
    new_pre_vec = np.mean(new_pre_vec, axis=1).reshape(-1, 1)
    new_pre_cluster = kMean.predict(new_pre_vec)
    print(f'\nCluster for {new_ob}:\n predict : {new_pre_cluster[0]}')

    # החזרת תוצאות האשכולות וה-S|SE
    return copy_f, sse , my_k_mean
########################################################################################################################

"""יצירה של ביקורות רעות לסיווג לפי המודל"""
#מודל ליצירת תקייה
import os
bad_reviews = [
    "The product arrived damaged and doesn't work as expected. I'm very disappointed.",
    "The material feels cheap, and using the product leaves me feeling completely dissatisfied.",
    "It's not worth the price at all. It didn't meet my expectations.",
    "The performance quality is very low, I can't use it properly.",
    "The product doesn't match the description on the website, and it gave me a bad user experience.",
    "I wouldn't recommend it at all, the communication with customer service was terrible, and they didn’t help me at all.",
    "It doesn’t function properly. I really regret purchasing it.",
    "I expected a better design; this looks awful.",
    "It didn't live up to my expectations, the product arrived with technical issues that weren't resolved.",
    "The service is awful, and the product simply doesn’t work. I didn't get the value I expected."
]

"""הרצה של המודל על קי שונים ויצירת תקייה מיועדת לשמירה שלהם"""

sse = {}
folder_path = 'final_data'
os.makedirs(folder_path, exist_ok=True)

print('='*100)
for i in range(2,10):
  copy_f , sseK , k_mean_model  =kMean_model(i , bad_reviews[i%10] , 42)
  sse[i]=sseK
  try:
    file_path = os.path.join(folder_path, f'final data {i} clustering.csv')
  except Exception as e:
    print(e)
    break
  copy_f.to_csv(file_path , index=False , encoding='utf-8')
  print(f'cluster {i} done successfully')
  print(f'sse: {sseK}')
  print('='*100)
  print('='*100)
print(sse)
print('='*180)
########################################################################################################################
"""**הערת מרצה**: ✅

הרצת המודל לפי ראנדום סטייט ומרכזים משתנים.

"""
"""הצגת תוצאות של דאטהפריים של רנדום משתנה

"""
r_state = [0,6,12,25,42,200,300,None]
save_df_res = []
results = []
os.makedirs('different random state result', exist_ok=True)
for r_state_ in r_state:
  for i in range (2,9):
      print(f'--------------------------------r : {r_state_}--------------------------------')
      copy_f , sseK , k_mean_model  =kMean_model(i , bad_reviews[i] ,r_state_)
      # הוספת התוצאות לרשימה
      results.append({
          'random_state': r_state_ if not None else 'None',
          'k': i,
          'sse': sseK
      })
  # יצירת DataFrame עם התוצאות
  df_results = pd.DataFrame(results)
  df_results.to_csv(os.path.join(f'different random state result', f'rand_state = {r_state_}_.csv'))

  save_df_res.append(df_results)
  results = []
merged_df = pd.concat(save_df_res, ignore_index=True)
merged_df.to_csv(os.path.join(f'different random state result', f'all df merged with any random state.csv'))
print('dir with file of generated random state results in CSV format made successfully')
print('='*180)
########################################################################################################################
"""הצגת גרף המרפק"""

plt.plot(list(sse.keys()), list(sse.values()))
plt.xlabel("Number of cluster")
plt.ylabel("SSE")
plt.title("Elbow method")
plt.figure(figsize=(1,1))
plt.show()

poly_deg = 3
coeff = np.polyfit(list(sse.keys()), list(sse.values()), poly_deg)  # דרגת הפולינום 3
p = np.poly1d(coeff)
print(f'f(x) = \n\n')
print(f'{p}')


x_vals = np.linspace(min(sse.keys()), max(sse.keys()), 100)
y_vals = p(x_vals)

# Plotting
plt.plot(x_vals, y_vals, label=f'Polynomial Fit (Degree {poly_deg})', color='blue')
plt.scatter(sse.keys(), sse.values(), color='red', label='Data Points')
plt.title('Polynomial Fit')
plt.xlabel('X values')
plt.ylabel('Y values')
plt.legend()
plt.grid(True)
plt.show()
########################################################################################################################


#3D graph
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# נתונים לדוגמה
x_values = list(sse.values())  # רשימת ערכים (כמו בדוגמה שלך)
y_values = list(sse.keys())  # רשימת מפתחות (כמו בדוגמה שלך)
z_values = y_values  # נניח שהערכים של z הם כמו y_values, אך אפשר לשנות זאת לפי הצורך

# יצירת גרף
fig = plt.figure(figsize=(10, 7))

# הוספת גרף תלת-מימדי
ax = fig.add_subplot(111, projection='3d')

# הצגת הנתונים בגרף תלת-מימדי
scatter = ax.scatter(x_values, y_values, z_values, c=z_values, cmap='viridis', marker='o', s=100)

# הגדרת כותרות לצירים
ax.set_xlabel('X - Clusters')
ax.set_ylabel('Y - SSE')
ax.set_zlabel('Z - Additional Metric')  # כותרת של ציר Z
ax.set_title('Elbow Method 3D')
########################################################################################################################

# הוספת בר צבע (Color Bar) כדי להציג את המשמעות של הצבעים
fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
# הוספת רשת
ax.grid(True)

# הצגת הגרף
plt.show()
########################################################################################################################
"""פתרון של הפונקציה ומציאות המספר בין קיצונים"""

import sympy
x = sympy.Symbol('x')
fun = ''
for i,conf in enumerate(p):
  fun += str(conf)+ f'*x**{poly_deg - i}+'
fun = fun[:-1]
sympy_fun = sympy.sympify(fun)
diff_x = sympy.diff(sympy_fun, x)
proof = sympy.solve(diff_x, x)
print('---------proof of polynomial function--------')
print(proof)
print('='*188)
########################################################################################################################
"""מדדים שונים
"""
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score

# הנחות:
# meanvec_reshape הוא המערך המכיל את הנתונים שלך לאחר המרת הטקסט לווקטור

def evaluate_clustering(X, n_clusters=3):
    # יצירת המודל
    kMeans = KMeans(n_clusters=n_clusters, random_state=42)
    kMeans.fit(X)

    # חישוב SSE
    sse = kMeans.inertia_

    # חישוב מדדים אחרים
    silhouette_avg = silhouette_score(X, kMeans.labels_)
    db_index = davies_bouldin_score(X, kMeans.labels_)
    ch_index = calinski_harabasz_score(X, kMeans.labels_)

    # הצגת התוצאות
    print(f"Number of clusters: {n_clusters}")
    metrics = {
    'SSE': [sse],
    'Silhouette Score': [silhouette_avg],
    'Davies-Bouldin Index': [db_index],
    'Calinski-Harabasz Index': [ch_index]
    }

# יצירת DataFrame
    metrics_df = pd.DataFrame(metrics)

# הצגת ה-DataFrame
    os.makedirs('index data', exist_ok=True)
    metrics_df.to_csv(os.path.join('index data', f'metrics with index k={n_clusters}.csv'))

    return sse,silhouette_score,db_index,ch_index

########################################################################################################################
"""הרצת הפונקציה של המדדים"""
print('='*188)
print('-------- find best k ------------')
L = []
try:
  for key,val in sse.items():
    if proof[0]<key<proof[1]: #if the proofs are imaginary number we got exception
      print(f'best cluster is {key} , sse : {val}\n\n')
      evaluate_clustering(meanvec_reshape, n_clusters=key)
      break
except Exception as e:
  evaluate_clustering(meanvec_reshape , n_clusters=6)
# יצירת גרף קו של SSE
sse_dict = sse
########################################################################################################################
"""סכום שגיאות לפי קלאס בגרף

"""

import numpy as np
import seaborn as sns

# יצירת Heatmap של SSE
sse_matrix = np.array(list(sse_dict.values())).reshape(-1, 1)
plt.figure(figsize=(8, 6))
sns.heatmap(sse_matrix, annot=True, cmap='coolwarm', fmt='.2f', cbar=True)
plt.xlabel('Clusters')
plt.ylabel('SSE')
plt.title('Heatmap of SSE for Different Number of Clusters')
plt.show()
print('='*188)
########################################################################################################################
"""הרצה לפי הקלאסטר שבחרתי

"""
print('--------------running by calculated K--------------------')
six_clus_path = fr'final_data/final data {key} clustering.csv'
print(f'choose file {key} clusters')
df_for_reg = load_data(six_clus_path)
print(df_for_reg.columns)
cur_col = ['mean vector' ,'cluster']
red_data_df = df_for_reg[cur_col]
print('='*188)
########################################################################################################################
"""יצירת עץ ויזואלי לממוצע של משפט"""

from sklearn.tree import DecisionTreeRegressor, plot_tree
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

def decision_tree(df):
    # הכנת הנתונים (פיצ'ר: 'mean vector', מטרה: 'cluster')
    X = df[['mean vector']].values  # פיצ'ר
    y = df['cluster']  # משתנה יעד (קלאסטר)

    # חילוק לסטים של אימון ובדיקה
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # יצירת המודל
    model = DecisionTreeRegressor(random_state=42)
    model.fit(X_train, y_train)

    # חיזוי על נתוני הבדיקה
    y_pred = model.predict(X_test)

    # חישוב MSE ו-R^2
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    #print(f'Mean Squared Error (MSE): {mse:.40f}')
    #print(f'R-squared (R^2): {r2:.40f}')



    # הצגת עץ ההחלטות
    plt.figure(figsize=(12,8))
    plot_tree(model, filled=True, feature_names=['mean vector'], fontsize=10 , max_depth=None)
    plt.title("Decision Tree Structure")
    plt.show()
    return model
# הפעלת הפונקציה

model = decision_tree(df_for_reg)
print('='*188)
########################################################################################################################
"""מילים מרכזיות לכל קלאסטר"""

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
print('main word in ant classification : ')


def find_top_words(df, top_n=5):
    cluster_top_words = {}

    for cluster in df["cluster"].unique():
        cluster_data = df[df["cluster"] == cluster]

        # חישוב מרכז הקלאסטר
        cluster_center = np.mean(np.vstack(cluster_data["mean vector"]), axis=0)

        # חישוב דמיון קוסינוס עבור כל המילים
        similarities = cosine_similarity(np.vstack(cluster_data["mean vector"]), [cluster_center]).flatten()

        # מיון האינדקסים של המילים לפי הדמיון
        top_indices = np.argsort(similarities)[::-1][:top_n]

        # בחירת המילים המובילות
        top_words = cluster_data.iloc[top_indices]["sentences"].tolist()

        # שמירת התוצאה
        cluster_top_words[cluster] = top_words

    return cluster_top_words

# קבלת 5 המילים המייצגות
top_words = find_top_words(df_for_reg, top_n=5)
copy_top_w = top_words.copy()
# הדפסת התוצאה
print("Top Words per Cluster:")
for cluster, words in sorted(top_words.items()):
    words = np.unique(words)
    print(f"Cluster {cluster}: {', '.join(words)}")
os.makedirs(f'top words', exist_ok=True)
df_top_words = pd.DataFrame(top_words)
df_top_words.to_csv(os.path.join('top words', f' for k={key}.csv'))
print('='*188)






########################################################################################################################
"""הצגת חיזוי מותאם אישית מתוך ליסט ביקורות"""
print('predict sentence : ')
pre_sen = bad_reviews[2]
pre_Sen = pre_sen
# הסרת stopwords
pre_sen = clear_stopWord(pre_sen.split())

# יצירת וקטור מהמשפט
pre_sen_vector = create_vector_from_list([pre_sen])

# הצגת הווקטור (תצוגה של המימדים)
print(f'The vector of sentences: {pre_sen_vector}')

# אם הווקטור דו-ממדי (כמו [ [1.5, 2.3, 0.1] ]), הפוך אותו לוקטור חד-ממדי
pre_sen_vector = np.mean(pre_sen_vector, axis=1).reshape(-1, 1)

# הצגת הווקטור שהפך להיות חד-ממדי
print(f'The reshaped vector: {pre_sen_vector}')

# חיזוי באמצעות המודל
prediction = model.predict(pre_sen_vector)
print(pre_Sen)
print(f'Prediction: {prediction[0]}')
########################################################################################################################
