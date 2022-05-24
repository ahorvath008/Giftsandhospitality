from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_mail import Message


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///trainline_gandh.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] =  465
app.config['MAIL_USERNAME'] = 'ahorvath008@gmail.com'
app.config['MAIL_PASSWORD'] =  'zerindvezerutca4'
app.config['MAIL_USE_TLS'] =  False
app.config['MAIL_USE_SSL'] = True


mail = Mail(app)


db = SQLAlchemy(app)
#migrate = Migrate(app, db)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    office = db.Column(db.String(100))
    gift_received_from = db.Column(db.String(100), nullable=False)
    date_gift_received = db.Column(db.String(100),nullable=False)
    gift_description = db.Column(db.String(100),nullable=False)
    action_taken = db.Column(db.String(100),nullable=False)
    date_event = db.Column(db.String(100))
    amount_raised = db.Column(db.Integer)

db.create_all()

# Setting up the routes
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['GET','POST'])
def submit():
    if request.method == 'POST':
        office = request.form['office']
        gift_received_from =  request.form['gift_received_from']
        date_gift_received =  request.form['date_gift_received']
        gift_description =  request.form['gift_description']
        action_taken = request.form['action_taken']
        date_event = request.form['date_event']
        amount_raised = request.form['amount_raised']
        mydata = Data(office=office, gift_received_from=gift_received_from,date_gift_received=date_gift_received,gift_description=gift_description,action_taken=action_taken, date_event=date_event, amount_raised=amount_raised)
        db.session.add(mydata)
        db.session.commit()
        return redirect('/submit')
    else:
        subject = "A new entry has been made in the gift register"
        msg = Message("A new entry has been added to the Gift Register",
                      sender="ahorvath00@gmail.com",
                      recipients=["ahorvath008@gmail.com"])

        msg.html = "table.html"
        mail.send(msg)
        return render_template('thanks.html')

@app.route('/table', methods=['GET', 'POST'])
def table():
    gifts = Data.query.all()
    return render_template('/table.html', gifts=gifts)

@app.route('/forms', methods=['GET', 'POST'])
def forms():

    return render_template('/forms.html')
if __name__ == "__main__":
    #init_db()
    app.run(debug=True)