-- ═══════════════════════════════════════════════════════════════
-- MUNDIAL DE FÚTBOL 2026 — Script de creación de base de datos
-- SGBD : Oracle (compatible con XE 21c / 19c)
-- Autor: generado para el proyecto mundial_app
-- ═══════════════════════════════════════════════════════════════
-- Ejecutar como el usuario propietario del esquema (mundial_user)
-- o con privilegios DBA para crear el usuario primero.
-- ═══════════════════════════════════════════════════════════════

-- ───────────────────────────────────────────
-- 1. LIMPIEZA (orden inverso a FK)
--    Útil para re-ejecutar el script desde cero.
-- ───────────────────────────────────────────
BEGIN
    FOR t IN (
        SELECT table_name FROM user_tables
        WHERE  table_name IN (
            'BITACORA','USUARIOS','PARTIDOS','JUGADORES',
            'EQUIPOS','ESTADIOS','CIUDADES','GRUPOS','CONFEDERACIONES'
        )
    ) LOOP
        EXECUTE IMMEDIATE 'DROP TABLE ' || t.table_name || ' CASCADE CONSTRAINTS PURGE';
    END LOOP;
END;
/

BEGIN
    FOR s IN (
        SELECT sequence_name FROM user_sequences
        WHERE  sequence_name IN (
            'SEQ_CONFEDERACIONES','SEQ_CIUDADES','SEQ_ESTADIOS',
            'SEQ_GRUPOS','SEQ_EQUIPOS','SEQ_JUGADORES',
            'SEQ_PARTIDOS','SEQ_USUARIOS','SEQ_BITACORA'
        )
    ) LOOP
        EXECUTE IMMEDIATE 'DROP SEQUENCE ' || s.sequence_name;
    END LOOP;
END;
/


-- ═══════════════════════════════════════════
-- 2. SECUENCIAS (autoincremento)
-- ═══════════════════════════════════════════

CREATE SEQUENCE seq_confederaciones START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_ciudades        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_estadios        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_grupos          START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_equipos         START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_jugadores       START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_partidos        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_usuarios        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;
CREATE SEQUENCE seq_bitacora        START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE;


-- ═══════════════════════════════════════════
-- 3. TABLAS
-- ═══════════════════════════════════════════

-- ── 3.1 Confederaciones ──────────────────────────────────────
CREATE TABLE confederaciones (
    id     NUMBER        PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL UNIQUE
);

-- ── 3.2 Ciudades ────────────────────────────────────────────
CREATE TABLE ciudades (
    id     NUMBER        PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    pais   VARCHAR2(50)  NOT NULL,
    CONSTRAINT chk_ciudad_pais
        CHECK (pais IN ('México', 'USA', 'Canadá')),
    CONSTRAINT uq_ciudad_nombre_pais
        UNIQUE (nombre, pais)
);

-- ── 3.3 Estadios ────────────────────────────────────────────
CREATE TABLE estadios (
    id         NUMBER        PRIMARY KEY,
    nombre     VARCHAR2(150) NOT NULL,
    capacidad  NUMBER(7)     NOT NULL,
    id_ciudad  NUMBER        NOT NULL,
    CONSTRAINT fk_estadio_ciudad
        FOREIGN KEY (id_ciudad) REFERENCES ciudades(id),
    CONSTRAINT chk_estadio_capacidad
        CHECK (capacidad > 0)
);

-- ── 3.4 Grupos ──────────────────────────────────────────────
CREATE TABLE grupos (
    id    NUMBER       PRIMARY KEY,
    letra VARCHAR2(10) NOT NULL UNIQUE
);

-- ── 3.5 Equipos ─────────────────────────────────────────────
--   id_dt referencia a jugadores, pero jugadores referencia a equipos.
--   Para romper la dependencia circular, la FK de id_dt se agrega
--   después de crear la tabla jugadores (ver sección 3.6).
CREATE TABLE equipos (
    id                NUMBER         PRIMARY KEY,
    nombre            VARCHAR2(150)  NOT NULL UNIQUE,
    id_confederacion  NUMBER         NOT NULL,
    id_dt             NUMBER,                      -- FK diferida (ver abajo)
    valor_mercado     NUMBER(15, 2)  DEFAULT 0 NOT NULL,
    CONSTRAINT fk_equipo_confederacion
        FOREIGN KEY (id_confederacion) REFERENCES confederaciones(id),
    CONSTRAINT chk_equipo_valor
        CHECK (valor_mercado >= 0)
);

-- ── 3.6 Jugadores ───────────────────────────────────────────
CREATE TABLE jugadores (
    id        NUMBER         PRIMARY KEY,
    nombre    VARCHAR2(150)  NOT NULL,
    edad      NUMBER(3)      NOT NULL,
    peso      NUMBER(5, 2)   NOT NULL,   -- kg
    estatura  NUMBER(4, 2)   NOT NULL,   -- metros
    valor     NUMBER(15, 2)  DEFAULT 0 NOT NULL,
    id_equipo NUMBER         NOT NULL,
    CONSTRAINT fk_jugador_equipo
        FOREIGN KEY (id_equipo) REFERENCES equipos(id),
    CONSTRAINT chk_jugador_edad
        CHECK (edad > 0 AND edad < 60),
    CONSTRAINT chk_jugador_peso
        CHECK (peso > 0),
    CONSTRAINT chk_jugador_estatura
        CHECK (estatura > 0),
    CONSTRAINT chk_jugador_valor
        CHECK (valor >= 0)
);

