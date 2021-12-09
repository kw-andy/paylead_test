#!/usr/bin/env python3

import requests
import pandas as pd
import sqlite3

from zipfile import ZipFile


def creating_tables(dbfile):
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS networks")
    cursor.execute("DROP TABLE IF EXISTS town")
    cursor.execute("DROP TABLE IF EXISTS theaters")

    networks = """CREATE TABLE networks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL
    )"""
    cursor.execute(networks)
    print("Table created - ok")

    town = """CREATE TABLE town (
    zipcode TEXT NOT NULL,
    town_name TEXT NOT NULL
    )"""
    cursor.execute(town)
    print("Table created - ok")

    theaters = """CREATE TABLE theaters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    osm_id TEXT UNIQUE NOT NULL,
    rooms INTEGER,
    seats INTEGER,
    com_nom TEXT NOT NULL,
    zipcode TEXT,
    network INTEGER REFERENCES networks (id)
    )"""
    cursor.execute(theaters)
    print("Table created - ok")
    conn.commit()
    conn.close()


def down_and_unzip(url, zipname, finalfile):
    down_file = requests.get(url, allow_redirects=True)
    open(zipname, "wb").write(down_file.content)

    with ZipFile(zipname, "r") as zipObj:
        zipObj.extract(finalfile)


def choose_cols_marque(csv_file):
    df = pd.read_csv(csv_file)
    df_no_nan = df.dropna(subset=["marque"])
    marque_dict = {}
    for idx_marque, marque in enumerate(df_no_nan["marque"].unique()):
        marque_dict[idx_marque] = marque
    return marque_dict


def choose_cols_town(csv_file):
    df = pd.read_csv(csv_file)
    depts_list = df[["com_insee", "com_nom"]].values.tolist()
    return depts_list


def choose_cols_theaters(csv_file, networks):
    df = pd.read_csv(csv_file)
    theater_dict = {}
    for idx_osm, osm_id in enumerate(df["osm_id"]):
        theater_dict[idx_osm] = [osm_id]
    for idx_nbscreens, nbscreeens in enumerate(df["nb_screens"]):
        theater_dict[idx_nbscreens].append(nbscreeens)
    for idx_seats, seats in enumerate(df["capacity"]):
        theater_dict[idx_seats].append(int(seats))
    for idx_town, town_name in enumerate(df["com_nom"]):
        theater_dict[idx_town].append(town_name)
    for idx_marque, marque_name in enumerate(df["marque"]):
        theater_dict[idx_marque].append(marque_name)
    for idx_commu, commu_zip in enumerate(df["com_insee"]):
        theater_dict[idx_commu].append(commu_zip)
    for keys_theaters, vals_theaters in theater_dict.items():
        for keys_networks, vals_networks in networks.items():
            if vals_networks in vals_theaters:
                theater_dict[keys_theaters][vals_theaters.index(vals_networks)] = keys_networks
    return theater_dict


def insert_into_db(choose_cols_marque, choose_cols_town, choose_cols_theaters, dbfile):
    conn = sqlite3.connect(dbfile)
    cursor = conn.cursor()

    for key_marque, marques in choose_cols_marque.items():
        cursor.execute("INSERT INTO networks VALUES (?, ?)", [key_marque, marques])

    for idx_items, depts_items in enumerate(choose_cols_town):
        cursor.execute(
            "INSERT INTO town VALUES (?, ?)",
            [choose_cols_town[idx_items][0], choose_cols_town[idx_items][1]],
        )

    for key_theaters, theaters in choose_cols_theaters.items():
        cursor.execute(
            "INSERT INTO theaters VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                key_theaters,
                theaters[0],
                theaters[1],
                theaters[2],
                theaters[3],
                theaters[4],
                theaters[5],
            ],
        )

    conn.commit()
    conn.close()


def transform_and_load_db(csvfile, dbfile):
    creating_tables(dbfile)

    insert_into_db(
        choose_cols_marque(csvfile),
        choose_cols_town(csvfile),
        choose_cols_theaters(csvfile, choose_cols_marque(csvfile)),
        dbfile,
    )


def show_me_min_max_stats(min_max_input, dbfile):
    con = sqlite3.connect(dbfile)
    cur = con.cursor()

    val_switch = min_max_input

    if val_switch == "min":
        cur.execute(
            "SELECT osm_id,com_nom,MIN(seats) FROM theaters WHERE seats IS NOT NULL GROUP BY seats LIMIT 1"
        )
        print('La salle ayant le moins de sièges est la suivante')
        print(cur.fetchall())
    elif val_switch == "max":
        cur.execute(
            "SELECT osm_id,com_nom,MAX(seats) FROM theaters WHERE seats IS NOT NULL GROUP BY seats ORDER BY seats DESC limit 1"
        )
        print(cur.fetchall())
        print('La salle ayant le plus de sièges est la suivante')
    con.close()

show_me_min_max_stats

if __name__ == "__main__":
    down_and_unzip(  # put arg
        "https://www.data.gouv.fr/fr/datasets/r/1d8c2bc0-d769-433a-b8ab-0f49341d4b8a",
        "movie.zip",
        "data.csv",
    )
    transform_and_load_db("data.csv", "paylead.db")  # put arg
    show_me_min_max_stats(min_max_input, dbfile)


"""
creating_tables("paylead.db")

insert_into_db(
    choose_cols_marque("data.csv"),
    choose_cols_town("data.csv"),
    choose_cols_theaters("data.csv", choose_cols_marque("data.csv")),
    "paylead.db",
)
"""
