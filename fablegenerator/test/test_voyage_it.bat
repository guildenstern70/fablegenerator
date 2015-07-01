@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (IT - EPUB)
CALL fablegenerator configs/voyage_it/voyage_epub_it.config
echo Fable #1 :  When I met the Pirates (IT - PDF)
CALL fablegenerator configs/voyage_it/voyage_pdf_it.config
cd test
pause
echo TEST FINISHED



