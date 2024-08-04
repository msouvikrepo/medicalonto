# Extract Bio Medical Entities from Clinical Trials

## Overview

This is a simple script to extract bio medical entities from clinical trial documents fetched from an Apache Solr server using [BERN](https://github.com/dmis-lab/bern), a BERT based biomedical NER extractor

## Pre-requisites not included in this repository

- Apache Solr Server (external) for more information on how to set up a Solr server please refer to the [Solr documentation](https://lucene.apache.org/solr/guide/8_8/solr-tutorial.html)
- BERN Server (external) in my case I self-hosted a BERN server in an EC2 instance, please refer to the [BERN installation guide](https://github.com/dmis-lab/bern?tab=readme-ov-file#installation)

## Running the script

Create a virtual environment

    virtualenv .venv

Install the required packages
    
    pip install -r requirements.txt

Test BERN server

    python test_BERN.py

Run the script

    python extract_bioMed_entities.py

## Output

The script will output the extracted bio medical entities in a JSON file with the study ID as the filename. Check the `output_files` directory for sample output files.