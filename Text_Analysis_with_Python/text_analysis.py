#from PIL import Image
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from nltk import ngrams
import nltk
nltk.download('punkt')

st.write('## Analyzing Shakespeare texts')

st.sidebar.header('Word Cloud Settings')
maximum_word = st.sidebar.slider('Max Words', 10, 200, 100, 10)
max_font = st.sidebar.slider('Size of Largest Word', 50, 350, 60)
image_size = st.sidebar.slider('Image Width', 100, 800, 400, 10)
random = st.sidebar.slider('Random State', 30, 100, 42)

stop_words = st.sidebar.checkbox('Remove Stop words', value = True)
st.sidebar.header('Word Count Settings')
min_word = st.sidebar.slider('Minimum Count of words', 5, 100, 40)

# Creating a dictionary not a list 
books = {" ":" ","A Mid Summer Night's Dream":"data/summer.txt","The Merchant of Venice":"data/merchant.txt","Romeo and Juliet":"data/romeo.txt"}

book = st.selectbox("Choose a txt file", books)
image = books[book]

if image is not " ":
    with open(image) as f:
        dataset = f.read()

    stopwords = set(STOPWORDS)
    stopwords.update(['us', 'one', 'will', 'said', 'now', 'well', 'man', 'may',
    'little', 'say', 'must', 'way', 'long', 'yet', 'mean',
    'put', 'seem', 'asked', 'made', 'half', 'much',
    'certainly', 'might', 'came', 'o'])

tab1, tab2, tab3 = st.tabs(['Word Cloud', 'Bar Chart', 'View Text'])

with tab1:
    if image is not " ":
        if stop_words:
            cloud = WordCloud(background_color = "white", 
                                max_words = maximum_word, 
                                max_font_size=max_font, 
                                stopwords = stopwords, 
                                random_state=random)
        else:
            cloud = WordCloud(background_color = "white", 
                                max_words = maximum_word, 
                                max_font_size=max_font, 
                                random_state=random)
        wc = cloud.generate(dataset)
        word_cloud = cloud.to_file('wordcloud.png')
        st.image(wc.to_array(), width= image_size)

with tab2:
    if image is not " ":
        st.write("### Bar Chart of Minimun count of the Words")
        tokens = nltk.word_tokenize(dataset)
        word_tokens = [t for t in tokens if t.isalpha()]
        tokens_remove_sw = [word for word in word_tokens if not word.lower() in stopwords]
        if stop_words:
            frequency = nltk.FreqDist(tokens_remove_sw)
        else:
            frequency = nltk.FreqDist(word_tokens)
        
        freq_data = pd.DataFrame(frequency.items(),columns=['word','count'])
        sorted_data = freq_data.sort_values("count", ascending=False)
        data = sorted_data[ sorted_data.iloc[:,1]>= min_word ]  
        bar_plot = alt.Chart(data).mark_bar().encode(
            x='count:Q',
            y=alt.Y('word:N', sort='-x'),
            color = 'count',
            tooltip = ('word', 'count')
        )
        st.altair_chart(bar_plot, use_container_width=True)


with tab3:
    if image is not " ":
        st.write(dataset)
