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
            database="BDD_nlahurte_sae",        # à modifier
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
    sql=''' SELECT * FROM ACHAT '''
    mycursor.execute(sql)
    Achats = mycursor.fetchall()
    return render_template('Tables/Achats.html', Achats=Achats)

app.route('/Achats-vetements/show')
def show_achats_vetements():
    sql = ''' SELECT * FROM ACHATS_VETEMENTS '''
    return render_template('Tables/Achats-vetements.html')

@app.route('/Achats-vetements/edit')
def edit_achats_vetements():
    return render_template('Tables/Achats-vetements.html')

@app.route('/Achats-vetements/delete')
def delete_achats_vetements():
    return render_template('Tables/Achats-vetements.html')

@app.route('/Achats-vetements/add')
def add_achats_vetements():
    return render_template('Tables/Achats-vetements.html')

@app.route('/Depose/show')
def show_depose():
    return render_template('Tables/Depose.html')
    
@app.route('/Collecte-vetements/show')
def show_collecte_vetements():
    mycursor = get_db().cursor()
    sql = ''' SELECT * FROM COLLECTE_VETEMENT '''
    mycursor.execute(sql)
    Collecte = mycursor.fetchall()
    return render_template('Tables/Collecte-vetements.html', Collecte = Collecte)

@app.route('/Collecte-vetements/delete')
def delete_collecte_vetements():
    return render_template('Tables/Collecte-vetements.html')

@app.route('/Collecte-vetements/add_collecte-vetements')
def add_collecte_vetements():
    return render_template('Tables/Collecte-vetements.html')

@app.route('/Collecte-vetements/edit-collecte-vetements')
def edit():
    return render_template('Tables/Collecte-vetements.html')

if __name__ == '__main__':
    app.run(debug=True)

