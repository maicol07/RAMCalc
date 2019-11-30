create TABLE IF NOT EXISTS "impostazioni"
(
    "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "setting" TEXT    NOT NULL,
    "value"   TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS "cronologia"
(
    "id"      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    "expression" TEXT    NOT NULL,
    "result"   TEXT    NOT NULL
)