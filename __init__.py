import os
from flask import (
  Flask, redirect, render_template, url_for, abort,
  jsonify, request, flash
)



messages = []

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET KEY', default=os.urandom(24).hex())   
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(
            test_config
        )
    

    from .models import db, Ticket
    from sqlalchemy.orm.exc import NoResultFound
    
    db.init_app(app)

    # create tables
    with app.app_context():
        db.create_all()


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.route('/')
    def index():
        return redirect(url_for('tickets'))
    

    @app.route('/tickets')
    def tickets():
        tickets = Ticket.query.all()
        return render_template('tickets_index.html', tickets=tickets)
    
    @app.route('/tickets/<int:ticket_id>')
    def tickets_show(ticket_id):
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).one()
            return render_template('tickets_show.html', ticket=ticket)
        except NoResultFound:
            print(ticket = Ticket.query.filter_by(id=ticket_id).one())  
            abort(404)

    @app.route('/api/tickets')  
    def api_tickets():
        tickets = Ticket.query.all()
        return jsonify([ticket.to_json() for ticket in tickets])

    @app.route('/api/tickets/<int:ticket_id>')
    def api_tickets_show(ticket_id):
        try:
            ticket = Ticket.query.filter_by(id=ticket_id).one()
            return jsonify(ticket.to_json)
        except NoResultFound:
            return jsonify({'error': 'ticket not found' }, 404)

    @app.route('/about')
    def about():
        return render_template('about.html')
    
    # html forms using bootstrap templates
    @app.route('/register', methods=('GET', 'POST'))
    def register():
        if request.method == 'POST':
            print(request.form)

            t = Ticket(
                id=request.form['ticket_id'],
                name=request.form['ticket_name'],
                status=request.form['ticket_status'], 
                url=request.form['ticket_url']
            )

            db.session.add(t)
            db.session.commit()

            return render_template('register.html')
        
        if request.method == 'GET':
            return render_template('register.html')
    
    return app