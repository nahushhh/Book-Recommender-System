from flask import Flask, render_template, request, request_tearing_down
import numpy as np
import pickle
import pandas as pd

popular = pickle.load(open('top50.pkl', 'rb'))
similarity = pickle.load(open('similarity_scores.pkl', 'rb'))
final_df = pickle.load(open('final_df.pkl', 'rb'))
books_df = pickle.load(open('books_df.pkl', 'rb'))
list_of_books = pickle.load(open('list_of_books.pkl','rb'))
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("index.html", 
                                        book_name = list(popular['Book-Title'].values), 
                                        book_author = list(popular['Book-Author'].values),
                                        book_img = list(popular['Image-URL-S'].values),
                                        book_ratings = list(popular['Number of ratings'].values),
                                        book_avg_ratings = list(popular['Avg of ratings'].values))  

@app.route("/recommend")
def recommend(): 
    return render_template("rec.html")

@app.route("/recommend_books", methods=["post"])
def recommend_books(): 
    user_input = request.form.get('user_input')
    #print(user_input)
    index = np.where(final_df.index==user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for book in similar_books:
        item = []
        temp_df = books_df[books_df["Book-Title"]==final_df.index[book[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)
    print(data)
    return render_template('rec.html', data=data)

if __name__ == "__main__":
    app.run(debug=True) 