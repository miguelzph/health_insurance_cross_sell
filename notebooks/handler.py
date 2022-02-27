from flask import Flask, request,Response
from insurance.InsuranceCrossSell import InsuranceCrossSell
import pickle
import pandas as pd

# loading model
model = pickle.load(open('../models/xgb_model.pkl', 'rb'))

# api
app = Flask(__name__)

@app.route('/')
def test_status():
    return {'status': 'ok'}

@app.route('/insurance/clients/rank', methods=['POST'])
def insurance_rank():
    test_json = request.get_json()
    
    if test_json:
        if isinstance(test_json, dict): # unique line
            test_raw = pd.DataFrame(test_json, index=[0])
        else: # multiple lines
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())
            
        # Instantiate Rossmanclass
        pipeline = InsuranceCrossSell()
        print(test_raw.head())
        # data cleaning
        #df_1 = pipeline.data_cleaning(test_raw)
        
        # feature engineering
        df_2 = pipeline.feature_engineering(test_raw)
        # data prepatarion
        df_3 = pipeline.data_preparation(df_2)
        # predicition
        df_response = pipeline.get_prediction(model, df_3, test_raw)
        
        return df_response
        
    else:
        return Response('{No Data}', status=200, mimetype='application/json')
    
if __name__=='__main__':
    app.run('0.0.0.0')