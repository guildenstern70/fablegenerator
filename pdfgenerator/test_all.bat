@ECHO OFF
echo Fable #0 :  When I met the Pirates (EN - EPUB)
CALL pdfgenerator configs/pirates_epub_en.config
echo Fable #1 :  My voyage in Aragon (IT - PDF)
CALL pdfgenerator configs/voyage_pdf_it.config
pause
echo TEST FINISHED



