import tkinter as tk
from tkinter import ttk, messagebox
from gui import mantenimiento, citas, reportes

class SistemaHorariosApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Administración de Horarios de Consulta")
        self.geometry("1300x700")
        self.create_widgets()

    def create_widgets(self):
        
        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill='both')

        
        self.mantenimiento_frame = mantenimiento.MantenimientoFrame(notebook)
        notebook.add(self.mantenimiento_frame, text="Mantenimiento de Datos")

        
        self.asignacion_citas_frame = citas.AsignacionCitasFrame(notebook)
        notebook.add(self.asignacion_citas_frame, text="Asignación de Citas")

        
        self.reportes_frame = reportes.ReportesFrame(notebook)
        notebook.add(self.reportes_frame, text="Reportes")

if __name__ == "__main__":
    app = SistemaHorariosApp()
    app.mainloop()
