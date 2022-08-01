from flask import Flask, render_template, request
import joblib
import pickle
import sqlite3 as sql

vec = pickle.load(open("fakeReviewModel/countVector.pkl", "rb"))
fakeReview_model = pickle.load(open("fakeReviewModel/fakeReviews.pkl", "rb"))
pipeline = joblib.load("sentimentAnalysisPipeline.joblib")

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/product', methods=['GET'])
def product():

    users = []
    try:
        with sql.connect("database.db") as conn:
            # conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT * FROM reviews")
            rows = cur.fetchall()
        
        print("rows", len(rows))

        # convert row objects to dictionary
        count=0
        for i in rows:
            print(i[2])
            print(i[3])
            if(i[2] == 'Or' and i[3] == 'Positive'):
                count=count+1
                # print("hellooo")
            
        print("count", count)

    except:
        users = []
    # return users
    return render_template('product.html', reliability_score = (count/len(rows))*100, rows=rows)

@app.route("/reliability", methods=['POST', 'GET'])
def reliability():
   
    review = [x for x in request.form.values()]

    sdf = vec.transform(review)
    fakeDetect_result = fakeReview_model.predict(sdf)
    if fakeDetect_result[0]=='CG':
        fakeDetect_result[0]='Fake'
    else: 
        fakeDetect_result[0]='Original'
    
    result = pipeline.predict(review)

    try:
        with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO reviews (review, fakeDetect, sentimentDetect) VALUES (?,?,?)",(review[0], fakeDetect_result[0], result[0]) )
            
            con.commit()
            msg = "Record successfully added"
    except:
        con.rollback()
        msg = "error in insert operation"
    
    finally:
        return render_template('product.html', result = result, fake_predict = fakeDetect_result, msg=msg)
    



if __name__ == "__main__" :
    app.run(debug=True, port=8000)