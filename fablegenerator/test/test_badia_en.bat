@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (EN - EPUB)
CALL fablegenerator configs/badia_en/badia_epub_en.config
echo Fable #1 :  When I met the Pirates (EN - PDF)
CALL fablegenerator configs/badia_en/badia_pdf_en.config
pause
cd test
echo TEST FINISHED



