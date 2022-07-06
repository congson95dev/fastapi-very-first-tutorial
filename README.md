This is a FastAPI very first example of tutorial followed by this tutorial:
Also, we are stayed in here: https://fastapi.tiangolo.com/tutorial/debugging/

To install, use:
`sudo pip3 install virtualenv
python3 -m venv venv
source venv/bin/activate
pip install "fastapi[all]"`

To run the app:
`uvicorn main:app --reload`

After you run this command, go to http://127.0.0.1:8000/docs to see the result
In this command `uvicorn main:app --reload`, it run the main.py

This tutorial is not fully present to us about the CRUD, so we need to learn from some other tutorials

There're serveral of tutorial that we can learn from, such as:
https://testdriven.io/blog/fastapi-beanie/
https://testdriven.io/blog/moving-from-flask-to-fastapi/
https://testdriven.io/blog/fastapi-mongo/