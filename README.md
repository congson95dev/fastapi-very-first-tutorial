This is a FastAPI very first example of tutorial followed by this tutorial:<br>
Also, we are stayed in here: https://fastapi.tiangolo.com/tutorial/debugging/

To install, use: <br>
`sudo pip3 install virtualenv` <br>
`python3 -m venv venv` <br>
`source venv/bin/activate` <br>
`pip install "fastapi[all]"`

To run the app: <br>
`uvicorn main:app --reload`

After you run this command, go to http://127.0.0.1:8000/docs to see the result <br>
In this command `uvicorn main:app --reload`, it run the `main.py`

Or could run by `uvicorn sql_app.main:app --reload`, it will go to `sql_app` folder, then run `main.py`
<br>
(This is a CRUD using sqlite db, but in very first look)

This tutorial is not fully present to us about the CRUD, so we need to learn from some other tutorials

There're serveral of tutorial that we can learn from, such as: <br>
https://testdriven.io/blog/fastapi-beanie/ <br>
https://testdriven.io/blog/fastapi-mongo/

I've create a fully complete CRUD module: <br>
https://github.com/saxsax1995/fast-api-postgres-crud-api

Also, for authenticate example, run `uvicorn auth:app --reload` or `uvicorn auth-jwt:app --reload`