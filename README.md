## CMIP7 Data Request Content

This repository version controls the information used in the data request, which is referred to as the data request "content".
It is versioned separately from the data request software, which provides an interface to query and utilize the content. 
The files in this repository function as input to the software; they are not intended to be accessed directly by users.
For further explanation, please see the guidance provided in the [software repository](https://github.com/CMIP-Data-Request/CMIP7_DReq_Software).


Airtable databases ("bases") maintained by the CMIP IPO and Data Request Task Team are the primary source of the content.
These Airtable bases are used to manage the information gathered by the extensive community consultation undertaken to develop the CMIP7 data request.
This github repository stores exports of the content from Airtable as `json` files, as well as scripts used to export the content and do basic checks on its validity.
There are two types of export file:

- `dreq_release_export.json` contains the content of an official data request release. New versions of this file correspond to tags in this repository with the names of official releases (e.g. `v1.0beta`).

- `dreq_raw_export.json` contains the content of the "working" bases used by the Data Request Task Team, CMIP IPO, and Thematic Author Teams to develop the data request. It is updated on an ongoing basis (i.e., there can be updates between official releases). Its format differs slightly from that of `dreq_release_export.json`, but for tagged versions its information content should be consistent with `dreq_release_export.json`.
