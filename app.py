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


@app.route('/Achat/show')
def show_achat():
    mycursor = get_db().cursor()
    sql=''' SELECT * FROM ACHAT '''
    mycursor.execute(sql)
    achats = mycursor.fetchall()
    return render_template('Tables/Achats.html', achats=achats)

@app.route('/Achat/add', methods=["GET"])
def add_achat():
    print('''affichage du formulaire pour enregistrer un Achat''')
    mycursor = get_db().cursor()
    sql=''' SELECT id_client, nom, prenom
    FROM CLIENT;'''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('Tables/Achat_add.html',clients=clients)



@app.route('/Achat/add', methods=['POST'])
def valid_add_achat():
    print('''ajout de L'achat dans le tableau''')
    id_client = request.form.get('id_client')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    message = 'id du client :' + id_client + ' - montant total :' + montant_total + ' - poids total :' + poids_total + "- date d'achat :" + date_achat
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(id_client, montant_total, poids_total, date_achat)
    sql="INSERT INTO ACHAT(id_client, montant_total, poids_total, date_achat ) VALUES (%s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/Achat/show')



@app.route('/Achat/edit', methods=["GET"])
def edit_achat():
    print('''affichage du formulaire pour modifier un achat''')
    print(request.args)
    print(request.args.get('id_achat'))
    id_achat=request.args.get('id_achat')
    mycursor = get_db().cursor()
    sql=''' SELECT id_achat , id_client,  montant_total , poids_total ,date_achat 
    FROM ACHAT
    WHERE id_achat=%s;'''
    tuple_param=(id_achat,)
    mycursor.execute(sql,tuple_param)
    achat = mycursor.fetchone()
    sql=''' SELECT id_client, nom, prenom
    FROM CLIENT;'''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('Tables/Achat_edit.html', achat=achat, clients=clients)

@app.route('/Achat/edit', methods=["POST"])
def valid_edit_achat():
    print('''modification de l'achat dans le tableau''')
    id_achat=request.form.get('id_achat')
    id_client = request.form.get('id_client')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    message = 'id de l\'achat:' + id_achat + 'id du client :' + id_client + ' - montant total :' + montant_total + ' - poids total :' + poids_total + "- date d'achat :" + date_achat
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(id_client, montant_total, poids_total, date_achat, id_achat)
    sql="UPDATE ACHAT SET id_client = %s, montant_total = %s, poids_total = %s, date_achat = %s WHERE id_achat=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/Achat/show')


@app.route('/Achat/delete')
def delete_achat():
    print('''suppression d'un achat''')
    id_achat=request.args.get('id_achat',0)
    print(id_achat)
    mycursor = get_db().cursor()
    tuple_param=(id_achat,)
    sql="DELETE FROM ACHAT WHERE id_achat=%s;"
    mycursor.execute(sql,tuple_param)

    get_db().commit()
    print(request.args)
    print(request.args.get('id_achat'))
    return redirect('/Achat/show')

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



