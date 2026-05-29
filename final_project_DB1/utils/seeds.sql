-- ═══════════════════════════════════════════════════════════════
-- MUNDIAL DE FÚTBOL 2026 — Datos de prueba
-- Ejecutar DESPUÉS de db_setup.sql
-- Incluye: equipos, directores técnicos, jugadores y partidos
-- ═══════════════════════════════════════════════════════════════


-- ═══════════════════════════════════════════
-- 1. EQUIPOS (sin id_dt por ahora; se actualiza
--    después de insertar jugadores)
-- ═══════════════════════════════════════════
-- UEFA (id_confederacion = 1)
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('España',      1, 900000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Francia',     1, 950000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Alemania',    1, 750000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Portugal',    1, 800000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Inglaterra',  1, 1100000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Italia',      1, 680000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Países Bajos',1, 600000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Croacia',     1, 380000000);

-- CONMEBOL (id_confederacion = 2)
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Brasil',      2, 1050000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Argentina',   2, 980000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Uruguay',     2, 320000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Colombia',    2, 410000000);

-- CONCACAF (id_confederacion = 3)
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('México',      3, 290000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('USA',         3, 450000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Canadá',      3, 230000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Costa Rica',  3, 90000000);

-- CAF (id_confederacion = 4)
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Marruecos',   4, 310000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Senegal',     4, 270000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Nigeria',     4, 250000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Camerún',     4, 180000000);

-- AFC (id_confederacion = 5)
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Japón',       5, 280000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Corea del Sur',5, 240000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Arabia Saudita',5,150000000);
INSERT INTO equipos (nombre, id_confederacion, valor_mercado) VALUES ('Australia',   5, 130000000);


-- ═══════════════════════════════════════════
-- 2. JUGADORES
--    Formato: nombre, edad, peso(kg), estatura(m), valor(€), id_equipo
--    id_equipo sigue el orden de inserción de equipos arriba
-- ═══════════════════════════════════════════

-- España (equipo 1)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Pedri González',    21, 60, 1.74, 120000000, 1);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Gavi Páez',         19, 60, 1.73, 130000000, 1);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Lamine Yamal',      17, 60, 1.81, 200000000, 1);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Álvaro Morata',     31, 78, 1.87,  45000000, 1);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Rodri Hernández',   28, 82, 1.91,  90000000, 1);

-- Francia (equipo 2)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Kylian Mbappé',     26, 73, 1.78, 180000000, 2);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Antoine Griezmann', 33, 73, 1.76,  40000000, 2);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Ousmane Dembélé',   27, 67, 1.78,  70000000, 2);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Aurélien Tchouaméni',24,78, 1.88,  80000000, 2);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Mike Maignan',       29, 84, 1.91,  45000000, 2);

-- Alemania (equipo 3)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Jamal Musiala',     21, 70, 1.80, 150000000, 3);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Florian Wirtz',     22, 68, 1.76, 130000000, 3);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Leroy Sané',        28, 75, 1.83,  55000000, 3);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Thomas Müller',     35, 76, 1.87,  10000000, 3);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Kai Havertz',       25, 79, 1.89,  65000000, 3);

-- Portugal (equipo 4)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Cristiano Ronaldo', 40, 83, 1.87,   5000000, 4);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Bernardo Silva',    30, 64, 1.73,  90000000, 4);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Rafael Leão',       25, 75, 1.88, 100000000, 4);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Rúben Dias',        27, 76, 1.87,  80000000, 4);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('João Neves',        20, 68, 1.79,  80000000, 4);

-- Inglaterra (equipo 5)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Jude Bellingham',   21, 75, 1.86, 180000000, 5);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Harry Kane',        31, 86, 1.88,  60000000, 5);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Phil Foden',        24, 70, 1.71, 150000000, 5);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Declan Rice',       26, 80, 1.85,  90000000, 5);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Bukayo Saka',       23, 72, 1.78, 150000000, 5);

