# EnigmaBackEnd



## Install OLlama before this
```bash
    ollama create choose-a-model-name -f <location of the file e.g. ./Modelfile>
```

## How to Use

1. Create a `.env` file in the root directory of the project.
2. Add the following lines to the `.env` file:
    ```plaintext
    SUMMARY_ENDPOINT_URL=""
    SUMMARY_ENDPOINT_KEY=""
    Modelname=""


# Create a virtual environment

```bash
pip install -r requirements.txt
```

# Run below command to launch the server
```bash
uvicorn main:app
```