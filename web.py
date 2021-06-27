from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField, SelectField
import predictions

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

class SymptomForm(FlaskForm):
    symptom1 = SelectField('Symptom1', choices=[(x,x) for x in predictions.l1])
    symptom2 = SelectField('Symptom2', choices=[(x,x) for x in predictions.l1])
    symptom3 = SelectField('Symptom3', choices=[(x,x) for x in predictions.l1])
    submit = SubmitField('Submit')

symptoms = []
@app.route("/", methods=['GET', 'POST'])
def main():
    form = SymptomForm()
    if form.validate_on_submit():
        flash('Symptoms submitted', 'success')
        value1 = dict(form.symptom1.choices).get(form.symptom1.data)
        value2 = dict(form.symptom2.choices).get(form.symptom2.data)
        value3 = dict(form.symptom3.choices).get(form.symptom3.data)
        symptoms.append(value1)
        symptoms.append(value2)
        symptoms.append(value3)
        disease = predictions.NaiveBayes(symptoms)
        return redirect(url_for('result', name =disease))
    return render_template('main.html', form=form)

@app.route("/result")
def result():
    disease = predictions.NaiveBayes(symptoms)
    return render_template("results.html", name =disease)

if __name__ == "__main__":
    app.run(debug=True)