-- Brasil (equipo 9)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Vinícius Jr.',      24, 73, 1.76, 200000000, 9);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Rodrygo Goes',      23, 67, 1.74, 100000000, 9);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Endrick Felipe',    18, 74, 1.73, 120000000, 9);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Raphinha',          28, 72, 1.76,  80000000, 9);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Marquinhos',        30, 75, 1.83,  35000000, 9);

-- Argentina (equipo 10)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Lionel Messi',      37, 72, 1.70,   8000000,10);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Julián Álvarez',    24, 70, 1.70, 100000000,10);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Alexis Mac Allister',25,72, 1.74,  80000000,10);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Enzo Fernández',    23, 75, 1.78,  80000000,10);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Lautaro Martínez',  26, 73, 1.74,  90000000,10);

-- México (equipo 13)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Santiago Giménez',  23, 77, 1.83,  50000000,13);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Edson Álvarez',     27, 80, 1.86,  40000000,13);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Hirving Lozano',    29, 70, 1.69,  22000000,13);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Guillermo Ochoa',   39, 82, 1.82,   3000000,13);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Charly Rodríguez',  20, 68, 1.77,  12000000,13);

-- USA (equipo 14)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Christian Pulisic', 26, 70, 1.77,  50000000,14);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Tyler Adams',       26, 75, 1.75,  30000000,14);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Folarin Balogun',   23, 75, 1.80,  35000000,14);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Gio Reyna',         22, 68, 1.81,  28000000,14);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Matt Turner',       30, 86, 1.93,  10000000,14);

-- Marruecos (equipo 17)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Achraf Hakimi',     25, 73, 1.81,  70000000,17);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Hakim Ziyech',      31, 70, 1.81,  15000000,17);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Sofyan Amrabat',    27, 75, 1.82,  30000000,17);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Youssef En-Nesyri', 27, 75, 1.89,  30000000,17);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Bono Yassine',      33, 84, 1.94,  12000000,17);

-- Japón (equipo 21)
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Takefusa Kubo',     23, 67, 1.73,  50000000,21);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Daichi Kamada',     28, 75, 1.82,  22000000,21);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Wataru Endo',       31, 75, 1.78,  12000000,21);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Ritsu Doan',        26, 72, 1.73,  22000000,21);
INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo) VALUES ('Ko Itakura',        27, 78, 1.87,  18000000,21);


-- ═══════════════════════════════════════════
-- 3. DIRECTORES TÉCNICOS
--    Asignamos un jugador ficticio como DT por equipo
--    (en un proyecto real habría una tabla propia para DTs)
--    Usamos los primeros jugadores insertados por equipo.
-- ═══════════════════════════════════════════

-- Necesitamos los IDs de jugadores; como el trigger empieza en 1:
-- España: jugador 1 = Pedri (DT ficticio)
UPDATE equipos SET id_dt = 1  WHERE nombre = 'España';
UPDATE equipos SET id_dt = 6  WHERE nombre = 'Francia';
UPDATE equipos SET id_dt = 11 WHERE nombre = 'Alemania';
UPDATE equipos SET id_dt = 16 WHERE nombre = 'Portugal';
UPDATE equipos SET id_dt = 21 WHERE nombre = 'Inglaterra';
UPDATE equipos SET id_dt = 26 WHERE nombre = 'Brasil';
UPDATE equipos SET id_dt = 31 WHERE nombre = 'Argentina';
UPDATE equipos SET id_dt = 36 WHERE nombre = 'México';
UPDATE equipos SET id_dt = 41 WHERE nombre = 'USA';
UPDATE equipos SET id_dt = 46 WHERE nombre = 'Marruecos';
UPDATE equipos SET id_dt = 51 WHERE nombre = 'Japón';


-- ═══════════════════════════════════════════
-- 4. PARTIDOS DE EJEMPLO (fase de grupos)
--    Estadio Azteca (1), MetLife (4), SoFi (5),
--    AT&T (6), BMO Field (15), BC Place (16)
-- ═══════════════════════════════════════════

