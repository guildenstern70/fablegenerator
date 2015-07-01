#!/usr/bin/env bash

cd ..
python fablegenerator.py configs/jackbeanstalk_en/jackbeanstalk_pdf_en.config
python fablegenerator.py configs/jackbeanstalk_en/jackbeanstalk_epub_en.config
python fablegenerator.py configs/jackbeanstalk_it/jackbeanstalk_pdf_it.config
python fablegenerator.py configs/jackbeanstalk_it/jackbeanstalk_epub_it.config
python fablegenerator.py configs/jackbeanstalk_ro/jackbeanstalk_pdf_ro.config
python fablegenerator.py configs/jackbeanstalk_ro/jackbeanstalk_epub_ro.config

