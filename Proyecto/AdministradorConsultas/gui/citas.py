import tkinter as tk
from tkinter import ttk, messagebox
from db import execute_query
from datetime import datetime
import locale

locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class AsignacionCitasFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Label y Entry para el Carnet del Estudiante
        lbl_carnet = ttk.Label(self, text="Carnet del Estudiante:")
        lbl_carnet.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_carnet = ttk.Entry(self)
        self.entry_carnet.grid(row=0, column=1, padx=10, pady=10)

        # Botón para Buscar Cursos
        self.btn_buscar = ttk.Button(self, text="Buscar Cursos", command=self.buscar_cursos)
        self.btn_buscar.grid(row=0, column=2, padx=10, pady=10)

        # Lista de Cursos y Opciones de Asignación
        self.treeview_cursos = ttk.Treeview(self, columns=("codigo", "nombre", "profesor", "dias", "horarios", "citas_totales", "citas_disponibles", "duracion"), show='headings')
        self.treeview_cursos.heading("codigo", text="Código")
        self.treeview_cursos.heading("nombre", text="Nombre")
        self.treeview_cursos.heading("profesor", text="Profesor")
        self.treeview_cursos.heading("dias", text="Días")
        self.treeview_cursos.heading("horarios", text="Horarios")
        self.treeview_cursos.heading("citas_totales", text="Citas Totales")
        self.treeview_cursos.heading("citas_disponibles", text="Citas Disponibles")
        self.treeview_cursos.heading("duracion", text="Duración de Cita")

        # Ajustar el ancho de las columnas
        self.treeview_cursos.column("codigo", width=100)
        self.treeview_cursos.column("nombre", width=150)
        self.treeview_cursos.column("profesor", width=150)
        self.treeview_cursos.column("dias", width=100)
        self.treeview_cursos.column("horarios", width=120)
        self.treeview_cursos.column("citas_totales", width=100)
        self.treeview_cursos.column("citas_disponibles", width=120)
        self.treeview_cursos.column("duracion", width=150)

        self.treeview_cursos.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Botón para Asignar Cita
        self.btn_asignar = ttk.Button(self, text="Asignar Cita", command=self.asignar_cita)
        self.btn_asignar.grid(row=2, column=1, padx=10, pady=10)

    def buscar_cursos(self):
        carnet = self.entry_carnet.get()
        if carnet:
            # Limpiar el Treeview antes de realizar la nueva búsqueda
            for item in self.treeview_cursos.get_children():
                self.treeview_cursos.delete(item)

            # Cargar los cursos asociados al estudiante
            query = """
            SELECT c.codigo, c.nombre AS curso_nombre, p.nombre AS profesor_nombre, p.dias_consulta, p.horario_consulta, 
                p.citas_totales, (p.citas_totales - p.citas_reservadas) AS citas_disponibles, '30 minutos' AS duracion
            FROM Estudiantes_Cursos ec
            JOIN Cursos c ON ec.codigo_curso = c.codigo
            JOIN Cursos_Profesores cp ON c.codigo = cp.codigo_curso
            JOIN Profesores p ON cp.id_profesor = p.id_profesor
            WHERE ec.carnet = %s
            """

            cursos = execute_query(query, (carnet,), fetch=True)
            if cursos:
                for curso in cursos:
                    print(f"Curso encontrado: {curso}")  # Debug
                    self.treeview_cursos.insert('', 'end', values=curso)
            else:
                messagebox.showwarning("Advertencia", "No se encontraron cursos asociados a este carnet.")
        else:
            messagebox.showwarning("Advertencia", "Por favor ingrese el carnet del estudiante.")

    def asignar_cita(self):
        selected_item = self.treeview_cursos.selection()
        if selected_item:
            curso = self.treeview_cursos.item(selected_item)['values'][0]
            carnet = self.entry_carnet.get()

            query = """
            SELECT ec.veces_llevado, ec.estrellas, p.id_profesor, p.dias_consulta, p.horario_consulta, p.citas_totales, p.citas_reservadas
            FROM Estudiantes_Cursos ec
            JOIN Cursos_Profesores cp ON ec.codigo_curso = cp.codigo_curso
            JOIN Profesores p ON cp.id_profesor = p.id_profesor
            WHERE ec.codigo_curso = %s AND ec.carnet = %s
            """
            result = execute_query(query, (curso, carnet), fetch=True)
            if result:
                veces_llevado, estrellas, id_profesor, dias_consulta, horario_consulta, citas_totales, citas_reservadas = result[0]
                print(f"Datos del profesor y estudiante: {result[0]}")  # Debug
                prioridad = self.calcular_prioridad(id_profesor, veces_llevado, estrellas, citas_totales, citas_reservadas)
                if prioridad:
                    # Asignar la cita según la prioridad calculada
                    self.registrar_cita(carnet, id_profesor, curso, prioridad)
                    messagebox.showinfo("Éxito", f"Cita asignada con éxito para el curso {curso}.")
                else:
                    messagebox.showwarning("Advertencia", "No hay citas disponibles con la prioridad necesaria.")
            else:
                messagebox.showwarning("Advertencia", "No se encontraron datos del curso.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un curso para asignar una cita.")

    def calcular_prioridad(self, id_profesor, veces_llevado, estrellas, citas_totales, citas_reservadas):
        tasa_reservadas = citas_reservadas / citas_totales if citas_totales > 0 else 0  # Evitar división por 0
        print(f"Tasa de reservación: {tasa_reservadas}, Veces llevado: {veces_llevado}, Estrellas: {estrellas}")  # Debug

        if veces_llevado == 0:
            if estrellas == 1:
                return self.obtener_primera_cita_disponible(id_profesor)
            elif estrellas == 2:
                if tasa_reservadas >= 0.7:
                    return self.obtener_primera_cita_reservada(id_profesor)
                return self.obtener_primera_cita_disponible(id_profesor, semana_proxima=True)
            elif estrellas == 3:
                if tasa_reservadas >= 0.5:
                    return self.obtener_primera_cita_reservada(id_profesor)
                return self.obtener_primera_cita_disponible(id_profesor)

        elif veces_llevado == 1:
            if estrellas == 1:
                return self.obtener_primera_cita_disponible(id_profesor)
            elif estrellas == 2:
                if tasa_reservadas >= 0.5:
                    return self.obtener_primera_cita_reservada(id_profesor)
                return self.obtener_primera_cita_disponible(id_profesor)
            elif estrellas == 3:
                return self.obtener_primera_cita_reservada(id_profesor)

        elif veces_llevado >= 2:
            if estrellas == 1:
                return self.obtener_primera_cita_disponible(id_profesor)
            elif estrellas == 2:
                if tasa_reservadas >= 0.35:
                    return self.obtener_primera_cita_reservada(id_profesor)
                return self.obtener_primera_cita_disponible(id_profesor)
            elif estrellas == 3:
                return self.obtener_primera_cita_reservada(id_profesor)

        print("No se encontró ninguna cita disponible según la prioridad")  # Debug
        return None

    def obtener_primera_cita_disponible(self, id_profesor, semana_proxima=False):
        query_profesor = """
        SELECT p.dias_consulta, p.horario_consulta, p.citas_totales, p.citas_reservadas
        FROM Profesores p
        WHERE p.id_profesor = %s
        """
        profesor_info = execute_query(query_profesor, (id_profesor,), fetch=True)

        if not profesor_info:
            print("No se encontró la información del profesor.")  # Debug
            return None

        dias_consulta, horarios_consulta, citas_totales, citas_reservadas = profesor_info[0]
        dias = dias_consulta.split(',')
        horarios = horarios_consulta.split(',')

        print(f"Días de consulta: {dias}, Horarios: {horarios}, Citas totales: {citas_totales}, Citas reservadas: {citas_reservadas}")  # Debug

        for dia, horario in zip(dias, horarios):
            dia = dia.strip().lower()
            horario_inicio, horario_fin = horario.strip().split('-')
            print(f"Verificando el día {dia} con horario {horario_inicio} - {horario_fin}")  # Debug

            if citas_reservadas < citas_totales:
                nueva_cita = self.crear_cita_disponible(id_profesor, dia, horario_inicio)
                if nueva_cita:
                    return (dia, horario_inicio)
        print("No se encontró ninguna cita disponible.")  # Debug
        return None

    def crear_cita_disponible(self, id_profesor, dia, horario_inicio):
        query_insert_cita = """
        INSERT INTO Citas (id_profesor, fecha, hora, estado)
        VALUES (%s, current_date, %s, 'no reservada')
        RETURNING id_cita
        """
        nueva_cita = execute_query(query_insert_cita, (id_profesor, horario_inicio), fetch=True)

        if nueva_cita:
            query_update_profesor = """
            UPDATE Profesores
            SET citas_reservadas = citas_reservadas + 1
            WHERE id_profesor = %s
            """
            execute_query(query_update_profesor, (id_profesor,))
            print(f"Cita creada con éxito: {nueva_cita}")  # Debug
            return nueva_cita
        else:
            print("Error al crear la cita.")  # Debug
        return None

    def obtener_primera_cita_reservada(self, id_profesor):
        query = """
        SELECT p.dias_consulta, p.horario_consulta, c.fecha, c.hora
        FROM Profesores p
        LEFT JOIN Citas c ON p.id_profesor = c.id_profesor AND c.estado = 'reservada'
        WHERE p.id_profesor = %s
        ORDER BY c.fecha ASC, c.hora ASC
        """
        citas_reservadas = execute_query(query, (id_profesor,), fetch=True)

        if citas_reservadas:
            for cita in citas_reservadas:
                dia, horario = cita[0], cita[1]
                print(f"Cita reservada encontrada: {dia} a las {horario}")  # Debug
                return cita
        print("No se encontró ninguna cita reservada.")  # Debug
        return None

    def registrar_cita(self, carnet, id_profesor, curso, prioridad):
        dias, horarios = prioridad[0], prioridad[1]
        horario_inicio = horarios.split(",")[0].strip().split("-")[0] + ":00"
        print("HORA INICIO", horario_inicio)  # Debug

        check_query = """
        SELECT citas_totales, citas_reservadas
        FROM Profesores
        WHERE id_profesor = %s
        """
        result = execute_query(check_query, (id_profesor,), fetch=True)

        if result:
            citas_totales, citas_reservadas = result[0]
            if citas_reservadas < citas_totales:
                query = """
                INSERT INTO Citas (carnet_estudiante, id_profesor, codigo_curso, fecha, hora, duracion, estado)
                VALUES (%s, %s, %s, current_date, %s, 30, 'reservada')
                """
                execute_query(query, (carnet, id_profesor, curso, horario_inicio))

                update_query = """
                UPDATE Profesores
                SET citas_reservadas = citas_reservadas + 1
                WHERE id_profesor = %s
                """
                execute_query(update_query, (id_profesor,))
                messagebox.showinfo("Éxito", "Cita reservada con éxito.")
            else:
                messagebox.showwarning("Advertencia", "El profesor no tiene más citas disponibles.")
        else:
            messagebox.showwarning("Advertencia", "No se encontró al profesor especificado.")

