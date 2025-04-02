import json

class Patient:
    def __init__(self, name, age, weight, temperature, respiration_rate, service, hospital, medicine=None):
        self.name = name
        self.age = age
        self.weight = weight
        self.temperature = temperature
        self.respiration_rate = respiration_rate
        self.service = service
        self.hospital = hospital
        self.medicine = medicine

    def __repr__(self):
        return f"Name: {self.name}, Age: {self.age}, Weight: {self.weight}, Temperature: {self.temperature}, Respiration Rate: {self.respiration_rate}, Service: {self.service}, Hospital: {self.hospital}, Medicine: {self.medicine}"

    def to_dict(self):
        return {
            "name": self.name,
            "age": self.age,
            "weight": self.weight,
            "temperature": self.temperature,
            "respiration_rate": self.respiration_rate,
            "service": self.service,
            "hospital": self.hospital,
            "medicine": self.medicine
        }

    @staticmethod
    def from_dict(data):
        return Patient(
            name=data["name"],
            age=data["age"],
            weight=data["weight"],
            temperature=data["temperature"],
            respiration_rate=data["respiration_rate"],
            service=data["service"],
            hospital=data["hospital"],
            medicine=data.get("medicine")
        )


def load_patients(filename="patients.json"):
    try:
        with open(filename, "r") as file:
            return [Patient.from_dict(patient_data) for patient_data in json.load(file)]
    except FileNotFoundError:
        return []


def save_patients(patients, filename="patients.json"):
    with open(filename, "w") as file:
        json.dump([patient.to_dict() for patient in patients], file, indent=4)


def print_intro():
    print("Welcome to the Doctor's Medical Prescription Suggestion System!")
    print("Rules and Guidelines:")
    print("- Patients falling within certain age ranges will be considered as the same case for medicine suggestion.")
    print("- Otherwise, you will be prompted to enter a new medicine for the new case.")


def categorize_age(age):
    if age <= 12:
        return "0 - 12"
    elif age <= 45:
        return "13 - 45"
    elif age <= 100:
        return "46 - 100"
    else:
        return "100 - Above"


def get_patient_data():
    name = input("Enter patient's name: ")
    age = int(input("Enter patient's age: "))
    weight = float(input("Enter patient's weight (in kg): "))
    temperature = float(input("Enter patient's temperature (in Celsius): "))
    respiration_rate = int(input("Enter patient's respiration rate (breaths per minute): "))
    service = input("Enter patient's service: ")
    hospital = input("Enter patient's hospital: ")
    return name, age, weight, temperature, respiration_rate, service, hospital


def suggest_medicine(patients, new_patient):
    patient_category = categorize_age(new_patient.age)
    for patient in patients:
        if (categorize_age(patient.age) == patient_category and
            patient.service == new_patient.service and
            patient.hospital == new_patient.hospital):
            print(f"Patient {new_patient.name} matches with previous patient {patient.name}.")
            if patient.medicine:
                print(f"Prescribing automatically: {patient.medicine}")
                new_patient.medicine = patient.medicine  # Automatically prescribe
            return
    print("No matching patient found. Prescribing new medicine.")
    new_patient.medicine = input("Enter medicine suggestion for the new patient: ")


def main():
    print_intro()
    patients = load_patients()
    while True:
        start = input("Start using the app? (Y/N): ").upper()
        if start != 'Y':
            break
        name, age, weight, temperature, respiration_rate, service, hospital = get_patient_data()
        new_patient = Patient(name, age, weight, temperature, respiration_rate, service, hospital)
        suggest_medicine(patients, new_patient)
        patients.append(new_patient)
        save_patients(patients)
        print("Patient data recorded successfully.")
        print("Current Patients:")
        for patient in patients:
            print(patient)
        print()

if __name__ == "__main__":
    main()
