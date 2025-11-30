from flask import Flask, render_template, request, redirect, flash
from datetime import date
app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

from flask import session, g
import pymysql.cursors

def get_db():
    if 'db' not in g:
        g.db =  pymysql.connect(
            host="192.168.1.124",                 # à modifier
            user="user",                     # à modifier
            password="secret",                   # à modifier
            database="sae",        # à modifier
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

@app.teardown_appcontext
def teardown_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# ------------------- LAYOUT -------------------
@app.route('/')
def show_layout():
    return render_template('layout.html')


# ------------------- ACHAT -------------------
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
    mycursor = get_db().cursor()
    sql=''' SELECT id_client, nom, prenom
    FROM CLIENT;'''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('Tables/Achat_add.html',clients=clients)

@app.route('/Achat/add', methods=['POST'])
def valid_add_achat():
    client_id = request.form.get('client_id')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    if not date_achat:
        date_achat = date.today().strftime("%Y-%m-%d")
    mycursor = get_db().cursor()
    tuple_param=(client_id, montant_total, poids_total, date_achat)
    sql="INSERT INTO ACHAT(client_id, montant_total, poids_total, date_achat ) VALUES (%s, %s, %s, %s);"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/Achat/show')

@app.route('/Achat/edit', methods=["GET"])
def edit_achat():
    id_achat=request.args.get('id_achat')
    mycursor = get_db().cursor()
    sql=''' SELECT id_achat , client_id,  montant_total , poids_total ,date_achat 
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
    id_achat=request.form.get('id_achat')
    client_id = request.form.get('client_id')
    montant_total = request.form.get('montant_total')
    poids_total = request.form.get('poids_total')
    date_achat = request.form.get('date_achat')
    mycursor = get_db().cursor()
    tuple_param=(client_id, montant_total, poids_total, date_achat, id_achat)
    sql="UPDATE ACHAT SET client_id = %s, montant_total = %s, poids_total = %s, date_achat = %s WHERE id_achat=%s;"
    mycursor.execute(sql,tuple_param)
    get_db().commit()
    return redirect('/Achat/show')

@app.route('/Achat/delete')
def delete_achat():
    id_achat=request.args.get('id_achat',0)
    mycursor = get_db().cursor()
    tuple_param=(id_achat,)
    sql = "DELETE FROM ACHAT_VETEMENT WHERE achat_id=%s;"
    mycursor.execute(sql, tuple_param)
    sql="DELETE FROM ACHAT WHERE id_achat=%s;"
    mycursor.execute(sql,tuple_param)  
    get_db().commit()
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
        LIMIT 3;
    '''
    mycursor.execute(sql)
    clients = mycursor.fetchall()
    return render_template('/Tables/Achat_etat.html', clients=clients)

@app.route('/Achat/etat', methods=['POST'])
def show_etat_param():
    date_debut = request.form.get('date_debut')
    date_fin = request.form.get('date_fin')
    mycursor = get_db().cursor()
    sql_client = '''
        SELECT client_id, SUM(montant_total) AS total_depense,COUNT(id_achat) AS nb_achat, CLIENT.nom, CLIENT.prenom
        FROM ACHAT
        JOIN CLIENT ON ACHAT.client_id = CLIENT.id_client
        GROUP BY client_id
        ORDER BY total_depense DESC
        LIMIT 3;
    '''
    mycursor.execute(sql_client)
    clients = mycursor.fetchall()

    sql= '''
        SELECT CLIENT.nom, CLIENT.prenom, COUNT(ACHAT.id_achat) AS nb_achats, SUM(ACHAT.montant_total) AS total_acheté, SUM(ACHAT.poids_total) AS total_poids, AVG(ACHAT.montant_total) AS moyenne_acheté, AVG(ACHAT.poids_total) AS moyenne_poids
        FROM ACHAT 
        JOIN CLIENT ON ACHAT.client_id = CLIENT.id_client
        WHERE ACHAT.date_achat BETWEEN %s AND %s
        GROUP BY CLIENT.id_client
        ORDER BY total_acheté DESC;
    '''
    parametre=(date_debut, date_fin)
    mycursor.execute(sql, parametre)
    liste_client = mycursor.fetchall()
    return render_template('/Tables/Achat_etat.html', liste_client=liste_client, date_debut=date_debut, date_fin=date_fin, clients=clients)


# ------------------- ACHATS VETEMENTS -------------------
@app.route('/Achats-vetements/show')
def show_achat_vetements():
    mycursor = get_db().cursor()
    sql = '''
        SELECT 
            av.id_achat_vetement,
            av.quantite_achete,
            av.achat_id,
            av.categorie_vetement_id,
            c.nom_vetement,
            a.date_achat,
            a.client_id,
            cl.nom,
            cl.prenom
        FROM ACHAT_VETEMENT av
        JOIN CATEGORIE_VETEMENTS c 
            ON av.categorie_vetement_id = c.id_categorie_vetement
        JOIN ACHAT a
            ON av.achat_id = a.id_achat
        JOIN CLIENT cl
            ON a.client_id = cl.id_client '''
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
    sql_achats = '''SELECT id_achat, date_achat, client_id, CLIENT.nom, CLIENT.prenom 
    FROM ACHAT 
    JOIN CLIENT 
    ON ACHAT.client_id = CLIENT.id_client 
    ORDER BY id_achat DESC'''
    mycursor.execute(sql_achats)
    achats = mycursor.fetchall()
    return render_template('Tables/Achats-vetements_edit.html', Av=Av, categories=categories, achats=achats)



@app.route('/Achats-vetements/edit', methods=['POST'])
def valid_edit_achat_vetement():
    id_achat_vetement = request.form.get('id_achat_vetement')
    quantite_achete = request.form.get('quantite_achete')
    categorie_vetement_id = request.form.get('categorie_vetement_id')
    achat_id = request.form.get('achat_id')

    mycursor = get_db().cursor()
    sql = """
        UPDATE ACHAT_VETEMENT
        SET quantite_achete = %s,
            categorie_vetement_id = %s,
            achat_id = %s
        WHERE id_achat_vetement = %s
    """
    mycursor.execute(sql, (quantite_achete, categorie_vetement_id, achat_id, id_achat_vetement))
    
    sql_somme_poids = "SELECT SUM(quantite_achete) as poids FROM ACHAT_VETEMENT WHERE achat_id = %s"
    mycursor.execute(sql_somme_poids, (achat_id,))
    result = mycursor.fetchone()
    poids_total = result['poids']
    sql_update_poids = "UPDATE ACHAT SET poids_total = %s WHERE id_achat = %s"
    mycursor.execute(sql_update_poids, (poids_total, achat_id))
    
    get_db().commit()

    flash(f"Achat de vêtement {id_achat_vetement} modifié avec succès !")
    return redirect('/Achats-vetements/show')




@app.route('/Achats-vetements/delete', methods=['GET'])
def delete_achat_vetement():
    mycursor = get_db().cursor()
    id_achat_vetement = request.args.get('id_achat_vetement')
    sql_get_achat_id = "SELECT achat_id FROM ACHAT_VETEMENT WHERE id_achat_vetement = %s"
    mycursor.execute(sql_get_achat_id, (id_achat_vetement,))
    result = mycursor.fetchone()
    achat_id = result['achat_id']

    tuple_delete = (id_achat_vetement,)
    sql = "DELETE FROM ACHAT_VETEMENT WHERE id_achat_vetement = %s"
    mycursor.execute(sql, tuple_delete)

    sql_somme_poids = "SELECT SUM(quantite_achete) as poids FROM ACHAT_VETEMENT WHERE achat_id = %s"
    mycursor.execute(sql_somme_poids, (achat_id,))
    result = mycursor.fetchone()
    poids_total = result['poids']
    sql_update_poids = "UPDATE ACHAT SET poids_total = %s WHERE id_achat = %s"
    mycursor.execute(sql_update_poids, (poids_total, achat_id))

    get_db().commit()
    flash('Un achat de vêtement a été supprimé : ' + id_achat_vetement)
    return redirect('/Achats-vetements/show')


@app.route('/Achats-vetements/add', methods=['GET'])
def add_achat_vetement():
    mycursor = get_db().cursor()
    sql = "SELECT id_categorie_vetement, nom_vetement FROM CATEGORIE_VETEMENTS"
    mycursor.execute(sql)
    categories = mycursor.fetchall()
    sql_achats = '''SELECT id_achat, date_achat, client_id, CLIENT.nom, CLIENT.prenom 
    FROM ACHAT 
    JOIN CLIENT 
    ON ACHAT.client_id = CLIENT.id_client 
    ORDER BY id_achat DESC'''
    mycursor.execute(sql_achats)
    achats = mycursor.fetchall()
    return render_template('Tables/Achats-vetements_add.html', categories=categories, achats=achats)


@app.route('/Achats-vetements/add', methods=['POST'])
def valid_add_achat_vetement():
    print("Ajout d'un nouvel achat de vêtement...")
    achat_id = request.form.get('achat_id')
    quantite_achete = request.form.get('quantite_achete') or 0
    categorie_vetement_id = request.form.get('categorie_vetement_id')
    date_achat = request.form.get('date_achat') or date.today().strftime("%Y-%m-%d")
    print(f"ID achat = {achat_id}, quantité = {quantite_achete}, date = {date_achat}")
    mycursor = get_db().cursor()
    sql_insert = """
        INSERT INTO ACHAT_VETEMENT (achat_id, categorie_vetement_id, quantite_achete)
        VALUES (%s, %s, %s)
    """
    mycursor.execute(sql_insert, (achat_id, categorie_vetement_id, quantite_achete))
    sql_update_date = "UPDATE ACHAT SET date_achat = %s WHERE id_achat = %s"
    mycursor.execute(sql_update_date, (date_achat, achat_id))
    sql_somme_poids = "SELECT SUM(quantite_achete) as poids FROM ACHAT_VETEMENT WHERE achat_id = %s"
    mycursor.execute(sql_somme_poids, (achat_id,))
    result = mycursor.fetchone()
    poids_total = result['poids']
    sql_update_poids = "UPDATE ACHAT SET poids_total = %s WHERE id_achat = %s"
    mycursor.execute(sql_update_poids, (poids_total, achat_id))
    get_db().commit()
    return redirect('/Achats-vetements/show')



@app.route('/Achats-vetements/etat', methods=['GET'])
def show_achat_vetement_etat():
    mycursor = get_db().cursor()
    sql = '''
        SELECT c.nom_vetement, SUM(av.quantite_achete) as total_quantite
        FROM ACHAT_VETEMENT av
        JOIN CATEGORIE_VETEMENTS c ON av.categorie_vetement_id = c.id_categorie_vetement
        GROUP BY c.nom_vetement
        ORDER BY total_quantite DESC
    '''
    mycursor.execute(sql)
    global_stats = mycursor.fetchall()
    return render_template('Tables/Achats-vetements_etat.html', global_stats=global_stats)


@app.route('/Achats-vetements/etat', methods=['POST'])
def show_achat_vetement_etat_param():
    min_quantite = request.form.get('min_quantite')
    max_quantite = request.form.get('max_quantite')
    mycursor = get_db().cursor()
    sql_global = '''
        SELECT c.nom_vetement, SUM(av.quantite_achete) as total_quantite
        FROM ACHAT_VETEMENT av
        JOIN CATEGORIE_VETEMENTS c ON av.categorie_vetement_id = c.id_categorie_vetement
        GROUP BY c.nom_vetement
        ORDER BY total_quantite DESC
    '''
    mycursor.execute(sql_global)
    global_stats = mycursor.fetchall()
    sql_filtered = '''
        SELECT c.nom_vetement, SUM(av.quantite_achete) as total_quantite, AVG(av.quantite_achete) as moy_quantite, COUNT(av.id_achat_vetement) as nb_achats
        FROM ACHAT_VETEMENT av
        JOIN CATEGORIE_VETEMENTS c ON av.categorie_vetement_id = c.id_categorie_vetement
        GROUP BY c.nom_vetement
        HAVING total_quantite BETWEEN %s AND %s
        ORDER BY total_quantite DESC
    '''
    mycursor.execute(sql_filtered, (min_quantite, max_quantite))
    stats_filtrees = mycursor.fetchall()
    
    return render_template('Tables/Achats-vetements_etat.html', global_stats=global_stats, stats_filtrees=stats_filtrees, min_quantite=min_quantite, max_quantite=max_quantite)


# ------------------- COLLECTE VETEMENTS -------------------
@app.route('/Collecte-vetements/show')
def show_collecte_vetements():
    mycursor = get_db().cursor()
    sql = ''' SELECT cv.id_collecte_vetement,cv.date_collecte, cv.quantite_vetement, cv.collecte_id, cv.categorie_vetement_id, c.nom_vetement FROM COLLECTE_VETEMENT cv JOIN CATEGORIE_VETEMENTS c ON cv.categorie_vetement_id = c.id_categorie_vetement'''
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
    categorie_vetement_id = request.form.get('categorie_vetement_id')
    print(f"quantité = {quantite_vetement}, date = {date_collecte}")
    mycursor = get_db().cursor()
    sql = """ INSERT INTO COLLECTE_VETEMENT (collecte_id,quantite_vetement, date_collecte,categorie_vetement_id) VALUES (%s, %s,%s,%s)"""
    tuple_insert = (collecte_id, quantite_vetement, date_collecte,categorie_vetement_id)
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
        SELECT d.id_depose, d.quantite_depot, d.date_depot,
               d.depot_id,
               c.id_client AS client_id, c.nom AS client_nom, c.prenom AS client_prenom,
               cv.id_categorie_vetement AS categorie_vetement_id, cv.nom_vetement
        FROM DEPOSE d
        JOIN CLIENT c ON d.client_id = c.id_client
        JOIN CATEGORIE_VETEMENTS cv ON d.categorie_vetement_id = cv.id_categorie_vetement
        ORDER BY d.id_depose
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
    date_today = date.today().strftime("%Y-%m-%d")
    return render_template('Tables/Depose_add.html', clients=clients, categories=categories, depots=depots, date_today=date_today)


@app.route('/Depose/add', methods=['POST'])
def valid_add_depose():
    cursor = get_db().cursor()
    cursor.execute('''
        INSERT INTO DEPOSE (quantite_depot, date_depot, depot_id, categorie_vetement_id, client_id)
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
    cursor.execute('SELECT * FROM DEPOSE WHERE id_depose=%s', (request.args.get('id'),))
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
        SET quantite_depot=%s, date_depot=%s, depot_id=%s,
            categorie_vetement_id=%s, client_id=%s
        WHERE id_depose=%s
    ''', (
        request.form.get('quantite_depot'),
        request.form.get('date_depot'),
        request.form.get('id_depot'),
        request.form.get('id_categorie_vetement'),
        request.form.get('id_client'),
        request.form.get('id_depose')
    ))
    get_db().commit()
    return redirect('/Depose/show')


@app.route('/Depose/delete')
def delete_depose():
    cursor = get_db().cursor()
    cursor.execute('DELETE FROM DEPOSE WHERE id_depose=%s', (request.args.get('id'),))
    get_db().commit()
    return redirect('/Depose/show')


# Route existante (total déposé par client)
@app.route('/Depose/etat')
def show_etat_depose():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT c.id_client, c.nom, c.prenom, SUM(d.quantite_depot) AS total_depose
        FROM DEPOSE d
        JOIN CLIENT c ON d.client_id = c.id_client
        GROUP BY c.id_client, c.nom, c.prenom
        ORDER BY total_depose DESC
    ''')
    etat_list = cursor.fetchall()
    return render_template('Tables/Depose_etat.html', etat_list=etat_list)


@app.route('/Depose/etat2')
def show_etat_depose2():
    cursor = get_db().cursor()
    cursor.execute('''
        SELECT c.id_client, c.nom, c.prenom, COUNT(d.id_depose) AS nb_depots
        FROM DEPOSE d
        JOIN CLIENT c ON d.client_id = c.id_client
        GROUP BY c.id_client, c.nom, c.prenom
        ORDER BY nb_depots DESC
    ''')
    etat2_list = cursor.fetchall()
    return render_template('Tables/Depose_etat2.html', etat2_list=etat2_list)


# ------------------- FIN DEPOSE -------------------



if __name__ == '__main__':
    app.run(debug=True)




