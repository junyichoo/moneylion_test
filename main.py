from flask import Flask, request
from pymongo import MongoClient



# Initialise the flask app
app = Flask(__name__)

# Initialise the local mongodb client
client = MongoClient ()
db = client.moneylionTest # specify the database
featureAccessCollection = db.featureAccess # specify the collection


@app.route('/feature',methods = ['POST'])
def insert_data():
    """
    This function is to update the 'enable' value given the email and the feature name. If there exist no such email and feature name, then a new data will be created to the database
    """
    try:

        # retrieve the json data from the POST request
        data = request.get_json()
        # Look through the database to see if we have the corresponding data
        db_data = featureAccessCollection.find({"email":data["email"], "featureName":data["featureName"]})
        
        # If the current email and featureName exist in the database then we would update the data
        if db_data.count() > 0:
            featureAccessCollection.update(
                {"_id":db_data[0]["_id"]},
                {
                    "$set":data
                }
            )

        # If the current data does not exist we create a new one
        else:
            featureAccessCollection.insert_one(data)

        return "", 200

    except Exception:
        return "Http Status Not Modified", 304


@app.route('/feature',methods = ['GET'])
def get_eligibility():
    """
    Given email and feature name, this function checks whether the given email is eligible to carry out that particular function
    """
    try:

        # unpack the arguments to feature and email
        data = request.values
        email = data.get("email")
        featureName = data.get("featureName")

        # search in mongodb the corresponding email and feature name
        data = featureAccessCollection.find({"email":email, "featureName":featureName})[0]

        # if the current email has access to the feature we return the json response, else return otherwise
        if data["enable"]:
            return {"canAccess":True}, 200
        else:
            return {"canAccess":False}, 200

    except IndexError:
        return "Email or Feature Name is invalid"
    

if __name__ == "__main__":
    app.run(debug=True)