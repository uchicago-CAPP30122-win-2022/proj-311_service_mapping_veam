echo -e "1. Creating new virtual environment..."

python3 -m venv env 

echo -e "2. Installing Requirements..."

source env/bin/activate
pip3 install -r requirements.txt

deactivate 
echo -e "Install is complete."
