@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (IT - EPUB)
CALL fablegenerator configs/pirates_it/pirates_epub_it.config
echo Fable #1 :  When I met the Pirates (IT - PDF)
CALL fablegenerator configs/pirates_it/pirates_pdf_it.config
cd test
pause
echo TEST FINISHED



