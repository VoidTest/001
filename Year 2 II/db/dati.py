import sqlite3


conn = sqlite3.connect("dati.db", check_same_thread=False)

def skolenu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE skoleni(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL
        )
        """
    )
    conn.commit()


def skolotaju_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE skolotaji(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vards TEXT NOT NULL,
        uzvards TEXT NOT NULL
        )
        """
    )
    conn.commit()

def prieksmetu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE prieksmeti(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nosaukums TEXT NOT NULL
        )
        """
    )
    conn.commit()

def atzimju_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE atzimes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        atzime INTEGER NOT NULL,
        skolena_id INTEGER NOT NULL,
        prieksmeta_id INTEGER NOT NULL,
    	FOREIGN KEY (skolena_id) REFERENCES skoleni(id),
        FOREIGN KEY (prieksmeta_id) REFERENCES prieksmeti(id)
        )
        """
    )
    conn.commit()

def sk_prieksmetu_tabulas_izveide():
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE sk_prieksmeti(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        skolotaja_id INTEGER NOT NULL,
        prieksmeta_id INTEGER NOT NULL,
    	FOREIGN KEY (skolotaja_id) REFERENCES skolotaji(id),
        FOREIGN KEY (prieksmeta_id) REFERENCES prieksmeti(id)
        )
        """
    )
    conn.commit()
#sk_prieksmetu_tabulas_izveide()
#skolotaju_tabulas_izveide()

#skolenu_tabulas_izveide()

#prieksmetu_tabulas_izveide()

#atzimju_tabulas_izveide()
def pievienot_skolenu(vards, uzvards):
    print(vards, uzvards)
    cur = conn.cursor()
    cur.execute(
        f"""
        INSERT INTO skoleni(vards, uzvards) VALUES("{vards}","{uzvards}")
        """
    )
    conn.commit()


def pievienot_skolotaju(vards, uzvards):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO skolotaji(vards, uzvards) VALUES("{vards}","{uzvards}")
    """
    )

    print(vards, uzvards)

def pievienot_prieksmetu(prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO prieksmeti(nosaukums) VALUES("{prieksmets}")
    """
    )
    conn.commit()

def pievienot_atzimi(atzime, skolens, prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO atzimes(atzime, skolena_id, prieksmeta_id) VALUES("{atzime}","{skolens}","{prieksmets}")
    """
    )
    print("eouhqwufhwe")
    conn.commit()

def pievienot_sk_prieksmetu(skolotajs, prieksmets):
    cur = conn.cursor()
    cur.execute(
    f"""
    INSERT INTO sk_prieksmeti(skolotaja_id, prieksmeta_id) VALUES("{skolotajs}","{prieksmets}")
    """
    )
    print("eouhqwufhwe")
    conn.commit()




def iegut_skolenus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, id FROM skoleni"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati


def iegut_skolotajus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, id FROM skolotaji"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_prieksmetus():
    cur = conn.cursor()
    cur.execute(
        """SELECT nosaukums, id FROM prieksmeti"""
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_atzimes():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, nosaukums, atzime FROM
        (atzimes JOIN skoleni ON skoleni.id = atzimes.skolena_id)
        JOIN prieksmeti ON prieksmeti.id = atzimes.prieksmeta_id
        """
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_sk_prieksmetus():
    cur = conn.cursor()
    cur.execute(
        """SELECT vards, uzvards, nosaukums FROM
        (sk_prieksmeti JOIN skolotaji ON skolotaji.id = sk_prieksmeti.skolotaja_id)
        JOIN prieksmeti ON prieksmeti.id = sk_prieksmeti.prieksmeta_id
        """
    )
    conn.commit()
    dati = cur.fetchall()
    return dati

def iegut_videjas_atzimes():
    dati = []
    return dati



