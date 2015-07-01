@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (RO - EPUB)
CALL fablegenerator configs/voyage_ro/voyage_epub_ro.config
echo Fable #1 :  When I met the Pirates (RO - PDF)
CALL fablegenerator configs/voyage_ro/voyage_pdf_ro.config
cd test
pause
echo TEST FINISHED



