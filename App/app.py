import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from docx import Document
import streamlit as st
import pandas as pd
import stylecloud
import string
import nltk

# Download necessary NLTK data for stopwords and tokenization
nltk.download("stopwords")
nltk.download("punkt")

def preprocess(text: str, lang="turkish"):
    # Get stopwords for the specified language
    stop_words = set(stopwords.words(lang))
    # Remove punctuation marks from the text
    text = text.translate(str.maketrans("", "", string.punctuation))
    # Tokenize the text into words
    text = word_tokenize(text.capitalize(), language=lang)
    # Remove stopwords from the tokenized words
    text = [i for i in text if i not in stop_words]
    return " ".join(text)  # Join the words back into a single string

def generate(text, icon):
    output = "word_cloud.png"  # Output file name for the word cloud image
    stylecloud.gen_stylecloud(
        text=text,
        background_color='black',
        icon_name=icon,  # Icon used for the word cloud
        output_name=output
    )
    return output  # Return the name of the generated output file


st.title("Word Cloud Generator")

icons_list = pd.read_csv("icons.csv")

icon = st.selectbox("Select an icon", icons_list["icon"])

language = st.selectbox("Select an language", ["turkish", "english"])

file = st.file_uploader("Upload a text file", type=["txt", "docx"])

if st.button("Generate"):
    try:
        text = ""
        # Check if the uploaded file is a .docx file
        if file.name.endswith(".docx"):
            doc = Document(file)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        # Check if the uploaded file is a .txt file
        elif(file.name.endswith(".txt")):
            text = file.read().decode("utf-8")
    
    except Exception as e:
        st.error(f"File is not readable: {e}")
    
    try:
        # Get the icon code corresponding to the selected icon
        icon = icons_list[icons_list["icon"] == icon]["code"].values[0]
        # Preprocess the text (remove stopwords, punctuation, etc.)
        text = preprocess(text, language)
        # Generate the word cloud image
        png = generate(text, icon)
    
    except Exception as e:
        st.error(f"Word cloud is not generated: {e}")
    
    try:
        image = plt.imread(png)
        st.image(image)

    except Exception as e:
        st.error(f"Image is not showed: {e}")  # Display error if the image cannot be shown
