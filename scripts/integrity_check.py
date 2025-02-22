#!/usr/bin/env python
'''
Check integrity of record links in raw airtable export.

First need to run airtable_export.py to produce the raw airtable export. 
This saves the 'bases' dict to a json file.

Usage:
    python integrity_check.py

'''
import json
import argparse

parser = argparse.ArgumentParser(description='Simple script to check consistency of links between tables in json file created by airtable_export.py.')
parser.add_argument('filepath', type=str, help=\
                    f'exported content json file to check')
parser.add_argument('-r', '--release', type=str, default='', help=\
                    'if this is an official release export, give the release tag (example: -r v1.0beta)')
args = parser.parse_args()

filepath = args.filepath
with open(filepath, 'r') as f:
    bases = json.load(f)
    print(f'Opened {filepath}')

# Show names of bases, their tables, and number of records in each table
for base_name, tables in bases.items():
    print(base_name)
    for table_name, table in tables.items():
        nrec = len(table['records'])
        print(f'  {table_name}  ({nrec} records)')


def check_id(uid : str, uid_type : str) -> bool:
    '''
    Return True if input string uid has the expected format for unique identifiers in an airtable export via pyairtable.
    Example: 'rec00yWOulzoqJuY7' (for a record id string)
    '''
    uid_prefix = {'record' : 'rec', 'field' : 'fld', 'base' : 'app', 'table' : 'tbl'}
    prefix = uid_prefix[uid_type]
    return isinstance(uid, str) and uid.startswith(prefix) and len(uid) == 17

# Check integrity of record links in each base
for base_name, tables in bases.items():
    print('\n' + base_name)

    table_id2name = {table['id'] : table['name'] for table in tables.values()} # given table id, look up table name
    n = len(tables)
    assert len(set(table_id2name.keys())) == n, 'table ids are not unique'
    assert len(set(table_id2name.values())) == n, 'table names are not unique'

    # For the tables in this base, check that linked records point to valid records in the indicated linked table
    for table_name, table in tables.items():
        print(table_name)

        # if args.release == '':  # if this is a working bases export

        #     # Fixing issue with non-unique field names in v1.0 working bases export
        #     remove_field_id = []
        #     for field_id, field in table['fields'].items():
        #         if table_name == 'Experiment Group':
        #             pass
        #             # if field['name'] == 'Experiments' and field['description'] is None:
        #             #     remove_field_id.append(field_id)
        #         elif table_name == 'Opportunity':
        #             if field['name'] == 'Comments' and field['description'] is None:
        #                 remove_field_id.append(field_id)
        #         elif table_name == 'Variable':
        #             if field['name'] == 'Comments' and field['description'] is None:
        #                 remove_field_id.append(field_id)

        #     for field_id in remove_field_id:
        #         print(f'Removing field {field_id} in table {table_name}')
        #         table['fields'].pop(field_id)
        #     del remove_field_id

        # Make dict with info on fields, indexed by field name (instead of field id)
        fields = {}
        for field_id, field in table['fields'].items():
            name = field['name']
            assert name not in fields, f'field names in table {table_name} are not unique: {name}'
            fields[name] = field

        records = table['records']
        for record in records.values():
            for name in record:
                field = fields[name]
                if 'linked_table_id' in field:
                    # This field in the record contains a list of links to records in another table
                    record_links = record[name]  # list of record ids

                    assert isinstance(record_links, list), 'links to other records should be in a list'
                    # if not isinstance(record_links, list):
                    #     print(f'Skipping invalid link in {table_name} for field: {name}')
                    #     continue


                    #     print()
                    #     print(table_name)
                    #     print(record['Title of Opportunity'])
                    #     print(record['Comments'])
                    #     print()
                    #     print(name)
                    #     print(record_links)
                    #     print(type(record_links))
                    #     stop

                    assert all([check_id(uid, 'record') for uid in record_links]), 'unrecognized format for record links'
                    
                    linked_table_name = table_id2name[ field['linked_table_id'] ]
                    for uid in record_links:
                        assert uid in tables[linked_table_name]['records'], 'record id not found in linked table'

# If we've got this far without errors, the integrity of links is ok.
print('\nNo link errors found in exported Airtable bases')

# While we're here, check uniqueness of variable Compound Names
if args.release != '':
    check_base_tables = {
        f'Data Request {args.release}' : ['Variables'],
    }
else:
    check_base_tables = {
        'Data Request Variables (Public)' : ['Variable'],
        'Data Request Opportunities (Public)' : ['Variables']
    }
for base_name in check_base_tables:
    print(f'\nChecking uniqueness of Compound Name in base: {base_name}')
    for table_name in check_base_tables[base_name]:
        print(f'  Checking table: {table_name}')
        if base_name not in bases:
            msg = f'Base name not found: "{base_name}"'
            msg += '\nDoes the release version need to be specified? Invoke with -r option, example: -r v1.0beta'
            raise Exception(msg)
        table = bases[base_name][table_name]
        nrec = len(table['records'])
        names = [ record['Compound Name'] for record in table['records'].values() ]
        print(f'    number of variables: {nrec}')
        n = len(set(names))
        print(f'    number of unique Compound Names: {n}')

