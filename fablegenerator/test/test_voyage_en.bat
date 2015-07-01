@ECHO OFF
cd ..
echo Fable #0 :  When I met the Pirates (EN - EPUB)
CALL fablegenerator configs/voyage_en/voyage_epub_en.config
echo Fable #1 :  When I met the Pirates (EN - PDF)
CALL fablegenerator configs/voyage_en/voyage_pdf_en.config
cd test
pause
echo TEST FINISHED



