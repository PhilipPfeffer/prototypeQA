# Prototype Question Answering

This repository contains prototype code for a question answering system. See the diagram for a description of the system.

# How to run this code
- Install python and pip.
- Install virtualenv and activate the environment:
    ```
    pip install virtualenv
    virtualenv prototypeQA
    source prototypeQA/bin/activate
    pip install -r requirements.txt
    ```
- Get an OpenAI API Key from https://platform.openai.com/docs/quickstart/build-your-application and create a file `env.py` with the API Key.
- Run the code: 
```
python3 qa.py
```

# Diagram
![Diagram](PrototypeQA.jpeg)
