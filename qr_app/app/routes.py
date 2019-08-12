from flask import render_template, redirect, flash
from app import app
from app.forms import ScanForm


@app.route('/')
@app.route('/index')
def index():
    qr = {'code': '323242'}
    return render_template('index.html', title='Home', qr=qr)


@app.route('/qr_scan', methods=['GET', 'POST'])
def qr_scan():
    # qr = {'code': '323242'}
    allowed = [606676, 384021, 992843, 261807, 269149, 644929, 450422, 803814]

    form = ScanForm()
    if form.validate_on_submit():
        if form.codigo.data in allowed:
            flash('Acceso APROBADO manilla {}'.format(form.codigo.data))
            return redirect('/qr_scan')
        else:
            flash('Acceso DENEGADO a manilla {}'.format(form.codigo.data))
            return redirect('/qr_scan')

    return render_template('scanner.html', title='Sign In', form=form)
