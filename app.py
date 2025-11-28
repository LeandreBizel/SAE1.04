from flask import Flask, render_template, request, redirect, flash
from datetime import date
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
    sql=''' SELECT id_achat, client_id, CLIENT.nom, CLIENT.prenom, montant_total, poids_total, date_achat 
    FROM ACHAT
    JOIN CLIENT ON ACHAT.client_id = CLIENT.id_client
    GROUP BY id_achat, client_id
    ORDER BY client_id ASC
     '''
    mycursor.execute(sql)
    achats = mycursor.fetchall()
    sql = '''
        SELECT client_id, SUM(montant_total) AS total_depense, CLIENT.nom, CLIENT.prenom
        FROM ACHAT
        JOIN CLIENT ON ACHAT.client_id = CLIENT.id_client
        GROUP BY client_id
        ORDER BY total_depense DESC
        LIMIT 1;
    '''
    mycursor.execute(sql)
    client = mycursor.fetchone()
    return render_template('Tables/Achats.html', achats=achats, client=client)

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
    client_id = request.form.get('client_id')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    if not date_achat:
        date_achat = date.today().strftime("%Y-%m-%d")
    message = 'id du client :' + client_id + ' - montant total :' + montant_total + ' - poids total :' + poids_total + "- date d'achat :" + date_achat
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(client_id, montant_total, poids_total, date_achat)
    sql="INSERT INTO ACHAT(client_id, montant_total, poids_total, date_achat ) VALUES (%s, %s, %s, %s);"
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
    sql=''' SELECT id_achat , client_id,  montant_total , poids_total ,date_achat 
    FROM ACHAT
    WHERE id_achat=%s;'''
    tuple_param=(id_achat,)
    mycursor.execute(sql,tuple_param)
    achat = mycursor.fetchone()
    sql=''' SELECT client_id, nom, prenom
    FROM CLIENT;'''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('Tables/Achat_edit.html', achat=achat, clients=clients)

@app.route('/Achat/edit', methods=["POST"])
def valid_edit_achat():
    print('''modification de l'achat dans le tableau''')
    id_achat=request.form.get('id_achat')
    client_id = request.form.get('client_id')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    message = 'id de l\'achat:' + id_achat + 'id du client :' + client_id + ' - montant total :' + montant_total + ' - poids total :' + poids_total + "- date d'achat :" + date_achat
    print(message)
    mycursor = get_db().cursor()
    tuple_param=(client_id, montant_total, poids_total, date_achat, id_achat)
    sql="UPDATE ACHAT SET client_id = %s, montant_total = %s, poids_total = %s, date_achat = %s WHERE id_achat=%s;"
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

@app.route('/Collecte-vetements/delete', methods = ['GET'])
def delete_collecte_vetements():
    mycursor = get_db().cursor()
    id_collecte_vetement = request.args.get('id_collecte_vetement')
    tuple_delete = (id_collecte_vetement,)
    sql ="DELETE FROM COLLECTE_VETEMENT WHERE id_collecte_vetement = %s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    flash('une collecte à été supprimé :' + id_collecte_vetement)
    return redirect('/Collecte-vetements/show')

@app.route('/Collecte-vetements/add', methods=['GET'])
def add_collecte_vetements():
    return render_template('Tables/Collecte-vetements_add.html')


@app.route('/Collecte-vetements/add', methods=['POST'])
def valid_add_collecte_vetements():
    print("Ajout d'une nouvelle collecte...")
    quantite_vetement = request.form.get('quantite_vetement')
    date_collecte = request.form.get('date_collecte')
    id_collecte = request.form.get('id_collecte')
    id_categorie_vetement = request.form.get('id_categorie_vetement')
    print(f"quantité = {quantite_vetement}, date = {date_collecte}")
    mycursor = get_db().cursor()
    sql = """ INSERT INTO COLLECTE_VETEMENT (id_collecte,quantite_vetement, date_collecte,id_categorie_vetement) VALUES (%s, %s,%s,%s)"""
    tuple_insert = (id_collecte, quantite_vetement, date_collecte,id_categorie_vetement)
    mycursor.execute(sql, tuple_insert)
    get_db().commit()
    flash("Nouvelle collecte ajoutée avec succès !")
    return redirect('/Collecte-vetements/show')

@app.route('/Collecte-vetements/edit', methods=['GET'])
def edit_collecte_vetements():
    mycursor = get_db().cursor()
    id_collecte_vetement = request.args.get('id_collecte_vetement')
    sql = """SELECT * FROM COLLECTE_VETEMENT WHERE id_collecte_vetement = %s"""
    mycursor.execute(sql, (id_collecte_vetement,))
    Collecte = mycursor.fetchone()
    return render_template('Tables/Collecte-vetements_edit.html', Collecte=Collecte)

@app.route('/Collecte-vetements/edit', methods=['POST'])
def valid_edit_collecte_vetements():
    print("Modification d'une collecte...")
    id_collecte_vetement = request.form.get('id_collecte_vetement')
    quantite_vetement = request.form.get('quantite_vetement')
    date_collecte = request.form.get('date_collecte')
    print(f"id: {id_collecte_vetement}, quantité: {quantite_vetement}, date: {date_collecte}")
    mycursor = get_db().cursor()
    sql = """ UPDATE COLLECTE_VETEMENT SET quantite_vetement = %s, date_collecte = %s WHERE id_collecte_vetement = %s """
    tuple_update = (quantite_vetement, date_collecte, id_collecte_vetement)
    mycursor.execute(sql, tuple_update)
    get_db().commit()
    flash(f"Collecte {id_collecte_vetement} modifiée avec succès !")
    return redirect('/Collecte-vetements/show')

if __name__ == '__main__':
    app.run(debug=True)





