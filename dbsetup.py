import sqlite3
if __name__ == "__main__":
    db = sqlite3.connect("data.db")
    db.execute("CREATE TABLE GeneralInt (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, key TEXT NOT NULL, value INTEGER);")
    db.execute("INSERT INTO GeneralInt (key, value) VALUES (\"visits\", 0);")
    db.commit()
    db.close()