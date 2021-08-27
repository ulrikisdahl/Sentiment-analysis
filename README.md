# Sentiment-analysis
This is a sentiment analysis app where the aim is to classify whether a restaurant review is positive or negative

#
Demo: http://sentiment-analysis-v2.herokuapp.com/ (It takes 30 seconds for the page to load the first time you click the link)

Notebook: https://github.com/Ulisman/Sentiment-analysis/blob/main/Sentiment_analysis.ipynb

## Architecture
The model uses a LSTM layer (long-short-term-memory) combined with two dense layers (where the second dense layer is the output layer which uses a sigmoid activation function becuase this is a binary classification task)

## Results

![Screenshot 2021-08-26 at 18 21 34](https://user-images.githubusercontent.com/42532774/130999486-fa2aa399-4678-4b0b-8a3d-0e8845f71403.png)

The validation accuracy (yellow) stagnated after 8 epochs at around 87%
#

![Screenshot 2021-08-26 at 20 12 29](https://user-images.githubusercontent.com/42532774/131014446-9a479c75-451b-41b1-a6ca-6f09e5e40409.png)

The validation loss stopped decreasing noticably after the 4th epoch and started to slowly increase which indicates that the model was starting to overfit. However, overfitting is very common in NLP tasks so this was to be expected

## Motivation
The goal of this project was to create a NLP model with data that I collected on my own (by webscraping review websites), because I wanted to get a understanding of how challenging it is to work with your own data. After finishing the project, my conclusion was that the biggest challenge in working with your own dataset is to find enough data. This is why i had to combine the 5 labels that i had originally intended on using (these labels represented the ratings from 1 to 5 stars) in to two labels (positive or negative), hence making it a binary classification task.