-- FK diferida: ahora que jugadores existe, enlazamos id_dt
ALTER TABLE equipos
    ADD CONSTRAINT fk_equipo_dt
        FOREIGN KEY (id_dt) REFERENCES jugadores(id);

-- ── 3.7 Partidos ────────────────────────────────────────────
CREATE TABLE partidos (
    id          NUMBER    PRIMARY KEY,
    id_equipo1  NUMBER    NOT NULL,
    id_equipo2  NUMBER    NOT NULL,
    id_estadio  NUMBER    NOT NULL,
    id_grupo    NUMBER    NOT NULL,
    fecha_hora  TIMESTAMP NOT NULL,
    CONSTRAINT fk_partido_equipo1
        FOREIGN KEY (id_equipo1) REFERENCES equipos(id),
    CONSTRAINT fk_partido_equipo2
        FOREIGN KEY (id_equipo2) REFERENCES equipos(id),
    CONSTRAINT fk_partido_estadio
        FOREIGN KEY (id_estadio) REFERENCES estadios(id),
    CONSTRAINT fk_partido_grupo
        FOREIGN KEY (id_grupo) REFERENCES grupos(id),
    CONSTRAINT chk_partido_equipos_distintos
        CHECK (id_equipo1 <> id_equipo2),
    CONSTRAINT uq_partido_equipos_grupo
        UNIQUE (id_equipo1, id_equipo2, id_grupo)
);

-- ── 3.8 Usuarios ────────────────────────────────────────────
CREATE TABLE usuarios (
    id        NUMBER        PRIMARY KEY,
    username  VARCHAR2(80)  NOT NULL UNIQUE,
    password  VARCHAR2(64)  NOT NULL,   -- SHA-256 hex (64 chars)
    rol       VARCHAR2(20)  NOT NULL,
    CONSTRAINT chk_usuario_rol
        CHECK (rol IN ('Admin', 'Tradicional', 'Esporadico'))
);

-- ── 3.9 Bitácora ────────────────────────────────────────────
CREATE TABLE bitacora (
    id             NUMBER    PRIMARY KEY,
    id_usuario     NUMBER    NOT NULL,
    fecha_ingreso  TIMESTAMP NOT NULL,
    fecha_salida   TIMESTAMP,           -- NULL mientras la sesión sigue activa
    CONSTRAINT fk_bitacora_usuario
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
);


-- ═══════════════════════════════════════════
-- 4. TRIGGERS (autoincremento via secuencias)
-- ═══════════════════════════════════════════

CREATE OR REPLACE TRIGGER trg_confederaciones_bi
    BEFORE INSERT ON confederaciones FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_confederaciones.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_ciudades_bi
    BEFORE INSERT ON ciudades FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_ciudades.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_estadios_bi
    BEFORE INSERT ON estadios FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_estadios.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_grupos_bi
    BEFORE INSERT ON grupos FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_grupos.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_equipos_bi
    BEFORE INSERT ON equipos FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_equipos.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_jugadores_bi
    BEFORE INSERT ON jugadores FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_jugadores.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_partidos_bi
    BEFORE INSERT ON partidos FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_partidos.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_usuarios_bi
    BEFORE INSERT ON usuarios FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_usuarios.NEXTVAL;
    END IF;
END;
/

CREATE OR REPLACE TRIGGER trg_bitacora_bi
    BEFORE INSERT ON bitacora FOR EACH ROW
BEGIN
    IF :NEW.id IS NULL THEN
        :NEW.id := seq_bitacora.NEXTVAL;
    END IF;
END;
/


-- ═══════════════════════════════════════════
-- 5. ÍNDICES (rendimiento en JOINs frecuentes)
-- ═══════════════════════════════════════════

CREATE INDEX idx_jugador_equipo    ON jugadores (id_equipo);
CREATE INDEX idx_jugador_edad      ON jugadores (edad);
CREATE INDEX idx_jugador_valor     ON jugadores (valor);
CREATE INDEX idx_equipo_conf       ON equipos   (id_confederacion);
CREATE INDEX idx_estadio_ciudad    ON estadios  (id_ciudad);
CREATE INDEX idx_partido_equipo1   ON partidos  (id_equipo1);
CREATE INDEX idx_partido_equipo2   ON partidos  (id_equipo2);
CREATE INDEX idx_partido_estadio   ON partidos  (id_estadio);
CREATE INDEX idx_partido_grupo     ON partidos  (id_grupo);
CREATE INDEX idx_partido_fecha     ON partidos  (fecha_hora);
CREATE INDEX idx_bitacora_usuario  ON bitacora  (id_usuario);
CREATE INDEX idx_bitacora_ingreso  ON bitacora  (fecha_ingreso);
CREATE INDEX idx_ciudad_pais       ON ciudades  (pais);


