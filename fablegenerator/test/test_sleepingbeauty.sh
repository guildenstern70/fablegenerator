#!/usr/bin/env bash

cd ..
python fablegenerator.py configs/sleepingbeauty_en/sleepingbeauty_pdf_en.config
python fablegenerator.py configs/sleepingbeauty_en/sleepingbeauty_epub_en.config
python fablegenerator.py configs/sleepingbeauty_it/sleepingbeauty_pdf_it.config
python fablegenerator.py configs/sleepingbeauty_it/sleepingbeauty_epub_it.config
python fablegenerator.py configs/sleepingbeauty_ro/sleepingbeauty_pdf_ro.config
python fablegenerator.py configs/sleepingbeauty_ro/sleepingbeauty_epub_ro.config

