from flask import Flask, Response, request, render_template, session, g
from flask_cors import CORS
from math import radians, cos, sin, asin, sqrt, isnan
import pandas as pd
import numpy as np
import pgeocode
import pickle
import json

HOST = "0.0.0.0"
PORT = 9001
app = Flask(__name__,
        static_url_path='/',
        static_folder='static/class-ui/',
        template_folder='web/templates')
CORS(app)
model_file = 'rf_model.pkl'

# Helper function that calculates Haversine distance
def haversine_distance(lat1, lon1, lat2, lon2):
  R = 6371  # radius of Earth in kilometers
  phi1 = np.radians(lat1)
  phi2 = np.radians(lat2)
  delta_phi = np.radians(lat2 - lat1)
  delta_lambda = np.radians(lon2 - lon1)
  
  a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2)**2
  c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
  
  return R * c

# Helper function that calculates the closest point between input point and points in dataset
def find_closest(dataset, lat, long):
    distances = dataset.apply(
        lambda row: haversine_distance(lat, long, row['latitude'], row['longitude']), axis=1)
    return dataset.loc[distances.idxmin(), ]

# Helper function that calculates the longtitude and latitude of a particular zipcode
def find_zip_info(zip):
    usnomi = pgeocode.Nominatim('US')
    result = usnomi.query_postal_code(zip)
    return result

# Helper function to pad zeros in front of zip code for calculation
def pad_zeros(num):
    num_len = len(num)
    for i in range(5-num_len):
        num = '0' + num
    return num

@app.route("/predict", methods=["post"])
def predict():
    content_type = request.headers.get('Content-Type')
    if (content_type != 'application/json'):
        return Response('Content-Type Not Supported', status=400, content_type="text/plain")

    # Retrieve data from request
    body = request.json
    print(body)
    bed = body['bed']
    bath = body['bath']
    house_size = body['house_size']
    zipcode = body['zip_code']

    # get zip code info
    if (type(zipcode) != str):
        zipcode = str(zipcode)
    zipcode = pad_zeros(zipcode)
    info = find_zip_info(zipcode)
    state = info.state_code
    city = info.place_name
    lon = info.longitude
    lat = info.latitude

    # Check zip code valid
    if (isnan(lon) or isnan(lat)):
        return Response('Invalid Zip Code', status=400, content_type="text/plain")

    # Check state
    if (state != 'NY' and state != 'NJ'):
        return Response('State Not Supported', status=400, content_type="text/plain")

    # Check W.R.T. dataset
    nynj_df = pd.read_csv("datasets/nynj_data.csv")
    
    # Here we manually removed some zipcode and assign to others just to test not existed zip codes
    # nynj_df.loc[nynj_df['zip_code'] == 7057, 'zip_code'] = 7051

    # Check city
    if (nynj_df[nynj_df['city']==city].shape[0] == 0):
        return Response('City Not Supported', status=400, content_type="text/plain")

    # Check zipcode
    city_enc = None
    zip_enc = None
    if (nynj_df[nynj_df['zip_code']==int(zipcode)].shape[0] == 0):
        # Not existed, find closest point in existed dataset
        print("not exist")
        closest_data = find_closest(nynj_df, lon, lat)
        city_enc = closest_data.city_enc
        zip_enc = closest_data.zip_enc
    else:
        # Existed in dataset
        print("exist")
        index = nynj_df[nynj_df['zip_code']==int(zipcode)].index.values[0]
        template_data = nynj_df.iloc[index,]
        city_enc = template_data.city_enc
        zip_enc = template_data.zip_enc

    # Can Predict! Load model
    loaded_model = pickle.load(open(model_file, 'rb'))
    X_pred_list = [bed, bath, house_size, city_enc, zip_enc, 1 if state == 'NY' else 0, 1 if state == 'NJ' else 0]
    X_pred = np.array(X_pred_list).reshape(1, -1)
    y_pred = loaded_model.predict(X_pred)
    result = {
        'result': "success",
        'price_predicted' : y_pred[0]
    }
    return Response(json.dumps(result), status=200, content_type="application.json")
        

if __name__ == "__main__":
    app.run(HOST, PORT)
