@echo off


:start
cls
python ./bat-gen.py

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install pandas
pip install matplotlib
pip install DateTime
pip install fpdf

pause
exit