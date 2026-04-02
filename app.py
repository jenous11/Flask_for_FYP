## url routing

from flask import Flask,render_template,request,redirect,url_for,jsonify
import joblib ## import necessary modules from flask
 #loading the model
loaded_svm=joblib.load('clf_svm.joblib') ## load the pre-trained SVM model from the file
# loaded_svm=joblib.load('clf_log.joblib') ## load the pre-trained SVM model from the file

loaded_vectorizer=joblib.load('vectorizer.joblib') ## load the pre-trained vectorizer from the file

#create a simple flask applicatino
app=Flask(__name__) ## program entry point

# @app.route('/',methods=["GET"]) # decorator to define the route for the home page
# def home():
#     return '<h1>Welcome to the home page!</h1>' ## return a simple message when the home page is accessed

# @app.route('/index',methods=["GET"]) # decorator to define the route for the index page
# def index():
#     return '<h1>Welcome to the index page!</h1>' ## return a simple message when the index page is accessed

# ##variable rule
# ##int: accepts integers
# @app.route('/success/<int:score>') # decorator to define the route for the success page with a variable score
# def success(score):
#     return "Test passed with score: " + str(score) ## return a message with the score when the success page is accessed

# @app.route('/fail/<int:score>') # decorator to define the route for the failure page with a variable score
# def failure(score):
#     return "Test failed with score: " + str(score) ## return a message with the score when the failure page is accessed

# @app.route('/form',methods=["GET","POST"]) # decorator to define the route for the form page with GET and POST methods
# def form():
#     if request.method == "GET":
#      return render_template('form.html') ## render the form template when the form page is accessed with GET method
#     else:
#         maths=float(request.form['maths'])
#         science=float(request.form['science'])
#         history=float(request.form['history'])
#         # return render_template('form.html',score=average)
#         average=(maths+science+history)/3 ## calculate the average score from the form data
#         res=""
#         if average>=50:
#             res="success"  ## create the success URL with the average score
#         else:
#             res="failure"  ## create the failure URL with the average score
#         return redirect(url_for(res,score=int(average))) ## render the form template with the average score and result URL

# @app.route('/api', methods=['POST']) # decorator to define the route for the API endpoint with GET method
# def calculate_sum():
#   data=request.get_json() ## get the JSON data from the request

#   a_val=float(data['a'])
#   b_val=float(data['b'])

#   return jsonify(a_val+b_val) ## return the sum of a and b as a string
@app.route('/', methods=['GET'])
def home():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
  text=[]
  text=request.form["text"]
  text=loaded_vectorizer.transform([text])
  predict=loaded_svm.predict(text)
  if(predict[0]==0):
    predict="Not Cyberbullying"
  else:
    predict="Cyberbullying"
  # return render_template('predict.html', prediction=predict) ## render the predict template with the prediction result

  # return render_template('predict.html', prediction=predict) ## render the predict template with the prediction result
  #this works
  return jsonify(predict) ## return the prediction as a string




if __name__ == '__main__':
    app.run(debug=True) ## run the application in debug mode
