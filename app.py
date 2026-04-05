## url routing

from flask import Flask,render_template,request,redirect,url_for,jsonify
import joblib ## import necessary modules from flask
 #loading the model
loaded_svm=joblib.load('clf_svm.joblib') ## load the pre-trained SVM model from the file
# loaded_svm=joblib.load('clf_log.joblib') ## load the pre-trained SVM model from the file
loaded_vectorizer=joblib.load('vectorizer.joblib') ## load the pre-trained vectorizer from the file
#create a simple flask applicatino
app=Flask(__name__) ## program entry point


@app.route('/', methods=['GET'])
def home():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
  data=request.get_json() ## get the JSON data from the request
  text=data['prediction']
  text=loaded_vectorizer.transform([text])
  predict=loaded_svm.predict(text)
  if(predict[0]==0):
    predict="Not Cyberbullying"
  else:
    predict="Cyberbullying"

  # return jsonify(predict) ## return the prediction as a string
  return jsonify({'result':predict})



if __name__ == '__main__':
    app.run(debug=True) ## run the application in debug mode
