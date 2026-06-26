from flask import Flask ,render_template,redirect,session,url_for,request
import joblib
from sklearn.preprocessing import StandardScaler
from datetime import timedelta

app=Flask(__name__)
model=joblib.load("housepricepredictmodel.pkl")
scaler=joblib.load("scaler.pkl")
app.secret_key='vivekkali'
app.permanent_session_lifetime=timedelta(minutes=60)


@app.route('/',methods=['GET','POST'])
def home():
    if request.method=='POST':
        area_sqft=int(request.form.get("area_sqft"))
        bathrooms=int(request.form.get("bathrooms"))  # isdigit is only aplicable for strings

        if area_sqft==0 or area_sqft is None:
            return 'enter a valid area of home '
        
        if bathrooms==0 or bathrooms is None:
            return 'enter a number of bathrooms in home '

        obs=scaler.transform([[area_sqft,bathrooms]])
        price=model.predict(obs)

        session['price'] = float(price[0])

        print("processing !!!!!!!")
        
        return redirect(url_for('result'))
    else:
        return render_template('index.html')   # focus vivek you are the best , you can do it alone


@app.route('/result',methods=['GET','POST'])
def result():
    price=session['price']
    return render_template("result.html",price=price)
        
if __name__=='__main__':
    app.run(debug=True)
