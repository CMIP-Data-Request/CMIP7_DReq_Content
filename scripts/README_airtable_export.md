This explains how to export the Airtable content to json, and what's in the export.
The description here is reference for developers, and is given in detail to ensure reproducibility of the workflow.
**The json file of exported content is not intended for direct use by general users of the data request software**.


## How to export Airtable data request content

Steps:

1. Setup: create environment, clone/update this repository, create an airtable token.
2. Run `airtable_export.py` to generate a json file containing the exported data request content.
3. Run `integrity_check.py` to confirm the internal consistency of the exported file.
4. If (2) and (3) were done for a release export (an official release version of the data request content), run them again for the raw export so that its state at the same time as the release export is also captured.
5. Commit the changes and push to github.

Each step is described in more detail below.
[See here](#full-example) for a full workflow of all steps done for a release export.

### Setup

The script `airtable_export.py` requires the `pyairtable` package.
Example of how to create an environment with this package (has been tested in python 3.13):
```bash
python -m venv dreq_export_v1  # environment name is arbitrary, and a dir with this name will be created in the current dir
source dreq_export_v1/bin/activate
pip install pyairtable
```
To clone the repository:
```bash
git clone git@github.com:CMIP-Data-Request/CMIP7_DReq_Content.git
```
If the repository was already cloned, ensure the local version is up to date:
```bash
cd CMIP7_DReq_Content
git checkout main
git fetch --all
git pull
```

Creating an Airtable token is described below.

### How to create an export

To export:

```bash
source dreq_export_v1/bin/activate   # replace dreq_export_v1 with the path to your environment
cd CMIP7_DReq_Content/scripts
./airtable_export.py my_token_file -f ../airtable_export/my_export_file.json
```
The positional argument (`my_token_file`) is the name of a file containing the Airtable token (how to create this file is explained below).
If the optional filename (`-f`) argument is omitted then a default output filename will be used (example: `dreq_raw_export_2024-09-25_04h09m51sUTC.json`).

Exports should go into the `airtable_export/` directory.
The file naming convention to follow is:
```bash
dreq_release_export.json  # content of an official data request release
dreq_raw_export.json  # content of working bases
```
When an official (tagged) release is done, both the above files should be created at the (approximate) same time, so that for the same tag the content of `dreq_raw_export.json` is consistent with `dreq_release_export.json`.
In between releases, `dreq_raw_export.json` might be created and committed if needed (without modifying `dreq_release_export.json` on the same commit).

Other filenames for exported json files should not be commited to this repository, to avoid bloating it with unnecessary data (export files are typically ~20-40 MB each).

### How to check export integrity

After exporting, the internal consistency of any export file should be checked by running:
```
./integrity_check.py ../airtable_export/my_export_file.json
```
If the export is an official release, the version tag needs to be added, e.g.:
```
./integrity_check.py ../airtable_export/my_export_file.json -r v1.2.1
```
The script writes information about the check to stdout, and raises errors for problems.
If the checks fail, the export file should not be committed to the repository!

### Full example

Here are steps of the workflow to generate and commit a release export (v1.2 in this example), assuming that the setup steps have already been done and the token files are stored in a separate directory `airtable_keys` outside the repository:
```bash
cd CMIP7_DReq_Content/scripts
./airtable_export.py ../../airtable_keys/token_export_v1.2 -f ../airtable_export/dreq_release_export.json
./airtable_export.py ../../airtable_keys/token_export_public_working_bases -f ../airtable_export/dreq_raw_export.json
./integrity_check.py ../airtable_export/dreq_release_export.json -r v1.2
./integrity_check.py ../airtable_export/dreq_raw_export.json
```
If the integrity checks passed, commit and push:
```bash
cd ../airtable_export
git checkout -b v1.2rc
git add dreq_raw_export.json 
git add dreq_release_export.json 
git commit -m "v1.2rc content"
git push --set-upstream origin v1.2rc
```
where in this example it's a official release, so "v1.2rc" means v1.2 release candidate.
Then open a pull request for this branch [on github](https://github.com/CMIP-Data-Request/CMIP7_DReq_Content).
Ensure the `main` branch target repository is correct.
By default it's  `WCRP-CMIP/CMIP7_DReq_Content`, but it should be switched `CMIP-Data-Request/CMIP7_DReq_Content` if development is happening there.


## How to generate an Airtable token

A text file containing the Airtable token is required by `airtable_export.py` (the `my_token_file` in the above example).
This token is a unique key allowing access to Airtable so that base content can be exported using the `pyairtable` package.
Tokens are not meant to be shared with others, and shouldn't be committed to this repository.

In the web browser, sign into an Airtable account with access to the bases, go to the [token creation page](https://airtable.com/create/tokens), and click "Create new token".
The "Scopes" and "Access" for the token need to be added (some explanation of these is [here](https://airtable.com/developers/web/api/scopes)).
For "Scopes", select these ones:
```
data.records:read
See the data in records

schema.bases:read
See the structure of a base, like table names or field types
```
These scopes give read permission for records and schema information.
"Access" controls which bases are accessible via the token.
For the working version public bases (for the "raw export"), scroll to find:
```
Data Request Opportunities (Public)
Data Request Physical Parameters (Public)
Data Request Variables (Public)
```
and add all of these.
For a release base, scroll to find (e.g., for v1.2 of the data request):
```
Data Request v1.2
```
Hit "Create token" and cut-paste the token string (a long string of random characters) into a text file.
Good practice is to include meaningful comments saying what the token is for (`airtable_export.py` ignores the comments), for example:
```
# Read-only key for these CMIP7 data request bases: 
#   Data Request v1.2
# Scopes:
#    data.records:read
#      See the data in records
#    schema.bases:read
#      See the structure of a base, like table names or field types
# Name of token on airtable:
#   ja_export_v1.2
# Airtable account:
#   data-request-coleads@wcrp-cmip.org
# URL where token was created:
#   https://airtable.com/create/tokens/new

pat635xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```
where "pat635xx..." is the token string.

A given token only provides access to the specified bases and scopes.
It doesn't give general access to all bases owned by the Airtable account in which it was generated.


## Structure of the exported content

The json file basic structure is:
```
{
    'base name 1' : {
        'table name 1' : {
            ...
            'records' : { # dict to contain all records (rows) in the table, indexed by each record's unique id string
                record id 1 : {record info}
                record id 2 : {record info}
                ...
            },
            'fields' : { # dict to contain schema info about the fields found in each record
                field id 1 : {field info}
                field id 2 : {field info}
                ...
            },
        'table name 2' : {...}
        ...
        }
    }
    'base name 2' : {...}
    ...
}
```
For example:
```json
{
  "Data Request Opportunities (Public)": {
    "Comment": {
      "base_id": "appbrFryP1MhstOS3",
      "base_name": "Data Request Opportunities (Public)",
      "id": "tblQqiAzywOppDNvj",
      "name": "Comment",      
      "description": "",
      "fields": {
        "fld5PnZpNhaifVJ8z": {
          "description": "Comment Title",
          "name": "Comment Title",
          "type": "singleLineText"
        },
        "fldKYZsaRAapA58NG": {
          "description": "Variable groups relevant to the comment.",
          "linked_table_id": "tbl4x1RxPwKRZ0VXY",
          "name": "Variable Groups",
          "type": "multipleRecordLinks"
        }, 
    ... 
      "records": {
        "rec5E9oBVZsxdxHKN": {
          "Comment": "The reference to Omon.sltbasin (Omon.slftbasin) is wrong and must be changed to Omon.sltbasin.\n",
          "Comment Title": "Update description",
          "Opportunities": [
            "reczXng420cBQ08hg"
          ],
          "Status": "Done",
          "Theme": [
            "Ocean & Sea-Ice"
          ],
          "Variable Groups": [
            "recPohW0nDzLULHye"
          ]
        },
        ...
```

Each base is a separate top-level entry ("base" is Airtable's term for database).
This is necessary to ensure the integrity of links between different tables in each base.
They are self-consistent within a base, but not across different bases.
Links from a record to one or more other records in other tables appear as lists of record id strings.
In the above example, "Opportunities" and "Variable Groups" are both links (in this instance the lists have length = 1).
The field description indicates which table a link points to, which in the above example for "Variable Groups" is the table with the id string given by `linked_table_id`.
(In this instance it's obvious which table is linked to because the field name is the same as the table name, but that's not required and isn't always the case.)
