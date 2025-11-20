from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

@app.route('/')
def show_layout():
    return render_template('layout.html')


@app.route('/Achats/show')
def show_achat():
    return render_template('Tables/Achats.html')

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
