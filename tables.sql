create TABLE IF NOT EXISTS "cronologia" (
	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	"operazione"	TEXT NOT NULL,
	"risultato"	TEXT NOT NULL
);

create TABLE IF NOT EXISTS "impostazioni"
(
    "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "setting" TEXT    NOT NULL,
    "value"   TEXT    NOT NULL
);