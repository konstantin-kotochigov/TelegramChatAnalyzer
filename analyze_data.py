import pandas

filesdir = "/home/konstantin/Downloads/Telegram Desktop/ChatExport_14_01_2019 (3)"
df = pandas.read_csv(filesdir+"/df.csv", sep=";")

# Filter out foreign names
df['from_name_cnt']=df['from_name'].map(dict(df.from_name.value_counts()))
df = df[df.from_name_cnt > 1000]

from sklearn.feature_extraction.text import CountVectorizer, TfiddfVectorizer


cv = TfidfVectorizer(
    tokenizer = None,
    min_df=0.0005,
    max_df=0.75, 
    # stop_words = russian_stop_words, 
    lowercase=True, 
    ngram_range=(1,2))



X = df.text
y = df.from_name

X = cv.fit_transform(X)

# Visualize TF-IDF scores
word2index = dict([(v,k) for k,v in cv.vocabulary_.items()])
for i,x in enumerate(X[0].toarray()[0]):
    if x>0.0:
        print(word2index[i]+":"+str(x))

# Convert nominal target values
label_to_name = dict([(i,x) for i,x in enumerate(df.from_name.unique())])
name_to_label = dict([(x,i) for i,x in enumerate(df.from_name.unique())])
y = y.map(name_to_label)

from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB()

from sklearn.ensemble import GradientBoostingClassifier
gb = GradientBoostingClassifier()

parameters = {'max_depth':(2,4,6)}
cv = GridSearchCV(gb, parameters, cv=5, verbose=2)
cv.fit(X,y)
cv_results = cv.cv_results_
cv_table = pandas.DataFrame({"param":cv_results['params'], "error":cv_results['mean_test_score']}).sort_values(by="error", ascending=False)


message_stats = df.from_name.value_counts()



list(c.index[c>1000])


c = y.value_counts()
names_df = pandas.DataFrame({"cnt":c, "from_name":c.index})
names = names_df.from_name[names.cnt > 100]

label_dict = {}
for i,x in enumerate(names.values):
    label_dict[x] = i

time2 = time.time()
print(round((time2 - time1) / 60,2))