-- Grupo A — Ciudad de México (Azteca)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (13, 17, 1, 1, TIMESTAMP '2026-06-11 20:00:00');   -- México vs Marruecos

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (21, 24, 1, 1, TIMESTAMP '2026-06-11 17:00:00');   -- Japón vs Australia

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (13, 21, 1, 1, TIMESTAMP '2026-06-15 20:00:00');   -- México vs Japón

-- Grupo B — New York (MetLife)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (5, 10, 4, 2, TIMESTAMP '2026-06-12 19:00:00');    -- Inglaterra vs Argentina

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (9, 20, 4, 2, TIMESTAMP '2026-06-12 16:00:00');    -- Brasil vs Camerún

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (5, 9, 4, 2, TIMESTAMP '2026-06-16 20:00:00');     -- Inglaterra vs Brasil

-- Grupo C — Los Angeles (SoFi)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (1, 2, 5, 3, TIMESTAMP '2026-06-13 22:00:00');     -- España vs Francia

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (3, 7, 5, 3, TIMESTAMP '2026-06-13 19:00:00');     -- Alemania vs Países Bajos

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (1, 3, 5, 3, TIMESTAMP '2026-06-17 22:00:00');     -- España vs Alemania

-- Grupo D — Dallas (AT&T)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (14, 15, 6, 4, TIMESTAMP '2026-06-14 21:00:00');   -- USA vs Canadá

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (4, 11, 6, 4, TIMESTAMP '2026-06-14 18:00:00');    -- Portugal vs Uruguay

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (14, 4, 6, 4, TIMESTAMP '2026-06-18 21:00:00');    -- USA vs Portugal

-- Grupo E — Toronto (BMO Field)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (15, 18, 15, 5, TIMESTAMP '2026-06-15 19:00:00');  -- Canadá vs Senegal

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (12, 16, 15, 5, TIMESTAMP '2026-06-15 16:00:00');  -- Colombia vs Costa Rica

-- Grupo F — Vancouver (BC Place)
INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (22, 19, 16, 6, TIMESTAMP '2026-06-16 18:00:00');  -- Corea del Sur vs Nigeria

INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
VALUES (6, 8, 16, 6, TIMESTAMP '2026-06-16 21:00:00');    -- Italia vs Croacia


-- ═══════════════════════════════════════════
-- 5. USUARIOS ADICIONALES DE PRUEBA
--    Contraseñas (SHA-256):
--    "Pass1234" = d8b5dc5e7f8b1e0e4c4a4a8a5c1a1b1d...
--    Generar con Python:
--      import hashlib
--      hashlib.sha256("Pass1234".encode()).hexdigest()
-- ═══════════════════════════════════════════

INSERT INTO usuarios (username, password, rol)
VALUES (
    'editor1',
    'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1',
    'Tradicional'
);

INSERT INTO usuarios (username, password, rol)
VALUES (
    'invitado1',
    'd74ff0ee8da3b9806b18c877dbf29bbde50b5bd8e4dad7a3a725000feb82e8f1',
    'Esporadico'
);

COMMIT;


-- ═══════════════════════════════════════════
-- 6. VERIFICACIÓN FINAL
-- ═══════════════════════════════════════════

SELECT 'confederaciones' AS tabla, COUNT(*) AS registros FROM confederaciones UNION ALL
SELECT 'ciudades',                 COUNT(*)               FROM ciudades        UNION ALL
SELECT 'estadios',                 COUNT(*)               FROM estadios        UNION ALL
SELECT 'grupos',                   COUNT(*)               FROM grupos          UNION ALL
SELECT 'equipos',                  COUNT(*)               FROM equipos         UNION ALL
SELECT 'jugadores',                COUNT(*)               FROM jugadores       UNION ALL
SELECT 'partidos',                 COUNT(*)               FROM partidos        UNION ALL
SELECT 'usuarios',                 COUNT(*)               FROM usuarios        UNION ALL
SELECT 'bitacora',                 COUNT(*)               FROM bitacora;