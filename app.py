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

@app.route('/Achat/etat')
def show_etat():
    mycursor = get_db().cursor()
    sql = '''
        SELECT client_id, SUM(montant_total) AS total_depense,COUNT(id_achat) AS nb_achat, CLIENT.nom, CLIENT.prenom
        FROM ACHAT
        JOIN CLIENT ON ACHAT.client_id = CLIENT.id_client
        GROUP BY client_id
        ORDER BY total_depense DESC
        LIMIT 1;
    '''
    mycursor.execute(sql)
    client = mycursor.fetchone()
    return render_template('/Tables/Achat_etat.html', client=client)


@app.route('/Achats-vetements/show')
def show_achat_vetements():
    mycursor = get_db().cursor()
    sql = '''
        SELECT 
            av.id_achat_vetement,
            av.quantite_achete,
            av.id_achat,
            av.id_categorie_vetement,
            c.nom_vetement,
            a.date_achat
        FROM ACHAT_VETEMENT av
        JOIN CATEGORIE_VETEMENTS c 
            ON av.id_categorie_vetement = c.id_categorie_vetement
        JOIN ACHAT a
            ON av.id_achat = a.id_achat '''
    mycursor.execute(sql)
    Av = mycursor.fetchall()
    return render_template('Tables/Achats-vetements.html', Av=Av)


@app.route('/Achats-vetements/edit', methods=['GET'])
def edit_achat_vetement():
    mycursor = get_db().cursor()
    id_achat_vetement = request.args.get('id_achat_vetement')
    sql_av = "SELECT * FROM ACHAT_VETEMENT WHERE id_achat_vetement = %s"
    mycursor.execute(sql_av, (id_achat_vetement,))
    Av = mycursor.fetchone()
    sql_categories = "SELECT * FROM CATEGORIE_VETEMENTS"
    mycursor.execute(sql_categories)
    categories = mycursor.fetchall()
    return render_template('Tables/Achats-vetements_edit.html', Av=Av, categories=categories)



@app.route('/Achats-vetements/edit', methods=['POST'])
def valid_edit_achat_vetement():
    id_achat_vetement = request.form.get('id_achat_vetement')
    quantite_achete = request.form.get('quantite_achete')
    id_categorie_vetement = request.form.get('id_categorie_vetement')
    id_achat = request.form.get('id_achat')
    date_achat = request.form.get('date_achat')  # <-- nouvelle ligne

    mycursor = get_db().cursor()
    sql = """
        UPDATE ACHAT_VETEMENT av
        JOIN ACHAT a ON av.id_achat = a.id_achat
        SET av.quantite_achete = %s,
            av.id_categorie_vetement = %s,
            av.id_achat = %s,
            a.date_achat = %s
        WHERE av.id_achat_vetement = %s
    """
    mycursor.execute(sql, (quantite_achete, id_categorie_vetement, id_achat, date_achat, id_achat_vetement))
    get_db().commit()

    flash(f"Achat de vêtement {id_achat_vetement} modifié avec succès !")
    return redirect('/Achats-vetements/show')




@app.route('/Achats-vetements/delete', methods=['GET'])
def delete_achat_vetement():
    mycursor = get_db().cursor()
    id_achat_vetement = request.args.get('id_achat_vetement')
    tuple_delete = (id_achat_vetement,)
    sql = "DELETE FROM ACHAT_VETEMENT WHERE id_achat_vetement = %s"
    mycursor.execute(sql, tuple_delete)
    get_db().commit()
    flash('Un achat de vêtement a été supprimé : ' + id_achat_vetement)
    return redirect('/Achats-vetements/show')


@app.route('/Achats-vetements/add', methods=['GET'])
def add_achat_vetement():
    mycursor = get_db().cursor()
    sql = "SELECT id_categorie_vetement, nom_vetement FROM CATEGORIE_VETEMENTS"
    mycursor.execute(sql)
    categories = mycursor.fetchall()
    return render_template('Tables/Achats-vetements_add.html', categories=categories)


@app.route('/Achats-vetements/add', methods=['POST'])
def valid_add_achat_vetement():
    print("Ajout d'un nouvel achat de vêtement...")
    id_achat = request.form.get('id_achat')
    quantite_achete = request.form.get('quantite_achete')
    id_categorie_vetement = request.form.get('id_categorie_vetement')
    date_achat = request.form.get('date_achat')
    print(f"ID achat = {id_achat}, quantité = {quantite_achete}, date = {date_achat}")
    mycursor = get_db().cursor()
    sql_insert = """
        INSERT INTO ACHAT_VETEMENT (id_achat, id_categorie_vetement, quantite_achete)
        VALUES (%s, %s, %s)
    """
    mycursor.execute(sql_insert, (id_achat, id_categorie_vetement, quantite_achete))
    sql_update_date = "UPDATE ACHAT SET date_achat = %s WHERE id_achat = %s"
    mycursor.execute(sql_update_date, (date_achat, id_achat))
    get_db().commit()
    flash("Nouvel achat de vêtement ajouté avec succès !")
    return redirect('/Achats-vetements/show')

@app.route('/Depose/show')
def show_depose():
    return render_template('Tables/Depose.html')
    
