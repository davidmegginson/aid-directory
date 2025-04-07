from diterator import Iterator

activities = Iterator({
    "country_code": "ke",
    "status_code": "2",   # implementation
})

for activity in activities:
    print("Activity", activity.title)
    print("  Reporting org: ", activity.reporting_org.name)
    for org in activity.participating_orgs:
        print("  Participating org: ", org.name)
