from flask import Flask, render_template, request,redirect,flash
from surveys import satisfaction_survey
app = Flask('__name__')
app.config["SECRET_KEY"]= "secret-key"
responses = []

@app.route('/')
def home():
    return render_template('base.html',survey = satisfaction_survey)

@app.route('/questions/<int:current_question>')
def show_question(current_question):
    if current_question!=len(responses):
        flash("almost went to the wrong place")
        return redirect(f'/questions/{len(responses)}')
    elif len(responses)==len(satisfaction_survey.questions):
        redirect('/thank_you')
    question = satisfaction_survey.questions[current_question]
    return render_template('questions.html',question=question,survey =satisfaction_survey,q_id=current_question)

@app.route('/answer')
def answer_view():
    answer = request.args["answer"]
    responses.append(answer)
    if len(responses)>=len(satisfaction_survey.questions):
        return redirect('/thank_you')
    return redirect(f'/questions/{len(responses)}')

@app.route('/thank_you')
def thank_you_view():
    if len(responses)!=len(satisfaction_survey):
        redirect('/')
    return render_template('thank-you.html',survey=satisfaction_survey,responses=responses)