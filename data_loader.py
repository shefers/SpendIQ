import pandas as pd

<<<<<<< HEAD
def load_data(file):
    if file.name.endswith(".csv"):
        df = pd.read_csv(file)
    elif file.name.endswith(".xlsx"):
        df = pd.read_excel(file)
    else:
        raise ValueError("Unsupported file type")

=======

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
>>>>>>> 46cf5dcb5f007443edae98e3d1139a16ef4a4a20
    return df