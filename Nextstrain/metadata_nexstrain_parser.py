#!/usr/bin/env python

import os
import sys
import argparse
import json


def parse_args(args=None):
    description = (
        "Convert fetch sample info from iskylims wetlab api to nextstrain metadata tsv."
    )
    epilog = (
        """Example usage: python metadata_nexstrain_parser.py <file_in> <file_out>"""
    )

    parser = argparse.ArgumentParser(description=description, epilog=epilog)
    parser.add_argument("file_in", help="Input json file from iskylims api request.")
    parser.add_argument("file_out", help="Output tsv file for nexstrain input.")
    return parser.parse_args(args)


def main(args=None):
    # Process args
    args = parse_args(args)

    # Opening JSON file
    f = open(args.file_in)

    # returns JSON object as a dictionary
    data = json.load(f)
    header = "strain\tvirus\tdate\taccession\tregion\tcountry\tdivision\tcity\tlab\tspecimen_source\thost_age\thost_gender\thost_sciencitic_name\tsequencing_platform\tsequencing_instrument_model\tenrichment_panel_version\tdiagnostic_pcr_Ct_value_1\tPANGO Lineage"
    count_err_dict={}
    with open(args.file_out, "w", encoding="utf8") as fout:
        fout.write(header + "\n")
        for record in data:
            try:
                trial = record["lineage_name"]
            except KeyError as e:
                record["lineage_name"] = "Unassigned"
            try:
                fout.write(
                    record["sequencing_sample_id"]
                    + "\t"
                    + record["organism"]
                    + "\t"
                    + record["sample_collection_date"]
                    + "\t"
                    + ""
                    + "\t"
                    + "Europe"
                    + "\t"
                    + record["geo_loc_country"]
                    + "\t"
                    + record["geo_loc_region"]
                    + "\t"
                    + record["geo_loc_city"]
                    + "\t"
                    + record["collecting_institution"]
                    + "\t"
                    + record["specimen_source"]
                    + "\t"
                    + record["host_age"]
                    + "\t"
                    + record["host_gender"]
                    + "\t"
                    + record["host_scientific_name"]
                    + "\t"
                    + record["sequencing_instrument_platform"]
                    + "\t"
                    + record["sequencing_instrument_model"]
                    + "\t"
                    + record["enrichment_panel_version"]
                    + "\t"
                    + record["diagnostic_pcr_Ct_value_1"]
                    + "\t"
                    + record["lineage_name"]
                    + "\n"
                )
            except KeyError as e:
                key = str(e).split("'")[1]
                if key not in count_err_dict:
                    count_err_dict[key] = 1
                else:
                    count_err_dict[key] += 1
                continue

    fout.close()
    if len(count_err_dict)>=1:
        print(f"Aborted, found errors: {count_err_dict}")
        sys.exit(1)
    
    with open("lat_longs.tsv", "w", encoding="utf8") as fout:
        for record in data:
            fout.write(
                "division"
                + "\t"
                + record["geo_loc_region"]
                + "\t"
                + record["geo_loc_latitude"]
                + "\t"
                + record["geo_loc_longitude"]
                + "\n"
            )
        fout.close()

if __name__ == "__main__":
    sys.exit(main())
