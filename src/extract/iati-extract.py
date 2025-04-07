from diterator import Iterator

ROLES = {
    '1': 'Funding',
    '2': 'Accountable',
    '3': 'Extending',
    '4': 'Implementing',
}

activities = Iterator({
    "country_code": "ke",
    "status_code": "2",   # implementation
})

for activity in activities:
    print('Activity:', activity.title)
    print('', 'Reporting org:', activity.reporting_org.name)
    for org in activity.participating_orgs:
        print('', 'Participating org:', org.name, ROLES.get(org.role, "unknown"))

    connections = set()
    for transaction in activity.transactions:
        provider_org = None
        receiver_org = None
        if (transaction.provider_org):
            provider_org = str(transaction.provider_org)
        if (transaction.receiver_org):
            receiver_org = str(transaction.receiver_org)
        if provider_org or receiver_org:
            connections.add((provider_org, receiver_org,))
        if len(connections) > 0:
            print('', 'Connections:')
            for connection in connections:
                print('', '', connection[0], '=>', connection[1])
