from fpdf import FPDF
import os

class DatabasePDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L', unit='mm', format='A4')
        self.set_auto_page_break(auto=True, margin=0)
        self.bg_color = (10, 10, 12)  # #0A0A0C
        self.accent_color = (0, 247, 255)  # #00F7FF
        self.text_color = (255, 255, 255)
        self.muted_color = (160, 160, 176) # #A0A0B0

    def header(self):
        if self.page_no() > 1:
            self.set_font('helvetica', 'B', 10)
            self.set_text_color(*self.accent_color)
            self.set_xy(10, 10)
            self.cell(0, 10, 'INTERACCIÓN CON BASES DE DATOS', ln=True)

    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.set_text_color(*self.muted_color)
        self.cell(0, 10, f'Página {self.page_no()}', align='C')

    def add_slide_bg(self):
        self.set_fill_color(*self.bg_color)
        self.rect(0, 0, 297, 210, 'F')

    def title_slide(self, title, subtitle, img_path):
        self.add_page()
        self.add_slide_bg()
        
        # Image
        if os.path.exists(img_path):
            self.image(img_path, x=160, y=40, w=110)
        
        # Text
        self.set_xy(20, 80)
        self.set_font('helvetica', 'B', 45)
        self.set_text_color(255, 255, 255)
        self.multi_cell(130, 20, title)
        
        self.set_xy(20, 130)
        self.set_font('helvetica', '', 18)
        self.set_text_color(*self.muted_color)
        self.multi_cell(130, 10, subtitle)

    def content_slide(self, title, text, img_path=None, icon=None, example=None, reverse=False):
        self.add_page()
        self.add_slide_bg()
        
        self.set_xy(20, 30)
        self.set_font('helvetica', 'B', 32)
        self.set_text_color(*self.accent_color)
        self.cell(0, 20, title, ln=True)
        
        text_x = 20 if not reverse else 140
        img_x = 160 if not reverse else 20
        
        if img_path and os.path.exists(img_path):
            self.image(img_path, x=img_x, y=60, w=110)
            
        self.set_xy(text_x, 70)
        self.set_font('helvetica', '', 16)
        self.set_text_color(255, 255, 255)
        self.multi_cell(130, 10, text)
        
        if example:
            self.set_xy(text_x, 140)
            self.set_fill_color(0, 247, 255)
            self.rect(text_x, 140, 2, 30, 'F')
            self.set_xy(text_x + 10, 145)
            self.set_font('helvetica', 'I', 14)
            self.set_text_color(*self.muted_color)
            self.multi_cell(120, 8, f"Ejemplo: {example}")

    def list_slide(self, title, items):
        self.add_page()
        self.add_slide_bg()
        
        self.set_xy(20, 30)
        self.set_font('helvetica', 'B', 32)
        self.set_text_color(*self.accent_color)
        self.cell(0, 20, title, ln=True)
        
        self.set_xy(30, 70)
        self.set_font('helvetica', '', 18)
        self.set_text_color(255, 255, 255)
        for item in items:
            self.cell(10, 15, '>', ln=0)
            self.cell(0, 15, item, ln=True)

# Generate PDF
pdf = DatabasePDF()

# 1. Cover
pdf.title_slide("Interacción con Bases de Datos", 
                "Usuarios y Administradores en el ecosistema de datos", 
                "assets/hero.png")

# 2. Objetivo
pdf.content_slide("Objetivo Primario", 
                  "El objetivo primario de una base de datos es ver la información que tiene guardada (Visualizar) y guardar nueva información en la base de datos (Almacenar).",
                  icon="🎯")

# 4. Naive
pdf.content_slide("Usuarios Naive", 
                  "Interactúan con la base de datos mediante algún programa o aplicación ya escrito.",
                  img_path="assets/naive.png",
                  example="Empleado de banco que requiere transferir dinero de una cuenta a otra invoca el programa 'transferir'.")

# 5. Programadores
pdf.content_slide("Programadores de Aplicación", 
                  "Personas que escriben las aplicaciones que interactúan con el sistema.",
                  img_path="assets/programmer.png",
                  reverse=True)

# 6. Sofisticados
pdf.content_slide("Usuarios Sofisticados", 
                  "Interactúan con el sistema sin escribir programas. Lo hacen mediante queries que suben a un procesador de queries.",
                  img_path="assets/sophisticated.png")

# 7. Especializados
pdf.content_slide("Usuarios Especializados", 
                  "Escriben aplicaciones de bases de datos especializadas que van más allá del procesamiento de datos tradicional.",
                  img_path="assets/specialized.png",
                  reverse=True)

# 8. Administrador
pdf.content_slide("Administrador (DBA)", 
                  "Es una persona que tiene control sobre los datos y los programas que acceden a esos datos.",
                  img_path="assets/admin.png")

# 9. Funciones
pdf.list_slide("Funciones del DBA", [
    "Schema definition: crea los schemas originales.",
    "Definiciones de almacenamiento y acceso de datos.",
    "Modificaciones físicas y de schema.",
    "Permitir autorización para el acceso de datos.",
    "Mantenimiento de rutina (backups, monitoreo)."
])

# 10. Mantenimiento
pdf.list_slide("Mantenimiento de Rutina", [
    "Respaldo de información (Backups).",
    "Verificación de espacio disponible.",
    "Monitoreo de procesos y rendimiento."
])

pdf.output("Database_Presentation.pdf")
print("PDF generado con éxito: Database_Presentation.pdf")
