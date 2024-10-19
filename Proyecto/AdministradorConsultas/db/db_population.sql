-- Población de Cursos
INSERT INTO Cursos (codigo, nombre) VALUES
('TI3404', 'Taller de Programación'),
('TI3600', 'Estructuras de Datos'),
('TI3700', 'Bases de Datos'),
('TI4500', 'Sistemas Operativos'),
('TI4600', 'Redes de Computadoras');

-- Población de Profesores
INSERT INTO Profesores (nombre, dias_consulta, horario_consulta, citas_totales, citas_reservadas) VALUES
('Isaac Alpízar', 'lunes, martes', '15:00-17:00, 08:00-09:00', 12, 4),
('Ana María Rodríguez', 'miércoles, viernes', '10:00-12:00, 14:00-16:00', 12, 6),
('Carlos Ramírez', 'lunes, jueves', '11:00-13:00, 16:00-18:00', 12, 3),
('Javier Morera', 'martes, jueves', '09:00-11:00, 14:00-16:00', 12, 5),
('Laura Quesada', 'lunes, viernes', '08:00-10:00, 12:00-14:00', 12, 2),
('Marcos Esquivel', 'miércoles, jueves', '13:00-15:00, 09:00-10:30', 12, 5),
('Sara Vargas', 'martes, viernes', '10:00-12:00, 15:00-17:00', 12, 4);

-- Población de Cursos_Profesores
INSERT INTO Cursos_Profesores (id_profesor, codigo_curso) VALUES
(1, 'TI3404'),
(1, 'TI4500'),
(2, 'TI3600'),
(2, 'TI4600'),
(3, 'TI3700'),
(4, 'TI3404'),
(4, 'TI4600'),
(5, 'TI3700'),
(6, 'TI4500'),
(7, 'TI3404'),
(7, 'TI4500');

-- Población de Estudiantes
INSERT INTO Estudiantes (carnet, nombre) VALUES
('2018489', 'Juan Pérez'),
('2019456', 'María Gómez'),
('2020567', 'Luis Rodríguez'),
('2021456', 'Andrea Castillo'),
('2022456', 'Roberto Jiménez'),
('2023567', 'Sofía López'),
('2024456', 'Pedro Sánchez');

-- Población de Estudiantes_Cursos
INSERT INTO Estudiantes_Cursos (carnet, codigo_curso, veces_llevado, estrellas) VALUES
('2018489', 'TI3404', 1, 3),
('2018489', 'TI3600', 0, 2),
('2019456', 'TI3600', 0, 3),
('2019456', 'TI3700', 1, 2),
('2020567', 'TI3404', 0, 1),
('2020567', 'TI3700', 0, 3),
('2018489', 'TI3700', 2, 2),
('2020567', 'TI3600', 2, 3),
('2021456', 'TI4500', 1, 2),
('2022456', 'TI3404', 0, 3),
('2023567', 'TI4500', 0, 2),
('2024456', 'TI4600', 0, 1),
('2021456', 'TI4600', 0, 2),
('2022456', 'TI3600', 1, 3);

-- Población del Semestre
INSERT INTO Semestre (fecha_inicio, fecha_fin) VALUES
('2024-08-01', '2024-12-15');

-- Población de Citas
INSERT INTO Citas (carnet_estudiante, id_profesor, codigo_curso, fecha, hora, duracion, estado) VALUES
('2018489', 1, 'TI3404', '2024-09-02', '15:00', 30, 'reservada'), 
('2019456', 2, 'TI3600', '2024-09-04', '10:00', 30, 'reservada'), 
('2020567', 3, 'TI3700', '2024-09-03', '11:00', 30, 'no reservada'), 
(NULL, 4, 'TI3404', '2024-09-03', '09:00', 30, 'no reservada'),
(NULL, 5, 'TI3700', '2024-09-05', '08:00', 30, 'no reservada'), 
(NULL, 1, 'TI3404', '2024-09-02', '08:00', 30, 'no reservada'),
(NULL, 2, 'TI3600', '2024-09-06', '14:00', 30, 'reservada'),
('2021456', 1, 'TI4500', '2024-09-06', '16:00', 30, 'reservada'), 
('2022456', 4, 'TI3404', '2024-09-05', '11:00', 30, 'no reservada'),
('2023567', 7, 'TI4500', '2024-09-09', '12:00', 30, 'no reservada'),
('2024456', 2, 'TI4600', '2024-09-10', '13:00', 30, 'reservada'), 
('2021456', 6, 'TI4600', '2024-09-11', '09:00', 30, 'reservada'), 
('2018489', 1, 'TI4500', '2024-09-12', '08:30', 30, 'no reservada'),
('2023567', 3, 'TI4500', '2024-09-13', '15:30', 30, 'no reservada'), 
('2022456', 7, 'TI3404', '2024-09-13', '12:00', 30, 'reservada'), 
('2020567', 3, 'TI4500', '2024-09-12', '10:00', 30, 'reservada'); 

