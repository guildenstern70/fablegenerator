@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (EN - EPUB)
CALL fablegenerator configs/pirates_en/pirates_epub_en.config
echo Fable #1 :  When I met the Pirates (EN - PDF)
CALL fablegenerator configs/pirates_en/pirates_pdf_en.config
cd test
pause
echo TEST FINISHED



