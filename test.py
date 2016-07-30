# import web
# from web import form

# render = web.template.render('templates') # your templates

# vpass = form.regexp(r".{3,20}$", 'must be between 3 and 20 characters')
# vemail = form.regexp(r".*@.*", "must be a valid email address")

# register_form = form.Form(
#     form.Textbox("username", description="Username"),
#     form.Textbox("email", vemail, description="E-Mail"),
#     form.Password("password", vpass, description="Password"),
#     form.Password("password2", description="Repeat password"),
#     form.Button("submit", type="submit", description="Register"),
#     validators = [
#         form.Validator("Passwords did't match", lambda i: i.password == i.password2)]

# )

# class register:
#     def GET(self):
#         # do $:f.render() in the template
#         f = register_form()
#         return render.register(f)

#     def POST(self):
#         f = register_form()
#         if not f.validates():
#             return render.register(f)
#         else:
#             f = register_form()
#             if not f.validates():
#                 return render.register(f)

from flask import (Flask, render_template, redirect,
                   url_for, request, make_response)

from tinydb.operations import delete

from tinydb import TinyDB, where

db = TinyDB('name_email.json')
datab = TinyDB('flight_details.json')
dbase = TinyDB('dbase.json')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/show', methods=['POST'])
def save():
    name=request.form['yourname']
    email=request.form['youremail']
    db.insert({name: email})
    return render_template('form_submit.html')



@app.route('/checked_status', methods=['POST'])
def fs():
    airname=request.form['airname']
    
    flight = datab.search(where('airname') == airname)
    
    for items in flight:
        status = items.get('status')
        deploc = items.get('deploc')
        arrloc = items.get('arrloc')
        flightname = items.get('airname')
    return render_template('checked_status.html', airname=flightname, status=status, deploc=deploc, arrloc=arrloc )



@app.route('/cancelled_msg', methods=['POST'])
def cs():
    flightname=request.form['flightname']
    dbase.update(delete(where('flightname') == flightname))
    return render_template('cancelled_msg.html') 

@app.route('/cancel_flight', methods=['POST'])
def gf():
    flightname=request.form['flightname']
    
    event = dbase.search(where('flightname') == flightname)
    
    for items in event:
        flightdate = items.get('flightdate')
        fromloc = items.get('fromloc')
        toloc = items.get('toloc')
        flightname =  items.get('flightname')
    return render_template('cancel_flight.html', flightname=flightname, flightdate=flightdate, fromloc=fromloc, toloc=toloc )


@app.route('/booked', methods=['POST'])
def move():
    name=request.form['yourname']
    age=request.form['age']
    gender=request.form['gender']
    flightname=request.form['flightname']
    flightdate=request.form['flightdate']
    fromloc=request.form['fromloc']
    toloc=request.form['toloc']
    
    dbase.insert({'name': name, 'flightname': flightname, 'age':age, 'gender':gender, 'flightdate': flightdate, 'fromloc': fromloc, 'toloc': toloc})
    
    return render_template('booked.html', name=name, age=age, gender=gender, flightname=flightname, flightdate=flightdate, fromloc=fromloc, toloc=toloc)

@app.route('/flight_status')
def flight_status():
    return render_template('flight_status.html')

@app.route('/get_flight')
def get_flight():
    return render_template('get_flight.html')
    
@app.route('/db')
def show_db():
    dbout = db.all()
    item1 = (dbout[0])
    # itemkey = item1.values()
    # return str(itemkey)
    return str(dbout)
    
@app.route('/booking')
def booking():
    return render_template('booking.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
