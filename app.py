import sys
from flask import Flask, render_template, request,redirect,flash, session
from surveys import satisfaction_survey
app = Flask('__name__')
app.config["SECRET_KEY"]= "secret-key"


@app.route('/')
def home():
    if not session.get('responses'):
        return render_template('base.html',survey = satisfaction_survey)
    if len(satisfaction_survey.questions)==len(session['responses']):
        return redirect('/thank_you')
    

@app.route('/start-session',methods=['POST'])
def start_session():
        session["responses"]=[]
        return redirect('/questions/0')

@app.route('/questions/<int:current_question>')
def show_question(current_question):
    if current_question!=len(session["responses"]):
        flash("almost went to the wrong place")
        return redirect(f'/questions/{len(session["responses"])}')
    elif len(session)==len(satisfaction_survey.questions):
        redirect('/thank_you')
    question = satisfaction_survey.questions[current_question]
    return render_template('questions.html',question=question,survey =satisfaction_survey,q_id=current_question)

@app.route('/answer',methods=['POST','GET'])
def answer_view():
    answer = request.form['answer']
    responses = session["responses"]
    responses.append(answer)
    session['responses']=responses
    if len(session['responses'])>=len(satisfaction_survey.questions):
        return redirect('/thank_you')
    return redirect(f'/questions/{len(session["responses"])}')

@app.route('/thank_you')
def thank_you_view():
    if len(session["responses"])!=len(satisfaction_survey.questions):
        redirect('/')
    return render_template('thank-you.html',survey=satisfaction_survey)