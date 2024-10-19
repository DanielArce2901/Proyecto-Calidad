import tkinter as tk 
from tkinter import ttk, messagebox
from db import execute_query
import re
import string

class MantenimientoFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()

    def create_widgets(self):
        tabs = ttk.Notebook(self)
        tabs.pack(expand=True, fill='both')

        self.cursos_tab = CursosTab(tabs)
        tabs.add(self.cursos_tab, text="Cursos")

        self.profesores_tab = ProfesoresTab(tabs)
        tabs.add(self.profesores_tab, text="Profesores")

        self.estudiantes_tab = EstudiantesTab(tabs)
        tabs.add(self.estudiantes_tab, text="Estudiantes")

class Validaciones:
    def __init__(self):
        pass

    @staticmethod
    def validar_texto(texto, min_len=1, max_len=255):
        if not isinstance(texto, str):
            return False
        return min_len <= len(texto) <= max_len

    @staticmethod
    def validar_numero(numero, min_val=None, max_val=None):
        try:
            numero = float(numero)
            if (min_val is not None and numero < min_val) or (max_val is not None and numero > max_val):
                return False
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_cadena(cadena):
        caracteres_permitidos = set(string.ascii_letters + ' ')
        for char in cadena:
            if char not in caracteres_permitidos:
                return False
        return True

    @staticmethod
    def validar_formato_horas(cadena):
        patron = r'^\d{2}:\d{2}-\d{2}:\d{2}$'
        cadenas = cadena.split(",")
        for c in cadenas:
            c = c.strip()
            if not re.match(patron, c):
                return False
        return True

    @staticmethod
    def validar_dias_semana(cadena):
        if not isinstance(cadena, str):
            return False
        dias_validos = {'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'}
        lista_dias = [dia.strip().lower() for dia in cadena.split(',')]
        for dia in lista_dias:
            if dia not in dias_validos:
                return False
        return True

    @staticmethod
    def validar_cadena_unica(cadena, tabla, columna):
        try:
            query = f"SELECT 1 FROM {tabla} WHERE {columna} = %s LIMIT 1;"
            result = execute_query(query, (cadena,), fetch=True)
            return len(result) == 0
        except Exception as e:
            print(f"Error al verificar la cadena en la base de datos: {e}")
            return False

class CursosTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_cursos()

    def create_widgets(self):
        lbl_codigo = ttk.Label(self, text="Código del Curso:")
        lbl_codigo.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_codigo = ttk.Entry(self)
        self.entry_codigo.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre = ttk.Label(self, text="Nombre del Curso:")
        lbl_nombre.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        self.btn_agregar = ttk.Button(self, text="Agregar Curso", command=self.agregar_curso)
        self.btn_agregar.grid(row=2, column=0, padx=10, pady=10)

        self.btn_actualizar = ttk.Button(self, text="Actualizar Curso", command=self.actualizar_curso)
        self.btn_actualizar.grid(row=2, column=1, padx=10, pady=10)

        self.btn_eliminar = ttk.Button(self, text="Eliminar Curso", command=self.eliminar_curso)
        self.btn_eliminar.grid(row=2, column=2, padx=10, pady=10)

        self.treeview = ttk.Treeview(self, columns=("codigo", "nombre"), show='headings')
        self.treeview.heading("codigo", text="Código")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.column("nombre", width=300)  # Ampliar el ancho de la columna de nombre
        self.treeview.grid(row=3, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.load_cursos()

    def load_cursos(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)
        query = "SELECT codigo, nombre FROM Cursos"
        cursos = execute_query(query, fetch=True)
        for curso in cursos:
            self.treeview.insert('', 'end', values=curso)

    def agregar_curso(self):
        codigo = self.entry_codigo.get()
        nombre = self.entry_nombre.get()
        if Validaciones.validar_cadena_unica(codigo, "Cursos", "codigo"):
            if codigo and nombre:
                query = "INSERT INTO Cursos (codigo, nombre) VALUES (%s, %s)"
                execute_query(query, (codigo, nombre))
                self.load_cursos()
                messagebox.showinfo("Éxito", "Curso agregado exitosamente.")
                self.update_profesores_cursos()
                self.update_estudiantes_cursos()
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        else:
            messagebox.showwarning("Advertencia", "Ya existe un curso con ese código.")

    def actualizar_curso(self):
        selected_item = self.treeview.selection()
        if selected_item:
            codigo = self.entry_codigo.get()
            nombre = self.entry_nombre.get()
            if codigo and nombre:
                query = "UPDATE Cursos SET nombre = %s WHERE codigo = %s"
                execute_query(query, (nombre, codigo))
                self.load_cursos()
                messagebox.showinfo("Éxito", "Curso actualizado exitosamente.")
                self.update_profesores_cursos()
                self.update_estudiantes_cursos()
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un curso para actualizar.")

    def eliminar_curso(self):
        selected_item = self.treeview.selection()
        if selected_item:
            codigo = self.treeview.item(selected_item)['values'][0]
            query = "DELETE FROM Cursos WHERE codigo = %s"
            execute_query(query, (codigo,))
            self.load_cursos()
            messagebox.showinfo("Éxito", "Curso eliminado exitosamente.")
            self.update_profesores_cursos()
            self.update_estudiantes_cursos()
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un curso para eliminar.")

    def update_profesores_cursos(self):
        self.master.profesor_tab.load_cursos()

    def update_estudiantes_cursos(self):
        self.master.estudiantes_tab.load_cursos()

class ProfesoresTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_profesores()

    def create_widgets(self):
        lbl_nombre = ttk.Label(self, text="Nombre del Profesor:")
        lbl_nombre.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        lbl_curso = ttk.Label(self, text="Cursos que Atiende:")
        lbl_curso.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.listbox_cursos = tk.Listbox(self, selectmode="multiple", height=5, width=40)
        self.listbox_cursos.grid(row=1, column=1, padx=10, pady=10)

        lbl_dias = ttk.Label(self, text="Días de Consulta:")
        lbl_dias.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.entry_dias = ttk.Entry(self)
        self.entry_dias.grid(row=2, column=1, padx=10, pady=10)

        lbl_horarios = ttk.Label(self, text="Horarios de Consulta:")
        lbl_horarios.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_horarios = ttk.Entry(self)
        self.entry_horarios.grid(row=3, column=1, padx=10, pady=10)

        lbl_citas_totales = ttk.Label(self, text="Citas Totales:")
        lbl_citas_totales.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_citas_totales = ttk.Entry(self)
        self.entry_citas_totales.grid(row=4, column=1, padx=10, pady=10)

        lbl_citas_reservadas = ttk.Label(self, text="Citas Reservadas:")
        lbl_citas_reservadas.grid(row=5, column=0, padx=10, pady=10, sticky='e')
        self.entry_citas_reservadas = ttk.Entry(self)
        self.entry_citas_reservadas.grid(row=5, column=1, padx=10, pady=10)

        self.btn_agregar = ttk.Button(self, text="Agregar Profesor", command=self.agregar_profesor)
        self.btn_agregar.grid(row=6, column=0, padx=10, pady=10)

        self.btn_actualizar = ttk.Button(self, text="Actualizar Profesor", command=self.actualizar_profesor)
        self.btn_actualizar.grid(row=6, column=1, padx=10, pady=10)

        self.btn_eliminar = ttk.Button(self, text="Eliminar Profesor", command=self.eliminar_profesor)
        self.btn_eliminar.grid(row=6, column=2, padx=10, pady=10)

        self.treeview = ttk.Treeview(self, columns=("id_profesor", "nombre", "cursos", "dias", "horarios", "citas_totales", "citas_reservadas"), show='headings')
        self.treeview.heading("id_profesor", text="ID")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("cursos", text="Cursos")
        self.treeview.heading("dias", text="Días")
        self.treeview.heading("horarios", text="Horarios")
        self.treeview.heading("citas_totales", text="Citas Totales")
        self.treeview.heading("citas_reservadas", text="Citas Reservadas")
        self.treeview.grid(row=7, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.load_cursos()

    def load_profesores(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        query = """
        SELECT p.id_profesor, p.nombre, STRING_AGG(c.codigo, ', ') AS cursos, p.dias_consulta, p.horario_consulta, p.citas_totales, p.citas_reservadas
        FROM Profesores p
        LEFT JOIN Cursos_Profesores cp ON p.id_profesor = cp.id_profesor
        LEFT JOIN Cursos c ON cp.codigo_curso = c.codigo
        GROUP BY p.id_profesor, p.nombre, p.dias_consulta, p.horario_consulta, p.citas_totales, p.citas_reservadas
        """
        profesores = execute_query(query, fetch=True)
        for profesor in profesores:
            self.treeview.insert('', 'end', values=profesor)

    def load_cursos(self):
        self.listbox_cursos.delete(0, tk.END)
        query = "SELECT codigo, nombre FROM Cursos"
        cursos = execute_query(query, fetch=True)
        for codigo, nombre in cursos:
            self.listbox_cursos.insert(tk.END, f"{codigo} - {nombre}")

    def agregar_profesor(self):
        nombre = self.entry_nombre.get()
        cursos_seleccionados = [self.listbox_cursos.get(i).split(" - ")[0] for i in self.listbox_cursos.curselection()]
        dias = self.entry_dias.get()
        horarios = self.entry_horarios.get()
        citas_totales = self.entry_citas_totales.get()
        citas_reservadas = self.entry_citas_reservadas.get()

        if nombre and cursos_seleccionados and dias and horarios and citas_totales and citas_reservadas and Validaciones.validar_dias_semana(dias) and Validaciones.validar_formato_horas(horarios) and Validaciones.validar_numero(citas_totales) and Validaciones.validar_numero(citas_reservadas):
            try:
                insert_profesor_query = """
                INSERT INTO Profesores (nombre, dias_consulta, horario_consulta, citas_totales, citas_reservadas) 
                VALUES (%s, %s, %s, %s, %s)
                """
                execute_query(insert_profesor_query, (nombre, dias, horarios, citas_totales, citas_reservadas))

                get_last_id_query = "SELECT id_profesor FROM Profesores ORDER BY id_profesor DESC LIMIT 1"
                id_profesor = execute_query(get_last_id_query, fetch=True)[0][0]

                for curso in cursos_seleccionados:
                    insert_curso_profesor_query = "INSERT INTO Cursos_Profesores (id_profesor, codigo_curso) VALUES (%s, %s)"
                    execute_query(insert_curso_profesor_query, (id_profesor, curso))

                self.load_profesores()
                messagebox.showinfo("Éxito", "Profesor y citas agregados exitosamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo agregar el profesor: {e}")
        else:
            messagebox.showwarning("Advertencia", "Por favor complete todos los campos o verifique los datos.")

    def actualizar_profesor(self):
        selected_item = self.treeview.selection()
        if selected_item:
            id_profesor = self.treeview.item(selected_item)['values'][0]
            nombre = self.entry_nombre.get()
            cursos_seleccionados = [self.listbox_cursos.get(i).split(" - ")[0] for i in self.listbox_cursos.curselection()]
            dias = self.entry_dias.get()
            horarios = self.entry_horarios.get()
            citas_totales = self.entry_citas_totales.get()
            citas_reservadas = self.entry_citas_reservadas.get()

            if nombre and cursos_seleccionados and dias and horarios and citas_totales and citas_reservadas:
                query = "UPDATE Profesores SET nombre = %s, dias_consulta = %s, horario_consulta = %s, citas_totales = %s, citas_reservadas = %s WHERE id_profesor = %s"
                execute_query(query, (nombre, dias, horarios, citas_totales, citas_reservadas, id_profesor))

                query = "DELETE FROM Cursos_Profesores WHERE id_profesor = %s"
                execute_query(query, (id_profesor,))
                for curso in cursos_seleccionados:
                    query = "INSERT INTO Cursos_Profesores (id_profesor, codigo_curso) VALUES (%s, %s)"
                    execute_query(query, (id_profesor, curso))

                self.load_profesores()
                messagebox.showinfo("Éxito", "Profesor actualizado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un profesor para actualizar.")

    def eliminar_profesor(self):
        selected_item = self.treeview.selection()
        if selected_item:
            id_profesor = self.treeview.item(selected_item)['values'][0]

            query = "DELETE FROM Cursos_Profesores WHERE id_profesor = %s"
            execute_query(query, (id_profesor,))

            query = "DELETE FROM Profesores WHERE id_profesor = %s"
            execute_query(query, (id_profesor,))

            self.load_profesores()
            messagebox.showinfo("Éxito", "Profesor eliminado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un profesor para eliminar.")

class EstudiantesTab(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.create_widgets()
        self.load_estudiantes()
        self.load_cursos()

    def create_widgets(self):
        lbl_carnet = ttk.Label(self, text="Carnet:")
        lbl_carnet.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.entry_carnet = ttk.Entry(self)
        self.entry_carnet.grid(row=0, column=1, padx=10, pady=10)

        lbl_nombre = ttk.Label(self, text="Nombre del Estudiante:")
        lbl_nombre.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entry_nombre = ttk.Entry(self)
        self.entry_nombre.grid(row=1, column=1, padx=10, pady=10)

        lbl_curso = ttk.Label(self, text="Cursos Actuales:")
        lbl_curso.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.listbox_cursos = tk.Listbox(self, selectmode="multiple", height=5, width=40)
        self.listbox_cursos.grid(row=2, column=1, padx=10, pady=10)

        lbl_veces_llevado = ttk.Label(self, text="Veces Llevado:")
        lbl_veces_llevado.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.entry_veces_llevado = ttk.Entry(self)
        self.entry_veces_llevado.grid(row=3, column=1, padx=10, pady=10)

        lbl_estrellas = ttk.Label(self, text="Estrellas:")
        lbl_estrellas.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.entry_estrellas = ttk.Entry(self)
        self.entry_estrellas.grid(row=4, column=1, padx=10, pady=10)

        self.btn_agregar = ttk.Button(self, text="Agregar Estudiante", command=self.agregar_estudiante)
        self.btn_agregar.grid(row=5, column=0, padx=10, pady=10)

        self.btn_actualizar = ttk.Button(self, text="Actualizar Estudiante", command=self.actualizar_estudiante)
        self.btn_actualizar.grid(row=5, column=1, padx=10, pady=10)

        self.btn_eliminar = ttk.Button(self, text="Eliminar Estudiante", command=self.eliminar_estudiante)
        self.btn_eliminar.grid(row=5, column=2, padx=10, pady=10)

        self.treeview = ttk.Treeview(self, columns=("carnet", "nombre", "cursos", "veces_llevado", "estrellas"), show='headings')
        self.treeview.heading("carnet", text="Carnet")
        self.treeview.heading("nombre", text="Nombre")
        self.treeview.heading("cursos", text="Cursos")
        self.treeview.heading("veces_llevado", text="Veces Llevado")
        self.treeview.heading("estrellas", text="Estrellas")
        self.treeview.grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        self.load_estudiantes()

    def load_estudiantes(self):
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        query = """
        SELECT e.carnet, e.nombre, STRING_AGG(c.codigo, ', ') AS cursos, ec.veces_llevado, ec.estrellas
        FROM Estudiantes e
        LEFT JOIN Estudiantes_Cursos ec ON e.carnet = ec.carnet
        LEFT JOIN Cursos c ON ec.codigo_curso = c.codigo
        GROUP BY e.carnet, e.nombre, ec.veces_llevado, ec.estrellas
        """
        estudiantes = execute_query(query, fetch=True)
        for estudiante in estudiantes:
            self.treeview.insert('', 'end', values=estudiante)

    def load_cursos(self):
        self.listbox_cursos.delete(0, tk.END)
        query = "SELECT codigo, nombre FROM Cursos"
        cursos = execute_query(query, fetch=True)
        for codigo, nombre in cursos:
            self.listbox_cursos.insert(tk.END, f"{codigo} - {nombre}")

    def agregar_estudiante(self):
        carnet = self.entry_carnet.get()
        nombre = self.entry_nombre.get()
        cursos_seleccionados = [self.listbox_cursos.get(i).split(" - ")[0] for i in self.listbox_cursos.curselection()]
        veces_llevado = self.entry_veces_llevado.get()
        estrellas = self.entry_estrellas.get()
        if Validaciones.validar_cadena_unica(carnet, "Estudiantes", "carnet"):
            if carnet and nombre and cursos_seleccionados and veces_llevado and estrellas and Validaciones.validar_numero(veces_llevado) and Validaciones.validar_numero(estrellas, 0, 3) and Validaciones.validar_cadena(nombre) and Validaciones.validar_numero(carnet):
                query = "INSERT INTO Estudiantes (carnet, nombre) VALUES (%s, %s) ON CONFLICT (carnet) DO NOTHING"
                execute_query(query, (carnet, nombre))

                for curso in cursos_seleccionados:
                    query = """
                    INSERT INTO Estudiantes_Cursos (carnet, codigo_curso, veces_llevado, estrellas)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (carnet, codigo_curso) DO UPDATE
                    SET veces_llevado = EXCLUDED.veces_llevado, estrellas = EXCLUDED.estrellas
                    """
                    execute_query(query, (carnet, curso, veces_llevado, estrellas))

                self.load_estudiantes()
                messagebox.showinfo("Éxito", "Estudiante agregado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos o verifique los datos.")
        else:
            messagebox.showwarning("Advertencia", "El carnet ya está registrado.")

    def actualizar_estudiante(self):
        selected_item = self.treeview.selection()
        if selected_item:
            carnet = self.treeview.item(selected_item)['values'][0]
            nombre = self.entry_nombre.get()
            cursos_seleccionados = [self.listbox_cursos.get(i).split(" - ")[0] for i in self.listbox_cursos.curselection()]
            veces_llevado = self.entry_veces_llevado.get()
            estrellas = self.entry_estrellas.get()

            if nombre and cursos_seleccionados and veces_llevado and estrellas:
                query = "UPDATE Estudiantes SET nombre = %s WHERE carnet = %s"
                execute_query(query, (nombre, str(carnet)))

                for curso in cursos_seleccionados:
                    query = """
                    INSERT INTO Estudiantes_Cursos (carnet, codigo_curso, veces_llevado, estrellas)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (carnet, codigo_curso) DO UPDATE
                    SET veces_llevado = EXCLUDED.veces_llevado, estrellas = EXCLUDED.estrellas
                    """
                    execute_query(query, (str(carnet), curso, veces_llevado, estrellas))

                self.load_estudiantes()
                messagebox.showinfo("Éxito", "Estudiante actualizado exitosamente.")
            else:
                messagebox.showwarning("Advertencia", "Por favor complete todos los campos.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante para actualizar.")

    def eliminar_estudiante(self):
        selected_item = self.treeview.selection()
        if selected_item:
            carnet = self.treeview.item(selected_item)['values'][0]

            query = "DELETE FROM Estudiantes_Cursos WHERE carnet = %s"
            execute_query(query, (carnet,))

            query = "DELETE FROM Estudiantes WHERE carnet = %s"
            execute_query(query, (carnet,))

            self.load_estudiantes()
            messagebox.showinfo("Éxito", "Estudiante eliminado exitosamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor seleccione un estudiante para eliminar.")


