-- Eliminar las tablas de la base de datos en un orden específico para evitar errores de clave foránea

DROP TABLE IF EXISTS Citas;
DROP TABLE IF EXISTS Estudiantes_Cursos;
DROP TABLE IF EXISTS Cursos_Profesores;
DROP TABLE IF EXISTS Estudiantes;
DROP TABLE IF EXISTS Profesores;
DROP TABLE IF EXISTS Cursos;
DROP TABLE IF EXISTS Semestre;
