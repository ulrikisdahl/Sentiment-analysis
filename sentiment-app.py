import pickle
import string
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask import Flask, render_template, request, jsonify, after_this_request
from nltk.corpus import stopwords

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

model_path = 'model.h5'
tokenizer_path = 'tokenizer.pickle'
max_len = 150
prediction_dict = {0: 'Positive review', 1: 'Negative review'}
stop_words = set(stopwords.words('english'))

# #Loading the tokenizer
with open(tokenizer_path, 'rb') as handle:
    tokenizer = pickle.load(handle)

#initializing the model
model = tf.keras.models.load_model(model_path)

#Cleaning and tokenizing the review text in the same way as in the data preprocessing 
def clean(sentence):
    punctuations = str.maketrans('', '', string.punctuation) #remove punctuations from the sentences
    sentence_stopwords = ''
    for word in sentence[0].split(' '):
        if word not in stop_words: #Removes stopwords
            sentence_stopwords += word + " "
    sentence_cleaned = sentence_stopwords.translate(punctuations)
    return sentence_cleaned

def text_to_padded(text):
    cleaned_text = clean(text)
    seq = tokenizer.texts_to_sequences([cleaned_text])
    padded_seq = pad_sequences(seq, maxlen=max_len, padding='post')
    padded_seq = np.array(padded_seq)
    return padded_seq


#function that listens to 'api' and returns the predictions from the model
@app.route('/api', methods=['POST', 'GET'])
def main():
    data = request.get_json() #respone from client side

    padded_sequence = text_to_padded(data)
    y_pred = model.predict(padded_sequence)
    y_pred_rounded = round(y_pred[0][0])
    predicted_sentiment = prediction_dict[y_pred_rounded]

    return jsonify({'result': predicted_sentiment})


if __name__ == "__main__":
    app.run()


#Example reviews:
#The food was average. The waiters were not nice either. I did not find this place exciting
#The service was a little bit disappointing. However the food was great and the atmosphere was also very good. I would recommend it
