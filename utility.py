#for reading data
import pandas as pd

#for computation
import numpy as np

#for preprocessing nd text cleaning
import nltk
import re
import contractions
nltk.download('stopwords')
#import english stopwords
from nltk.corpus import stopwords

#instantiate stopwords for english words
stop_words = stopwords.words('english')

nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer

# Create a WordNetLemmatizer object
wnl = WordNetLemmatizer()


#to display wordcloud
from wordcloud import WordCloud, STOPWORDS

#for other visualization
import seaborn as sns
import matplotlib.pyplot as plt

#to connect to the datawarehouse
# import cx_Oracle as cx

def file_reader(path):
    import pandas
    """
    reads the file as an excel file
    
    args:
        path: specified file path
    returns:
        excel file as a dataframe
    """
    data = pandas.read_excel(path)
    return data

# def dbms_connector(user, pw, dsn):
#     """
#     connect to the DBMS using specified connection parameters
#     """
#     # user = 'Bianalytics'
#     # pw = 'password10$'
#     # dsn = 'AB01DWDB-SCAN1:6655/DWH'
#     # dsn_tns = cx.makedsn('10.111.60.40', '1421', service_name='dwh')

#     path = r"C:\Users\TabansiJ\Downloads\instantclient-basic-windows.x64-21.12.0.0.0dbru\instantclient_21_12"

#     cx.init_oracle_client(lib_dir=path)

#     connection = cx.connect(
#     user=user,
#     password=pw,
#     dsn =dsn   
#     )

#     try:
#         c  = connection.cursor()
#         print("Connection Successful")
#     except:
#         print("connection failed")

#     return c




def labeled_barplot(data, feature, perc=False,n=None):
# """this function will plot a labelled count plot for the feature
# data:dataframe
# feature: column
# perc: boolean, percentage value to be displayed
# n: int, display top n category"""
    total = len(data[feature])
    count= data[feature].nunique()

    if n is None:
        plt.figure(figsize=(count, 5))
    else:
        plt.figure(figsize=(n+1, 5))
    plt.title(feature + " countplot")

    plt.xticks(rotation=90, fontsize=15)
    plt.yticks(fontsize=15)
    ax = sns.countplot(
            data=data,
            x=feature,
            order = data[feature].value_counts().index[:n].sort_values(),
        palette="Paired")

    for i in ax.patches:
        if perc == True: #if percentage is true
            label = "{:.2f}%".format(#display the format as 2 digits after the dot
            (i.get_height()/total) * 100) #convert the height value to percentage
        else:
            label = i.get_height() #if perc is false display on height value

        x = i.get_x() + i.get_width() / 2  # width of the plot
        y = i.get_height()  # height of the plot

        ax.annotate(text=label, xy=(x, y), #display label on cordinates x_ax, y
                    va="center", ha="center", #align it to the center of both vertical and horizontal axis
                    xytext = (0,5), #gap between the text relative to the bars
                    textcoords="offset points")
    plt.show()


def WordCloudGen(data, label):
    """
    this function generates a word cloud based on the specified comment class
    data: dataframe
    label: category  {'half-true': 2, 'false': 1, 'mostly-true': 3, 'true': 5, 'barely-true': 0, 'not-known': 4}
    """
    # step 1: filter the dataset based on the label
    df = data[data['Labels'] == label] #this will return a subset of the data with specified label

    # step 2: join the words in the text
    combined_text = " ".join(df['Text'])

    # step 3: intialize the wordcloud
    wcloud = WordCloud(stopwords=STOPWORDS, random_state=14, width=3000, height=2500,).generate(combined_text)

    # set the figure
    plt.figure(1, figsize=(12,12))

    # display the wordcloud image
    plt.imshow(wcloud, interpolation='bilinear')

    # off the axis
    plt.axis('off')

    # show the plot
    plt.show()

def contraction_fixer(text):
    """
    This function fixes the contractions found in the sentence and returns text with no contractions.
    Text: string of words
    """
    clean_text = contractions.fix(text)
    return clean_text

def text_cleaner(text):
    """
    This function removes unwanted characters such as: digits and punctuation marks, extra
    whitespaces & special charcaters found in the text.
    it will return only uppercase and lowecased alphabets.
    text: string of words
    """
    cleaned_text = re.sub(pattern = "[^a-zA-Z]", repl=" ", string=text)
    cleaned_text = re.sub(pattern = "\s+", repl=" ", string=cleaned_text)
    return cleaned_text

def lowercase(text):
    """
    returns a lowercased string of text.
    text: string of words
    """
    # step1: lowercase each word in the list of tokens
    lowercased_tokens = [word.lower() for word in text.split()]
    # step 2: join the words together
    lowercased_text = " ".join(lowercased_tokens)
    # step 3: return text
    return lowercased_text


def stopword_remover(text):
    """
    the function removes stopwords found in the text and returns the remaining word
    text: string of words
    """
    # remove the word if the word is a stopword
    cleaned_tokens = [word for word in text.split() if word not in stop_words]


    #join the remiaining words back together
    cleaned_text = " ".join(cleaned_tokens)

    # return the cleaned text
    return cleaned_text

def lemmatizer(text):
    
    """
    the function lemmatize the words in the comment
    text: string of words
    """
    # lemmatize each word
    lemmatized_tokens = [wnl.lemmatize(word) for word in text.split()]

    # join the remiaining words back together
    lemmatized_text = " ".join(lemmatized_tokens)

    # return the lemmatized text
    return lemmatized_text

def remove_punctuation(text):
    import string
    cleaned_tokens = [word for word in text.split() if word not in string.punctuation]

    # join the remiaining words back together
    cleaned_text = " ".join(cleaned_tokens)

    return cleaned_text


def histogram_boxplot(data, feature, figsize=(9, 5), kde=False, bins=None):
    """
    Boxplot and histogram combined

    data: dataframe
    feature: dataframe column
    figsize: size of figure (default (12,7))
    kde: whether to show the density curve (default False)
    bins: number of bins for histogram (default None)
    kind: specifies if a histogram or countplot should be plotted
    """
    
    f1, (ax_box, ax_hist) = plt.subplots(2, 1, #fig should appear in a 2 rows and 1 column style
                                     #nrows=2, #number of rows on grid = 2
                                    sharex = True, # share the x column
                                    gridspec_kw={"height_ratios": (0.25, 0.75)},
                                        figsize = figsize)

    # plot the boxplot
    # boxplot will be created and a star will indicate the mean value of the column
    sns.boxplot(data=data, x=feature, ax=ax_box, showmeans=True, color="mediumturquoise")
    
        #plot the hisstogram
    if bins != None:
            #if bins is specified
        sns.histplot(data=data, x=feature, kde=kde, ax=ax_hist, bins=bins, color="mediumpurple")
    else:
            #if bins is not specified
        sns.histplot(data=data, x=feature, kde=kde, ax=ax_hist, color="mediumpurple")

        ax_hist.axvline(data[feature].mean(), color="green", linestyle="--")  # Add mean to the histogram

        ax_hist.axvline(data[feature].median(), color="black", linestyle="-")  # Add median to the histogram
    
