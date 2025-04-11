Aid Directory
=============

Early prototype for an online directory of aid organisations.

## System prerequisites

- Unix-like shell environment
- Python3
- Gnu Make

## Usage

    $ cd src && make
    
This will create or overwrite the file ``output/orgs.csv`` (running time is fairly long, so head out for a tea or coffee).  It's currently hardcoded to included only current IATI activities that affect Madagascar, though many of them affect other countries as well.

## Output format

The output is a single CSV file containing denormalised information about aid organisations discovered in published IATI activities, and by implication, the relationships among those organisations.  The file has the following columns:

- ``org_name`` - the human-readable organisation name in the activity's default language
- ``org_id`` - the organisation's IATI identifier (if available)
- ``source`` - always "iati" for now (will include other sources later)
- ``activity_name`` - the human-readable name of the aid activity that the org is involved in, in the activity's default language
- ``activity_id`` - the activity's IATI identifier
- ``is_humanitarian`` - 1 if the activity as a whole appears to be related to humanitarian aid; 0 otherwise
- ``country_name`` - the country's human-readable name, in English
- ``country_code`` - the country's ISO 3166-1 alpha2 country code
- ``sector_name`` - the aid-sector name in the activity's default language
- ``sector_code`` - the aid-sector's code
- ``sector_type`` - a code for the aid-sector vocabulary used (OECD DAC is most common)
- ``org_role`` - the role the org plays in the activity (Reporting, Funding, Accountable, Extending, Implementing, Provider, Receiver)
- ``relationship_index`` - an index for the unique provider/receiver relationships found in the activity's transactions, so that one can reconstruct the direct funding connections

Rows are repeated for each activity, country, sector, org, role, and unique relationship.


## Author

David Megginson
