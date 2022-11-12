from flask import Flask, request, render_template
import joblib
import pandas as pd

def df_builder(dictionary):
    
    feature_list = ["sex", "pclass", "fare", "age"]
    target_feature = "survived"
    feature_to_drop = ['name', 'sibsp', 'parch', 'ticket', 'cabin', 'embarked']
    
    columns = []
    values = []
    
    for key in feature_list:
        columns.append(key)
        values.append(dictionary[key] if key in dictionary else None)

    for key in feature_to_drop:
        columns.append(key)
        values.append(None)
    
    columns.append(target_feature)
    values.append("unknown")

    return pd.DataFrame([values], columns=columns)

def build_data_from_source(source):
    data =  {}
    for param in ["pclass" , "fare", "age", "sex"]:
        value = source.get(param)
        if value is None:
            return None
        else:
            data[param]=value
    return data

def build_data_from_request(request):
    if request.method == 'POST':
        return build_data_from_source(request.form)
    if request.method == 'GET':
        return build_data_from_source(request.args)
    return None


app = Flask(__name__, template_folder="template")
@app.route("/" , methods = ["GET", "POST"])
def home():
    data = build_data_from_request(request)
    df = None if data is None else df_builder(data)

    if df is None:
        return render_template("index.html", output="", data=data)
    else:
        pipeline = joblib.load("pipeline.pkl")
        model = joblib.load("model.pkl")
        df = pipeline.transform(df).drop("survived", axis=1)
        prediction = "Superviviente" if model.predict(df)[0] else "No Superviviente"
        return render_template("index.html", output=prediction, data=data)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8181)


