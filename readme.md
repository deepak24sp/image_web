
move ur chunk file to project folder

create a file called  .env and insert 

FILE_NAME = "chunk_9 1.xlsx"

replace the file name with ur filename

--run this commands in cmd 
python -m venv venv 
venv/scripts/activate 
pip install -r requirements.txt

--run the project
python app.py

**************waring***********
if the row number in excel is 2 to 4 then u have enter 0 to 2 in start to end range
and if u skip any of the image use "Process rows with empty REASON" to fill the skipped images 