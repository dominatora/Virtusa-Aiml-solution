from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np
import pandas as pd
from pycaret.clustering import *
app = Flask(__name__, static_folder='static', static_url_path='/home/static')

model = load_model('Final Kmeans Model')
unseen_predictions = pd.read_csv('unseenPredictions.csv')

@app.route('/home/static/<path:path>')
def send_js(path):
    return send_from_directory('js', path)
        
@app.route('/home/')
def home():
    return render_template('index.html')

@app.route('/home/predict',methods=['POST'])

def predict():
    '''
    For rendering results on HTML GUI
    '''
    list1 = request.form.to_dict()
    pname = list1['pname']
    del list1['pname'] 
    list1 = list(list1.values()) 
    list1 = list(map(int, list1))
    #int_features = [int(x) for x in request.form.values()]
    #final_features = [np.array(int_features)]
    #prediction = model.predict(unseen_predictions.head(1))


    list2 = list1
    #For Provider Type
    if list2[1] == 0:
        list1[1] = "Medicare"
    elif list2[1] == 1:
        list1[1] = "Medicaid"
    else:
        list2[1] = "Medicare and Medicaid"
    #For PCP
    if list2[2] == 0:
        list1[2] = "FP"
    elif list2[2] == 1:
        list1[2] = "GP"
    elif list2[2] == 2:
        list1[2] = "PD"
    elif list2[2] == 3:
        list1[2] = "GER"
    elif list2[2] == 4:
        list1[2] = "GIM"
    else:
        list1[2] = "No"

    
        
    list_atoformat = [100 , 1 , "Name" , "Adress" , "City" , "State" , list1[0] , 9999 , "county" , list1[9] , list1[10] , list1[1] , list1[3] , list1[4] , list1[5] , list1[6] , (list1[11]/100) , (list1[12]/100) , list1[8] , 2,2,2,2,list1[13],list1[14],list1[15],50,list1[16],list1[18],list1[2],"Cluster 3"  ]
    final_features = pd.DataFrame(data = [np.array(list_atoformat)], columns = unseen_predictions.columns)
    prediction = model.predict(final_features) 

    
    output = round(prediction[0], 2)
    #output = 2
    # OUTPUT
    if output == 0:
        cname = "Not Eligible"
    elif output == 1:
        cname = "Low End"
        if list1[2] == "No":
            contract = "Cluster_1_Low_end_provider_Specialty.docx"
        else:
            contract = "Cluster_1_Low_end_provider_PCP.docx" 
    elif output == 2:
        cname = "Mid Level"
        if list1[2] == "No":
            contract = "Cluster_2_Mid_level_provider_Specialty.docx"
        else:
            contract = "Cluster_2_Mid_level_Provider_PCP.docx"
    elif output == 3:
        cname = "High End"
        if list1[2] == "No":
            contract = "Cluster_3_ High_end_provider_Specialty.docx"
        else:
            contract = "Cluster_3_High_end_provider_PCP_Agreement.docx"

    #contract

#     if list1[2] == "No":
#         contract = "Cluster_1_Low_end_provider_Specialty.docx"
#     else:
#         contract = "Cluster_1_Low_end_provider_PCP.docx"    


    #Avg Hospital Stay
    avgHS = list1[13]
    #Reimbursement
    TC = list1[14]
    #Patient Satisfaction rate:
    PSR = list1[16]
    #Hospital readmission rate:
    HRS = list1[15]
    if output == 0:
        return render_template('/dashboard/index_0.html',pname = '{}'.format(pname) ,prediction_text='{}'.format(output) ,cname = '{}'.format(cname) ,avghs = '{}'.format(avgHS) , TC = '{}'.format(TC) , PSR = '{}'.format(PSR) , HRS = '{}'.format(HRS))
    elif output == 1:
        return render_template('/dashboard/index.html',pname = '{}'.format(pname) ,prediction_text='{}'.format(output) ,cname = '{}'.format(cname) ,avghs = '{}'.format(avgHS) , TC = '{}'.format(TC) , PSR = '{}'.format(PSR) , HRS = '{}'.format(HRS),contract = '{}'.format(contract))
    elif output == 2:
        return render_template('dashboard/index_2.html',pname = '{}'.format(pname) ,prediction_text='{}'.format(output) ,cname = '{}'.format(cname) ,avghs = '{}'.format(avgHS) , TC = '{}'.format(TC) , PSR = '{}'.format(PSR) , HRS = '{}'.format(HRS),contract = '{}'.format(contract))
    else :    
        return render_template('dashboard/index_3.html',pname = '{}'.format(pname) ,prediction_text='{}'.format(output) ,cname = '{}'.format(cname) ,avghs = '{}'.format(avgHS) , TC = '{}'.format(TC) , PSR = '{}'.format(PSR) , HRS = '{}'.format(HRS),contract = '{}'.format(contract))


      
        
@app.route('/home/cluster_analysis')
def cluster_analysis():
    return render_template('dashboard/ca.html')
    
@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)

if __name__ == "__main__":
      app.run(port=12323, debug=True)