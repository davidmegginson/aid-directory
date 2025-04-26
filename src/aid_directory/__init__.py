from flask import Flask, render_template

from .data import *

app = Flask(__name__)

@app.route("/orgs/")
def show_orgs():
    orgs = sorted(data.get_orgs(), key=lambda x: x['org_name'])
    return render_template('list-orgs.html', orgs=orgs)

@app.route("/orgs/<org_id>/")
def show_org(org_id):
    org = data.get_org(org_id)
    return render_template('show-org.html', org=org)

@app.route("/sectors/<sector_type>/<sector_code>/")
def show_sector(sector_type, sector_code):
    sector = data.get_sector(sector_type, sector_code)
    return render_template('show-sector.html', sector=sector)
