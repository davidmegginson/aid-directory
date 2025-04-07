""" Demonstrate extracting IATI organisation information from D-Portal
"""

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


def get_connections (activity):
    """ Return a set of tuples for all the unique provider/receiver org combos in an activity """
    connections = set()
    for transaction in activity.transactions:
        provider_org = None
        receiver_org = None
        provider_org = org2str(transaction.provider_org)
        receiver_org = org2str(transaction.receiver_org)
        if provider_org or receiver_org:
            connections.add((provider_org, receiver_org,))
    return connections


def show_activity (activity):
    """ Display an activity to standard output """
    print('Activity:', activity.title)
    print('', 'Reporting org:', org2str(activity.reporting_org))
    for org in activity.participating_orgs:
        print('', 'Participating org (' + ROLES.get(org.role, "unknown") + '):', org2str(org))
        
    connections = get_connections(activity)
    if len(connections) > 0:
        print('', 'Connections:')
        for connection in connections:
            print('', '', connection[0], '=>', connection[1])


def show_activities (activities):
    """ Display a list of activities to standard output """
    for activity in activities:
        show_activity(activity)


# Main entry point

activities = Iterator({
    "country_code": "ke", # Kenya
    "status_code": "2",   # implementation
})
show_activities(activities)
