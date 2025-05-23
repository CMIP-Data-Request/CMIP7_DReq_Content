## CMIP7 Data Request Content

This repository version controls the information used in the data request, which is referred to as the data request "content".
It is versioned separately from the data request software, which provides an interface to query and utilize the content. 

**The content (json) files in this repository function as input to the software and are not intended to be accessed directly by users.**
The intention is that the content files are accessed "under the hood" when using the software, invisible to the user.
Further guidance is provided in the [software repository](https://github.com/CMIP-Data-Request/CMIP7_DReq_Software).

Airtable databases ("bases") maintained by the CMIP IPO and Data Request Task Team are the primary source of the content (i.e., the "source of truth").
These Airtable bases are used to manage the information gathered by the extensive community consultation undertaken to develop the CMIP7 data request.
This github repository stores exports of the content from Airtable as `json` files, and basic explanation of their format can be [found here](https://github.com/CMIP-Data-Request/CMIP7_DReq_Content/blob/main/scripts/README_airtable_export.md#structure-of-the-exported-content).
It also stores scripts used to export the content and do basic checks on its validity.

There are two types of export file:

- `dreq_release_export.json` contains the content of an official data request release. New versions of this file correspond official data request releases (e.g., `v1.2.1`) and are tagged with the version identifier in this repository. **This is the export file that is relevant to users, but (as noted above) they do not need to access it directly.** By default a tagged version of this file is automatically accessed when using the [software](https://github.com/CMIP-Data-Request/CMIP7_DReq_Software). 

- `dreq_raw_export.json` contains the content of the "working" bases used by the Data Request Task Team, CMIP IPO, and Thematic Author Teams to develop the data request. **This export file is intended for use by developers; users of the data request should not need to access it.** It may be updated on an ongoing basis (i.e., between official data request releases). Its format differs slightly from that of `dreq_release_export.json`, but for tagged versions its information content should be consistent with `dreq_release_export.json`.

