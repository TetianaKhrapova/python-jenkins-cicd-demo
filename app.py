from flask import Flask
app = Flask(_name)

@app.route("/")
def hello ():
  return "Hello from Jenkins CI/CD!"
