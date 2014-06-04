@ECHO OFF
cd output
del *.epub
del *.pdf
cd ..
echo Fable #0 :  When I met the Pirates 
CALL fablegenerator configs/pirates_epub_en.config
echo Fable #1 :  My voyage in Aragon 
CALL fablegenerator configs/voyage_pdf_it.config
CALL fablegenerator configs/voyage_epub_en.config
echo Fable #2 :  The Talisman of the Badia
CALL fablegenerator configs/badia_epub_en.config
CALL fablegenerator configs/badia_epub_it.config
pause
echo TEST FINISHED



