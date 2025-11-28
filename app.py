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
            password="secret",                   # à modifier
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
    sql=''' SELECT client_id, nom, prenom
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
        LIMIT 1;
    '''
    mycursor.execute(sql)
    client = mycursor.fetchone()
    return render_template('/Tables/Achat_etat.html', client=client)


# ------------------- ACHATS VETEMENTS -------------------
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


# ------------------- COLLECTE VETEMENTS -------------------
@app.route('/Collecte-vetements/show')
def show_collecte_vetements():
    mycursor = get_db().cursor()
    sql = ''' SELECT cv.id_collecte_vetement,cv.date_collecte, cv.quantite_vetement, cv.collecte_id, cv.id_categorie_vetement, c.nom_vetement FROM COLLECTE_VETEMENT cv JOIN CATEGORIE_VETEMENTS c ON cv.id_categorie_vetement = c.id_categorie_vetement'''
    mycursor.execute(sql)
    Collecte = mycursor.fetchall()
    return render_template('Tables/Collecte-vetements.html', Collecte=Collecte)


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
