#!/usr/bin/env bash

cd ..
python fablegenerator.py configs/tomthumb_en/tomthumb_pdf_en.config
python fablegenerator.py configs/tomthumb_en/tomthumb_epub_en.config
python fablegenerator.py configs/tomthumb_it/tomthumb_pdf_it.config
python fablegenerator.py configs/tomthumb_it/tomthumb_epub_it.config
python fablegenerator.py configs/tomthumb_ro/tomthumb_pdf_ro.config
python fablegenerator.py configs/tomthumb_ro/tomthumb_epub_ro.config

