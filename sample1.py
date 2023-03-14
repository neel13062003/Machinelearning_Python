import json
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# read in the data from CSV
data = pd.read_csv('pizza.csv')

# preprocess the data
data['pizzaName'] = data['pizzaName'].apply(lambda x: x.lower()) # convert to lowercase
data['pizzaDesc'] = data['pizzaDesc'].apply(lambda x: x.lower()) # convert to lowercase

# create a TF-IDF vectorizer
tfidf_vectorizer = TfidfVectorizer()

# fit and transform the vectorizer on the preprocessed data
tfidf_matrix = tfidf_vectorizer.fit_transform(data['pizzaName'] + ' ' + data['pizzaDesc'])

# save the tfidf_vectorizer and cosine_sim_matrix objects to disk
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.joblib')
cosine_sim_matrix = cosine_similarity(tfidf_matrix)
joblib.dump(cosine_sim_matrix, 'cosine_sim_matrix.joblib')

# load the tfidf_vectorizer and cosine_sim_matrix objects
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')
cosine_sim_matrix = joblib.load('cosine_sim_matrix.joblib')

# take user input
#user_input = 'Well Amla'
user_input = sys.argv[1]
#user_input = 'Wipes'

# preprocess the user input
user_input = user_input.lower()

# get the index of the user input
input_index = data[data['pizzaName'] == user_input].index[0]

# calculate the cosine similarity matrix
cosine_sim_matrix = cosine_similarity(tfidf_matrix)

# get the top 5 most similar products
similar_products = list(enumerate(cosine_sim_matrix[input_index]))
sorted_similar_products = sorted(similar_products, key=lambda x:x[1], reverse=True)[1:6]
top_5_product_indices = [i[0] for i in sorted_similar_products]

# get the product names and prices
# output_data = []
# for i in top_5_product_indices:
#     output_data.append({"name": data.loc[i, "pizzaName"], "price": data.loc[i, "pizzaPrice"], "desc": data.loc[i, "pizzaDesc"].replace("\r\n", "\\r\\n")})

output_data = []
for i in top_5_product_indices:
    # output_data.append({"name": data.loc[i, "pizzaName"], "price": int(data.loc[i, "pizzaPrice"]), "desc": data.loc[i, "pizzaDesc"]})
    output_data.append({"name": data.loc[i, "pizzaName"], "price": int(data.loc[i, "pizzaPrice"]),
                        "id": int(data.loc[i, "pizzaId"]),"price1": int(data.loc[i, "pizzaPrice1"]),"price2": int(data.loc[i, "pizzaPrice2"]), "desc": data.loc[i, "pizzaDesc"]})

json_output = json.dumps(output_data)
print(json_output)


# print(type(output_data))
# output_string = json.dumps(output_data)
# print the output
# print(output_data)
# print(output_string)