-- ═══════════════════════════════════════════
-- 6. DATOS INICIALES
-- ═══════════════════════════════════════════

-- ── 6.1 Usuario Administrador inicial ───────────────────────
-- Contraseña: Admin1234
-- SHA-256 de "Admin1234" = 3e5c2b0d5a2f92e94d4d3b0c0b6a5d4e...
-- Generar el hash correcto ejecutando en Python:
--   import hashlib; print(hashlib.sha256("Admin1234".encode()).hexdigest())
-- y reemplazar el valor de abajo.
INSERT INTO usuarios (username, password, rol)
VALUES (
    'admin',
    '60fe74406e7f353ed979f350f2fbb6a2e8690a5fa7d1b0c32983d1d8b3f95f67',
    'Admin'
);

-- ── 6.2 Confederaciones ─────────────────────────────────────
INSERT INTO confederaciones (nombre) VALUES ('UEFA');
INSERT INTO confederaciones (nombre) VALUES ('CONMEBOL');
INSERT INTO confederaciones (nombre) VALUES ('CONCACAF');
INSERT INTO confederaciones (nombre) VALUES ('CAF');
INSERT INTO confederaciones (nombre) VALUES ('AFC');
INSERT INTO confederaciones (nombre) VALUES ('OFC');

-- ── 6.3 Ciudades anfitrionas ────────────────────────────────
-- México
INSERT INTO ciudades (nombre, pais) VALUES ('Ciudad de México', 'México');
INSERT INTO ciudades (nombre, pais) VALUES ('Guadalajara',      'México');
INSERT INTO ciudades (nombre, pais) VALUES ('Monterrey',        'México');

-- USA
INSERT INTO ciudades (nombre, pais) VALUES ('New York',         'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Los Angeles',      'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Dallas',           'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Miami',            'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('San Francisco',    'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Seattle',          'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Boston',           'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Houston',          'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Atlanta',          'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Kansas City',      'USA');
INSERT INTO ciudades (nombre, pais) VALUES ('Philadelphia',     'USA');

-- Canadá
INSERT INTO ciudades (nombre, pais) VALUES ('Toronto',          'Canadá');
INSERT INTO ciudades (nombre, pais) VALUES ('Vancouver',        'Canadá');

-- ── 6.4 Estadios ────────────────────────────────────────────
-- Los id_ciudad se referencian por posición de inserción (secuencia)
-- Ciudad de México = 1, Guadalajara = 2, Monterrey = 3,
-- New York = 4, Los Angeles = 5, Dallas = 6, Miami = 7 ...
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Estadio Azteca',                     87500, 1);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Estadio Akron',                      49850, 2);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Estadio BBVA',                       53500, 3);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('MetLife Stadium',                    82500, 4);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('SoFi Stadium',                       70240, 5);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('AT&&T Stadium',                       80000, 6);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Hard Rock Stadium',                  65326, 7);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Levi''s Stadium',                    68500, 8);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Lumen Field',                        69000, 9);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Gillette Stadium',                   65878, 10);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('NRG Stadium',                        72220, 11);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Mercedes-Benz Stadium',              71000, 12);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Arrowhead Stadium',                  76416, 13);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('Lincoln Financial Field',            69796, 14);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('BMO Field',                          45000, 15);
INSERT INTO estadios (nombre, capacidad, id_ciudad)
VALUES ('BC Place',                           54500, 16);

-- ── 6.5 Grupos (A–L, 12 grupos para 48 equipos) ─────────────
INSERT INTO grupos (letra) VALUES ('A');
INSERT INTO grupos (letra) VALUES ('B');
INSERT INTO grupos (letra) VALUES ('C');
INSERT INTO grupos (letra) VALUES ('D');
INSERT INTO grupos (letra) VALUES ('E');
INSERT INTO grupos (letra) VALUES ('F');
INSERT INTO grupos (letra) VALUES ('G');
INSERT INTO grupos (letra) VALUES ('H');
INSERT INTO grupos (letra) VALUES ('I');
INSERT INTO grupos (letra) VALUES ('J');
INSERT INTO grupos (letra) VALUES ('K');
INSERT INTO grupos (letra) VALUES ('L');

COMMIT;


-- ═══════════════════════════════════════════
-- 7. VERIFICACIÓN RÁPIDA
-- ═══════════════════════════════════════════

SELECT 'confederaciones' AS tabla, COUNT(*) AS registros FROM confederaciones
UNION ALL
SELECT 'ciudades',   COUNT(*) FROM ciudades
UNION ALL
SELECT 'estadios',   COUNT(*) FROM estadios
UNION ALL
SELECT 'grupos',     COUNT(*) FROM grupos
UNION ALL
SELECT 'equipos',    COUNT(*) FROM equipos
UNION ALL
SELECT 'jugadores',  COUNT(*) FROM jugadores
UNION ALL
SELECT 'partidos',   COUNT(*) FROM partidos
UNION ALL
SELECT 'usuarios',   COUNT(*) FROM usuarios
UNION ALL
SELECT 'bitacora',   COUNT(*) FROM bitacora;