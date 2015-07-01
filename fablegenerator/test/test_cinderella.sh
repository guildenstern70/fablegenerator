#!/usr/bin/env bash

cd ..
python fablegenerator.py configs/cinderella_en/cinderella_pdf_en.config
python fablegenerator.py configs/cinderella_en/cinderella_epub_en.config
python fablegenerator.py configs/cinderella_it/cinderella_pdf_it.config
python fablegenerator.py configs/cinderella_it/cinderella_epub_it.config
python fablegenerator.py configs/cinderella_ro/cinderella_pdf_ro.config
python fablegenerator.py configs/cinderella_ro/cinderella_epub_ro.config


