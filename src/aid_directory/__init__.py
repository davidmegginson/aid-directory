from flask import Flask, render_template

from .data import *

app = Flask(__name__)

@app.route("/")
def show_home():
    return render_template('show-home.html')

@app.route("/orgs/")
def list_orgs():
    orgs = data.get_orgs()
    return render_template('list-orgs.html', orgs=orgs)

@app.route("/orgs/<org_id>/")
def show_org(org_id):
    org = data.get_org(org_id)
    return render_template('show-org.html', org=org)

@app.route("/sectors/")
def list_sectors():
    sectors = data.get_sectors()
    return render_template('list-sectors.html', sectors=sectors)

@app.route("/sectors/<sector_type>/<sector_code>/")
@app.route("/sectors/<sector_type>/<org_id>/<sector_code>/")
def show_sector(sector_type, sector_code, org_id=None):
    sector = data.get_sector(sector_type, sector_code, org_id)
    return render_template('show-sector.html', sector=sector)
