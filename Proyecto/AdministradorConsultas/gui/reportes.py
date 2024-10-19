import tkinter as tk
from tkinter import ttk, messagebox
from db import execute_query

class ReportesFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        # Filtro por Curso
        lbl_curso = ttk.Label(self, text="Curso:")
        lbl_curso.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.combo_curso = ttk.Combobox(self, state="readonly")
        self.combo_curso.grid(row=0, column=1, padx=10, pady=10)

        # Filtro por Profesor
        lbl_profesor = ttk.Label(self, text="Profesor:")
        lbl_profesor.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.combo_profesor = ttk.Combobox(self, state="readonly")
        self.combo_profesor.grid(row=1, column=1, padx=10, pady=10)

        # Filtro por Día
        lbl_dia = ttk.Label(self, text="Día:")
        lbl_dia.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.combo_dia = ttk.Combobox(self, state="readonly", values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
        self.combo_dia.grid(row=2, column=1, padx=10, pady=10)

        # Filtro por Estado de la Cita (Reservada o No Reservada)
        lbl_estado = ttk.Label(self, text="Estado de la Cita:")
        lbl_estado.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.combo_estado = ttk.Combobox(self, state="readonly", values=["Reservada", "No Reservada"])
        self.combo_estado.grid(row=3, column=1, padx=10, pady=10)

        # Botón para Generar Reporte
        self.btn_generar = ttk.Button(self, text="Generar Reporte", command=self.generar_reporte)
        self.btn_generar.grid(row=4, column=1, padx=10, pady=10)

        # Treeview para mostrar el resultado del reporte
        self.treeview = ttk.Treeview(self, columns=("curso", "profesor", "dia", "hora", "estado", "carnet", "estudiante"), show='headings')
        self.treeview.heading("curso", text="Curso")
        self.treeview.heading("profesor", text="Profesor")
        self.treeview.heading("dia", text="Día")
        self.treeview.heading("hora", text="Hora")
        self.treeview.heading("estado", text="Estado")
        self.treeview.heading("carnet", text="Carnet Estudiante")
        self.treeview.heading("estudiante", text="Nombre Estudiante")

        # Agregar columnas a la tabla para que no se corte
        self.treeview.column("curso", width=100)
        self.treeview.column("profesor", width=150)
        self.treeview.column("dia", width=100)
        self.treeview.column("hora", width=100)
        self.treeview.column("estado", width=100)
        self.treeview.column("carnet", width=150)
        self.treeview.column("estudiante", width=150)

        self.treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Cargar los cursos y profesores disponibles en los ComboBox
        self.load_cursos()
        self.load_profesores()

    def load_cursos(self):
        query = "SELECT codigo, nombre FROM Cursos"
        cursos = execute_query(query, fetch=True)
        self.combo_curso['values'] = [f"{codigo} - {nombre}" for codigo, nombre in cursos]

    def load_profesores(self):
        query = "SELECT id_profesor, nombre FROM Profesores"
        profesores = execute_query(query, fetch=True)
        self.combo_profesor['values'] = [f"{id_profesor} - {nombre}" for id_profesor, nombre in profesores]

    def generar_reporte(self):
        # Obtener los filtros seleccionados
        curso = self.combo_curso.get().split(" - ")[0] if self.combo_curso.get() else None
        profesor = self.combo_profesor.get().split(" - ")[0] if self.combo_profesor.get() else None
        dia = self.combo_dia.get()
        estado = self.combo_estado.get()

        # Convertir los días a inglés para la consulta SQL
        dias_semana = {
            "Lunes": "Monday", "Martes": "Tuesday", "Miércoles": "Wednesday", 
            "Jueves": "Thursday", "Viernes": "Friday", "Sábado": "Saturday", "Domingo": "Sunday"
        }
        if dia in dias_semana:
            dia = dias_semana[dia]

        # Establecer el estado de la cita
        estado_bd = "reservada" if estado == "Reservada" else "no reservada"

        # Consulta SQL para generar el reporte con filtros
        query = """
        SELECT c.codigo, p.nombre AS profesor_nombre, ci.fecha, ci.hora, ci.estado, e.carnet, e.nombre AS estudiante_nombre
        FROM Citas ci
        JOIN Cursos c ON c.codigo = ci.codigo_curso
        JOIN Profesores p ON p.id_profesor = ci.id_profesor
        JOIN Estudiantes e ON e.carnet = ci.carnet_estudiante
        WHERE 1=1
        """
        params = []

        if curso:
            query += " AND c.codigo = %s"
            params.append(curso)

        if profesor:
            query += " AND p.id_profesor = %s"
            params.append(profesor)

        if dia:
            query += " AND TO_CHAR(ci.fecha, 'Day') ILIKE %s"
            params.append(f"%{dia}%")

        if estado:
            query += " AND ci.estado = %s"
            params.append(estado_bd)

        # Ejecutar la consulta y mostrar los resultados
        resultados = execute_query(query, params, fetch=True)
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, resultados):
        # Limpiar los resultados actuales en el Treeview
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Insertar los nuevos resultados en el Treeview
        for resultado in resultados:
            curso, profesor, fecha, hora, estado, carnet, estudiante = resultado
            dia_semana = fecha.strftime("%A")  # Convertir la fecha al día de la semana en inglés
            self.treeview.insert('', 'end', values=(curso, profesor, dia_semana, hora, estado.capitalize(), carnet, estudiante))

