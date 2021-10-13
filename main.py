from flask import Flask, request
from pymongo import MongoClient


app = Flask(__name__)

client = MongoClient ()
db = client.moneylionTest
featureAccessCollection = db.featureAccess


@app.route('/feature',methods = ['POST'])
def insert_data():
    # catch the insert fail error
    try:
        data = request.get_json()
        db_data = featureAccessCollection.find({"email":data["email"], "featureName":data["featureName"]})
        if db_data.count() > 0:
            featureAccessCollection.update(
                {"_id":db_data[0]["_id"]},
                {
                    "$set":data
                }
            )
        else:
            featureAccessCollection.insert_one(data)
        return "", 200
    except Exception:
        return "Http Status Not Modified", 304


@app.route('/feature',methods = ['GET'])
def get_eligibility():
    try:
        data = request.values
        email = data.get("email")
        featureName = data.get("featureName")

        data = featureAccessCollection.find({"email":email, "featureName":featureName})[0]
        if data["enable"]:
            return {"canAccess":True}
        else:
            {"canAccess":False}

    except IndexError:
        return "Email or Feature Name is invalid"
    

if __name__ == "__main__":
    app.run(debug=True)