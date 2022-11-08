# Turbo

<h3>:construction: Work enviroment:</h3>
<li>Install <b>Python 3.9</b></li> 
<li>Create enviroment: <b>py -m venv env</b></li> 
<li>Activate on WINDOWS: <b>env\Scripts\activate</b></li>
<li>Activate on MAC: <b>source env/bin/activate</b></li>
<h3>:books: Dependencies</h3>
<li><b>pip3 install -r requirements.txt</b></li>
<h3>:mag_right: Testing</h3>
<li>pytest -W ignore::DeprecationWarning</b></li>
<h3>:rocket: Launch inventory:</h3>
<li><b>uvicorn main:app --reload</b></li>
<li><b>py consumer.py</b></li>
<h3>:rocket: Launch payment:</h3>
<li><b>uvicorn main:app --reload --port 8001</b></li>
<li><b>py consumer.py</b></li>
