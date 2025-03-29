import spacy
from fuzzywuzzy import process

class ChatBot:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")  # Ensure spaCy model is loaded
        self.responses = {
            "greeting": "Hello! How can I assist you today?",
            "fallback": "I'm sorry, I didn't understand that. Can you please rephrase?",
            "goodbye": "Goodbye! Have a great day!",
        }

    def get_response(self, user_input):
        user_input = user_input.lower().strip()

        if any(greet in user_input for greet in ["hello", "hi", "hey"]):
            return self.responses["greeting"]

        doc = self.nlp(user_input)
        keywords = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]

        # Matching user input with available queries
        query_map = {
            "doctor": self.handle_doctor_query,
            "appointment": self.handle_appointment_query,
            "department": self.handle_department_query,
            "medicine": self.handle_medicine_query,
            "lab test": self.handle_lab_test_query,
            "radio test": self.handle_radio_test_query,
        }

        matched_query, score = process.extractOne(" ".join(keywords), query_map.keys())
        if score > 70:
            if matched_query == "doctor":
                return self.handle_doctor_query(" ".join(keywords))
            elif matched_query == "appointment":
                return self.handle_appointment_query(" ".join(keywords))
            elif matched_query == "department":
                return self.handle_department_query()
            elif matched_query == "medicine":
                return self.handle_medicine_query(" ".join(keywords))
            elif matched_query == "lab test":
                return self.handle_lab_test_query(" ".join(keywords))
            elif matched_query == "radio test":
                return self.handle_radio_test_query(" ".join(keywords))

        return self.responses["fallback"]

    def handle_doctor_query(self, department_name):
        from .models import Doctor, Departments
        department = Departments.objects.filter(specialization_name__icontains=department_name).first()
        if department:
            doctors = Doctor.objects.filter(fk_dep=department)
            if doctors.exists():
                return "Doctors in {}:\n{}".format(
                    department.specialization_name, "\n".join(f"- {doc.fk_user.username}" for doc in doctors)
                )
            return f"No doctors found in {department.specialization_name}."
        return "Department not found."

    def handle_appointment_query(self, patient_id):
        from .models import Appointment, Patient
        patient = Patient.objects.filter(fk_user__username=patient_id).first()
        if patient:
            appointments = Appointment.objects.filter(patient=patient)
            if appointments.exists():
                return "Appointments for {}:\n{}".format(
                    patient.fk_user.username,
                    "\n".join(f"- Dr. {app.doctor.fk_user.username} on {app.day}" for app in appointments)
                )
            return f"No appointments found for {patient.fk_user.username}."
        return "Patient not found."

    def handle_department_query(self):
        from .models import Departments
        departments = Departments.objects.all()
        if departments.exists():
            return "Available departments:\n" + "\n".join(f"- {dep.specialization_name}" for dep in departments)
        return "No departments found."

    def handle_medicine_query(self, medicine_name):
        from .models import Med
        medicines = Med.objects.filter(medicine_name__medicine_name__icontains=medicine_name)
        if medicines.exists():
            return "Medicines matching '{}':\n{}".format(
                medicine_name,
                "\n".join(f"- {med.medicine_name.medicine_name} (Batch: {med.batch_no}, Expiry: {med.expiry_date})" for med in medicines)
            )
        return f"No medicines found matching '{medicine_name}'."

    def handle_lab_test_query(self, test_name):
        from .models import LabTest
        tests = LabTest.objects.filter(test_name__icontains=test_name)
        if tests.exists():
            return "Lab tests matching '{}':\n{}".format(
                test_name,
                "\n".join(f"- {test.get_test_name_display()} (Price: {test.price})" for test in tests)
            )
        return f"No lab tests found matching '{test_name}'."

    def handle_radio_test_query(self, test_name):
        from .models import RadioTest
        tests = RadioTest.objects.filter(test_name__icontains=test_name)
        if tests.exists():
            return "Radiology tests matching '{}':\n{}".format(
                test_name,
                "\n".join(f"- {test.get_test_name_display()} (Price: {test.price})" for test in tests)
            )
        return f"No radiology tests found matching '{test_name}'."
