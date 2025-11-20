from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="serveurmysql",                 # à modifier
            user="nlahurte",                     # à modifier
            password="secret",                # à modifier
            database="BDD_nlahurte",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db


@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()
@app.route('/')
def show_layout():

    return render_template('layout.html')


@app.route('/Achats/show')
def show_achat():
    mycursor = get_db().cursor()
    sql = ''' SELECT id_achat, montant_total, date_achat, poid_total, client_id FROM ACHAT '''
    mycursor.execute(sql)

    achats = mycursor.fetchall()
    return render_template('Tables/Achats.html', achats=achats)

@app.route('/Achats-vetements/show')
def show_achats_vetements():
    return render_template('Tables/Achats-vetements.html')

@app.route('/Depose/show')
def show_depose():
    return render_template('Tables/Depose.html')
@app.route('/Categories-vetements/show')
def show_categories_vetements():
    return render_template('Tables/Categories-vetements.html')

if __name__ == '__main__':
    app.run(debug=True)
