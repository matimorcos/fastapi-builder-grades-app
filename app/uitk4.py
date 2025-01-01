import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base
from core.schemas import Student, PracticalWork, Qualification
from solution.services.mssgs import send_email
from decouple import config

FIXED_EMAIL = "useremail@smtp.com"

# cfg de la base de datos
DATABASE_URL = config('DATABASE_URL')
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
metadata = MetaData()
metadata.reflect(bind=engine)

class PracticalWorkApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Practical Work Grading")
        self.geometry("400x500")

        # variables para los dropdowns
        self.student_var = tk.StringVar()
        self.pw_var = tk.StringVar()
        self.achievement_g1_var = tk.StringVar()
        self.achievement_g2_var = tk.StringVar()
        self.achievement_g3_var = tk.StringVar()

        # labels y dropdowns
        tk.Label(self, text="Select Student:").pack(pady=5)
        self.student_dropdown = ttk.Combobox(self, textvariable=self.student_var)
        self.student_dropdown.pack(pady=5)

        tk.Label(self, text="Select Practical Work:").pack(pady=5)
        self.pw_dropdown = ttk.Combobox(self, textvariable=self.pw_var)
        self.pw_dropdown.pack(pady=5)

        tk.Label(self, text="Select Achievement for Guideline 1:").pack(pady=5)
        self.achievement_g1_dropdown = ttk.Combobox(self, textvariable=self.achievement_g1_var)
        self.achievement_g1_dropdown.pack(pady=5)

        tk.Label(self, text="Select Achievement for Guideline 2:").pack(pady=5)
        self.achievement_g2_dropdown = ttk.Combobox(self, textvariable=self.achievement_g2_var)
        self.achievement_g2_dropdown.pack(pady=5)

        tk.Label(self, text="Select Achievement for Guideline 3:").pack(pady=5)
        self.achievement_g3_dropdown = ttk.Combobox(self, textvariable=self.achievement_g3_var)
        self.achievement_g3_dropdown.pack(pady=5)

        # button para cargar la calificación en la DB
        self.submit_button = tk.Button(self, text="Submit Grade", command=self.submit_grade)
        self.submit_button.pack(pady=20)

        # cargar datos al iniciarse
        self.load_students()
        self.load_practical_works()

        # Cdo se selecciona un PW, cargar los achievements correspondientes
        self.pw_dropdown.bind("<<ComboboxSelected>>", self.on_pw_change)

    def load_students(self):
        """Carga los estudiantes en el dropdown."""
        students = session.query(Student).all()
        student_options = [f"{student.student_id} - {student.student_names}" for student in students]
        self.student_dropdown['values'] = student_options

    def load_practical_works(self):
        """Carga los Practical Works en el dropdown."""
        practical_works = session.query(PracticalWork).all()
        pw_options = [f"{pw.pw_id} - {pw.subject_id}" for pw in practical_works]
        self.pw_dropdown['values'] = pw_options

    def load_achievements(self, pw_id, guideline_number):
        """Carga los achievements de un guideline específico en el dropdown correspondiente."""
        practical_work = session.query(PracticalWork).filter_by(pw_id=pw_id).first()

        if practical_work:
            achievements = []
            for i in range(1, 4):  # hay 3 achievements por cada guideline
                achievement_description = getattr(practical_work, f'achievement_{i}_g{guideline_number}_description', None)
                if achievement_description:
                    achievements.append(achievement_description)

            # asigna las opciones disponibles al dropdown correspondiente
            if guideline_number == 1:
                self.achievement_g1_dropdown['values'] = achievements
            elif guideline_number == 2:
                self.achievement_g2_dropdown['values'] = achievements
            elif guideline_number == 3:
                self.achievement_g3_dropdown['values'] = achievements

    def on_pw_change(self, event):
        """Cuando se selecciona un Practical Work, se cargan los achievements de cada guideline."""
        pw_id = self.pw_var.get().split(" - ")[0]

        # Cargar achievements para cada guideline
        self.load_achievements(pw_id, 1)
        self.load_achievements(pw_id, 2)
        self.load_achievements(pw_id, 3)

    def submit_grade(self):
        """Envía la calificación a la base de datos."""
        try:
            # obtener el ID del estudiante y Practical Work
            student_selection = self.student_var.get().split(" - ")
            student_id = student_selection[0]
            student_names = student_selection[1] if len(student_selection) > 1 else "Unknown Student"

            pw_id = self.pw_var.get().split(" - ")[0]

            # verificar si el estudiante ya ha sido calificado para este PW
            existing_qualification = session.query(Qualification).filter_by(student_id=student_id, pw_id=pw_id).first()
            if existing_qualification:
                messagebox.showerror("Error", "This student has already been graded for this practical work.")
                return

            # Obtener los achievements seleccionados para cada guideline
            achievement_g1 = self.achievement_g1_var.get()
            achievement_g2 = self.achievement_g2_var.get()
            achievement_g3 = self.achievement_g3_var.get()

            # obtener el Practical Work para calcular los scores
            practical_work = session.query(PracticalWork).filter_by(pw_id=pw_id).first()

            # inicializar el scoring y las descripciones
            score_g1 = 0
            score_g2 = 0
            score_g3 = 0
            description_g1 = ""
            description_g2 = ""
            description_g3 = ""

            # determinar cuál achievement fue seleccionado para asignar el score y la descripción correspondiente
            if achievement_g1 == practical_work.achievement_1_g1_description:
                score_g1 = practical_work.achievement_1_g1_score
                description_g1 = practical_work.achievement_1_g1_description
            elif achievement_g1 == practical_work.achievement_2_g1_description:
                score_g1 = practical_work.achievement_2_g1_score
                description_g1 = practical_work.achievement_2_g1_description
            elif achievement_g1 == practical_work.achievement_3_g1_description:
                score_g1 = practical_work.achievement_3_g1_score
                description_g1 = practical_work.achievement_3_g1_description

            if achievement_g2 == practical_work.achievement_1_g2_description:
                score_g2 = practical_work.achievement_1_g2_score
                description_g2 = practical_work.achievement_1_g2_description
            elif achievement_g2 == practical_work.achievement_2_g2_description:
                score_g2 = practical_work.achievement_2_g2_score
                description_g2 = practical_work.achievement_2_g2_description
            elif achievement_g2 == practical_work.achievement_3_g2_description:
                score_g2 = practical_work.achievement_3_g2_score
                description_g2 = practical_work.achievement_3_g2_description

            if achievement_g3 == practical_work.achievement_1_g3_description:
                score_g3 = practical_work.achievement_1_g3_score
                description_g3 = practical_work.achievement_1_g3_description
            elif achievement_g3 == practical_work.achievement_2_g3_description:
                score_g3 = practical_work.achievement_2_g3_score
                description_g3 = practical_work.achievement_2_g3_description
            elif achievement_g3 == practical_work.achievement_3_g3_description:
                score_g3 = practical_work.achievement_3_g3_score
                description_g3 = practical_work.achievement_3_g3_description

            # score total
            total_score = score_g1 + score_g2 + score_g3

            # crear entrada en la tabla Qualifications con la descripción de los achievements
            qualification = Qualification(
                student_id=student_id,
                pw_id=pw_id,
                score=total_score,
                achievements_description=f"{description_g1}, {description_g2}, {description_g3}"
            )
            session.add(qualification)
            session.commit()

            # el cuerpo del email
            email_body = (
                f"Hola! {student_names} esta es una devolución preliminar de tu ultimo trabajo practico en la materia Concursos y Quiebras.\n\n"
                f"{description_g1}, {description_g2}, {description_g3}\n\n"
                "Tu calificación final se encuentra pendiente!. No respondas este email."
            )

            # enviar el correo
            FIXED_EMAIL = "useremail@smtp.com"  # define tu email fijo
            send_email("New Qualification Submitted", FIXED_EMAIL, email_body)

            messagebox.showinfo("Success", "Grade submitted successfully.")

        except Exception as e:
            session.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    app = PracticalWorkApp()
    app.mainloop()