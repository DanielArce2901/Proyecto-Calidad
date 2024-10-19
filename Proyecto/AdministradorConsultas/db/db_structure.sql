-- Crear la base de datos
--CREATE DATABASE querymanager;

-- Creación de la tabla Cursos
CREATE TABLE IF NOT EXISTS Cursos (
    codigo VARCHAR(10) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Creación de la tabla Profesores
CREATE TABLE IF NOT EXISTS Profesores (
    id_profesor SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    dias_consulta VARCHAR(50),
    horario_consulta VARCHAR(100),
    citas_totales INTEGER,
    citas_reservadas INTEGER
);

-- Creación de la tabla Cursos_Profesores
CREATE TABLE IF NOT EXISTS Cursos_Profesores (
    id_profesor INTEGER,
    codigo_curso VARCHAR(10),
    PRIMARY KEY (id_profesor, codigo_curso),
    FOREIGN KEY (id_profesor) REFERENCES Profesores(id_profesor) ON DELETE CASCADE,
    FOREIGN KEY (codigo_curso) REFERENCES Cursos(codigo) ON DELETE CASCADE
);

-- Creación de la tabla Estudiantes
CREATE TABLE IF NOT EXISTS Estudiantes (
    carnet VARCHAR(20) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

-- Creación de la tabla Estudiantes_Cursos
CREATE TABLE IF NOT EXISTS Estudiantes_Cursos (
    carnet VARCHAR(20),
    codigo_curso VARCHAR(10),
    veces_llevado INTEGER,
    estrellas INTEGER,
    PRIMARY KEY (carnet, codigo_curso),
    FOREIGN KEY (carnet) REFERENCES Estudiantes(carnet) ON DELETE CASCADE,
    FOREIGN KEY (codigo_curso) REFERENCES Cursos(codigo) ON DELETE CASCADE
);

-- Creación de la tabla Citas
CREATE TABLE IF NOT EXISTS Citas (
    id_cita SERIAL PRIMARY KEY,
    carnet_estudiante VARCHAR(20),
    id_profesor INTEGER,
    codigo_curso VARCHAR(10),
    fecha DATE,
    hora TIME,
    duracion INTEGER,
    estado VARCHAR(20),
    FOREIGN KEY(carnet_estudiante) REFERENCES Estudiantes(carnet),
    FOREIGN KEY(id_profesor) REFERENCES Profesores(id_profesor),
    FOREIGN KEY(codigo_curso) REFERENCES Cursos(codigo)
);

-- Creación de la tabla Semestre
CREATE TABLE IF NOT EXISTS Semestre (
    id_semestre SERIAL PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL
);
