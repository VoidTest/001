import sqlite3

conn = sqlite3.connect("data.db", check_same_thread=False)

def lietotaju_tabulas_izveide():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS lietotaji (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vards TEXT NOT NULL,
            uzvards TEXT NOT NULL,
            lietotajvards TEXT UNIQUE NOT NULL
        )
    """)
    conn.commit()

def zinu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS zinas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lietotaja_id INTEGER NOT NULL,
            zina TEXT NOT NULL,
            izveidots TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lietotaja_id) REFERENCES lietotaji(id)
        )
    """)
    conn.commit()

# Izveido tabulas
lietotaju_tabulas_izveide()
zinu_tabulas_izveide()

def pievienot_lietotaju(vards, uzvards, lietotajvards):
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO lietotaji (vards, uzvards, lietotajvards) VALUES (?, ?, ?)
        """, (vards, uzvards, lietotajvards))
        conn.commit()
    except sqlite3.IntegrityError:
        return "Šāds lietotājvārds jau eksistē."
    return "Lietotājs pievienots veiksmīgi."

def iegut_lietotajus():
    cur = conn.cursor()
    cur.execute("SELECT id, vards, uzvards, lietotajvards FROM lietotaji ORDER BY lietotajvards ASC")
    return cur.fetchall()

def pievienot_zinu(lietotaja_id, zina):
    cur = conn.cursor()
    if not zina.strip():
        return "Ziņa nevar būt tukša."
    cur.execute("""
        INSERT INTO zinas (lietotaja_id, zina) VALUES (?, ?)
    """, (lietotaja_id, zina))
    conn.commit()
    return "Ziņa pievienota veiksmīgi."

def iegut_zinas():
    cur = conn.cursor()
    cur.execute("""
        SELECT lietotaji.vards, lietotaji.uzvards, zinas.zina, zinas.izveidots
        FROM zinas
        JOIN lietotaji ON lietotaji.id = zinas.lietotaja_id
        ORDER BY zinas.izveidots DESC
    """)
    return cur.fetchall()

def iegut_statistiku():
    cur = conn.cursor()
    cur.execute("""
        SELECT lietotaji.vards, lietotaji.uzvards, COUNT(zinas.id) AS zinu_skaits
        FROM lietotaji
        LEFT JOIN zinas ON lietotaji.id = zinas.lietotaja_id
        GROUP BY lietotaji.id
        ORDER BY zinu_skaits DESC
    """)
    return cur.fetchall()
