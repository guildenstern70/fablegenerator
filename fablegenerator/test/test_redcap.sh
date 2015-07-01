#!/usr/bin/env bash

cd ..
python fablegenerator.py configs/redcap_en/redcap_pdf_en.config
python fablegenerator.py configs/redcap_en/redcap_epub_en.config
python fablegenerator.py configs/redcap_it/redcap_pdf_it.config
python fablegenerator.py configs/redcap_it/redcap_epub_it.config
python fablegenerator.py configs/redcap_ro/redcap_pdf_ro.config
python fablegenerator.py configs/redcap_ro/redcap_epub_ro.config