@app.route('/Collecte-vetements/show')
def show_collecte_vetements():
    mycursor = get_db().cursor()
    sql = ''' SELECT cv.id_collecte_vetement,cv.date_collecte, cv.quantite_vetement, cv.collecte_id, cv.id_categorie_vetement, c.nom_vetement FROM COLLECTE_VETEMENT cv JOIN CATEGORIE_VETEMENTS c ON cv.id_categorie_vetement = c.id_categorie_vetement'''
    mycursor.execute(sql)
    Collecte = mycursor.fetchall()
    return render_template('Tables/Collecte-vetements.html', Collecte=Collecte)

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
    mycursor = get_db().cursor()
    mycursor.execute("SELECT id_categorie_vetement, nom_vetement FROM CATEGORIE_VETEMENTS")
    Cat = mycursor.fetchall()
    mycursor.execute("SELECT id_collecte, date_collecte FROM COLLECTE")
    collectes = mycursor.fetchall()
    return render_template('Tables/Collecte-vetements_add.html', Cat=Cat, collectes=collectes)



@app.route('/Collecte-vetements/add', methods=['POST'])
def valid_add_collecte_vetements():
    print("Ajout d'une nouvelle collecte...")
    quantite_vetement = request.form.get('quantite_vetement')
    date_collecte = request.form.get('date_collecte')
    collecte_id = request.form.get('collecte_id')
    id_categorie_vetement = request.form.get('id_categorie_vetement')
    print(f"quantité = {quantite_vetement}, date = {date_collecte}")
    mycursor = get_db().cursor()
    sql = """ INSERT INTO COLLECTE_VETEMENT (collecte_id,quantite_vetement, date_collecte,id_categorie_vetement) VALUES (%s, %s,%s,%s)"""
    tuple_insert = (collecte_id, quantite_vetement, date_collecte,id_categorie_vetement)
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


# ------------------- DEPOSE -------------------
@app.route('/Depose/show')
def show_depose():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT d.num_depot, d.id_depot, d.quantite_depot, d.date_depot,
               c.nom AS client_nom, c.prenom AS client_prenom, c.id_client,
               cv.nom_vetement, cv.id_categorie_vetement
        FROM DEPOSE d
        JOIN CLIENT c ON d.id_client = c.id_client
        JOIN CATEGORIE_VETEMENTS cv ON d.id_categorie_vetement = cv.id_categorie_vetement
        ORDER BY d.num_depot
    ''')
    depose_list = cursor.fetchall()
    return render_template('Tables/Depose.html', depose_list=depose_list)

@app.route('/Depose/add', methods=['GET'])
def add_depose():
    cursor = get_db().cursor()
    cursor.execute('SELECT id_client, nom, prenom FROM CLIENT')
    clients = cursor.fetchall()
    cursor.execute('SELECT id_categorie_vetement, nom_vetement FROM CATEGORIE_VETEMENTS')
    categories = cursor.fetchall()
    cursor.execute('SELECT id_depot FROM DEPOT')
    depots = cursor.fetchall()
    return render_template('Tables/Depose_add.html', clients=clients, categories=categories, depots=depots)

@app.route('/Depose/add', methods=['POST'])
def valid_add_depose():
    cursor = get_db().cursor()
    cursor.execute('''
        INSERT INTO DEPOSE(quantite_depot, date_depot, id_depot, id_categorie_vetement, id_client)
        VALUES (%s, %s, %s, %s, %s)
    ''', (
        request.form.get('quantite_depot'),
        request.form.get('date_depot'),
        request.form.get('id_depot'),
        request.form.get('id_categorie_vetement'),
        request.form.get('id_client')
    ))
    get_db().commit()
    return redirect('/Depose/show')

@app.route('/Depose/edit', methods=['GET'])
def edit_depose():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM DEPOSE WHERE num_depot=%s', (request.args.get('id'),))
    depose = cursor.fetchone()
    cursor.execute('SELECT id_client, nom, prenom FROM CLIENT')
    clients = cursor.fetchall()
    cursor.execute('SELECT id_categorie_vetement, nom_vetement FROM CATEGORIE_VETEMENTS')
    categories = cursor.fetchall()
    cursor.execute('SELECT id_depot FROM DEPOT')
    depots = cursor.fetchall()
    return render_template('Tables/Depose_edit.html', depose=depose, clients=clients, categories=categories, depots=depots)

@app.route('/Depose/edit', methods=['POST'])
def valid_edit_depose():
    cursor = get_db().cursor()
    cursor.execute('''
        UPDATE DEPOSE
        SET quantite_depot=%s, date_depot=%s, id_depot=%s,
            id_categorie_vetement=%s, id_client=%s
        WHERE num_depot=%s
    ''', (
        request.form.get('quantite_depot'),
        request.form.get('date_depot'),
        request.form.get('id_depot'),
        request.form.get('id_categorie_vetement'),
        request.form.get('id_client'),
        request.form.get('num_depot')
    ))
    get_db().commit()
    return redirect('/Depose/show')

@app.route('/Depose/delete')
def delete_depose():
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM DEPOSE WHERE num_depot=%s', (request.args.get('id'),))
    get_db().commit()
    return redirect('/Depose/show')

# ------------------- FIN DEPOSE -------------------

if __name__ == '__main__':
    app.run(debug=True)













