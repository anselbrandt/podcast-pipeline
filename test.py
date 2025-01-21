import sqlite3

episode = "567"
conn = sqlite3.connect("transcripts.db")
c = conn.cursor()

c.execute("""SELECT * FROM lines WHERE episode = ?""", (episode,))

results = c.fetchall()

conn.commit()
conn.close()


print(len(results))
