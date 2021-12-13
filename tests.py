import requests
import pandas as pd
import sqlite3
import pytest

from zipfile import ZipFile

from cinema_facts import choose_cols_marque

#Note: To run, do `pytest tests.py`

def test_choose_cols_marque():
    mock_marque_dict = {
        0: "CGR cinémas",
        1: "Ville de Choisy-le-Roi",
        2: "Pathé Gaumont",
        3: "UGC",
        4: "Cinéode",
        5: "Magestic",
        6: "Cinéville",
    }
    assert choose_cols_marque("mock_data.csv") == mock_marque_dict
