@ECHO OFF
cd ../output
del *.epub
del *.pdf
cd ../test
CALL test_badia_en.bat
CALL test_badia_it.bat
CALL test_badia_ro.bat
CALL test_pirates_en.bat
CALL test_pirates_it.bat
CALL test_pirates_ro.bat
CALL test_voyage_en.bat
CALL test_voyage_it.bat
CALL test_voyage_ro.bat




