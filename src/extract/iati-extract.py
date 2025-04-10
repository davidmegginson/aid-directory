""" Demonstrate extracting IATI organisation information from D-Portal
"""

import csv, sys
from diterator import Iterator

ROLES = {
    '1': 'Funding',
    '2': 'Accountable',
    '3': 'Extending',
    '4': 'Implementing',
}
""" IATI org role codelist """


def org2str (org):
    orgname = None
    if org:
        orgname = str(org.name)
        if org.ref:
            orgname = orgname + " (" + org.ref + ")"
    return orgname


def show_org (output, org, activity, default_role='', transaction_ref='', transaction_num=''):
    output.writerow([
        org.name,
        org.ref,
        'iati',
        activity.title,
        activity.identifier,
        org.role if org.role else default_role,
        transaction_ref,
        transaction_num,
    ])


def show_activity (output, activity):
    """ Display an activity to standard output """
    show_org(output, activity.reporting_org, activity, 'reporting')

    for org in activity.participating_orgs:
        show_org(output, org, activity)

    # TODO reduce transactions to unique combos
    for (n, transaction) in enumerate(activity.transactions):
        if transaction.provider_org:
            show_org(transaction.provider_org, activity, 'provider', transaction.ref, n)
        if transaction.receiver_org:
            show_org(output, transaction.receiver_org, activity, 'receiver', transaction.ref, n)

def show_activities (activities):
    """ Display a list of activities to standard output """
    output = csv.writer(sys.stdout)
    output.writerow([
        'org_name',
        'org_id',
        'source',
        'activity_name',
        'activity_id',
        'org_role',
        'transaction_num',
        'transaction_id',
    ])
    for activity in activities:
        show_activity(output, activity)


# Main entry point

activities = Iterator({
    "country_code": "ke", # Kenya
    "status_code": "2",   # implementation
})
show_activities(activities)
