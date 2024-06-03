from ..models import MedicationCategory, Medication
from random import randrange, sample

medicine_categories = [ "Pain relievers", "Antibiotics", "Allergy", "Antidepressants", "Blood pressure", "Antifungals", "Cholesterol", "Anxiolytics", "Diabetes", "Antihistamines", "Anesthetics", "Steroids", "Vitamins and Minerals", "Antipsychotics", "Hormonal", "Antimycobacterials", "Analgesics", "Antispasticity", "Genitourinary", "Antiemetics", "Dermatological", "Gastrointestinal" ]

medicine_names = [ "Acetaminophen", "Ibuprofen", "Aspirin", "Lisinopril", "Levothyroxine", "Atorvastatin", "Metformin", "Amlodipine", "Simvastatin", "Omeprazole", "Losartan", "Azithromycin", "Hydrochlorothiazide", "Alprazolam", "Gabapentin", "Sertraline", "Metoprolol", "Escitalopram", "Furosemide", "Prednisone", "Amoxicillin", "Citalopram", "Trazodone", "Cephalexin", "Clonazepam", "Duloxetine", "Venlafaxine", "Fluoxetine", "Pantoprazole", "Warfarin", "Carvedilol", "Tramadol", "Ciprofloxacin", "Meloxicam", "Diazepam", "Lorazepam", "Naproxen", "Fluconazole", "Doxycycline", "Hydrocodone", "Metronidazole", "Tamsulosin", "Ranitidine", "Clonidine", "Bupropion", "Quetiapine", "Amitriptyline", "Mirtazapine", "Benazepril", "Sildenafil", "Valsartan", "Tadalafil", "Esomeprazole", "Memantine", "Cyclobenzaprine", "Buspirone", "Amphetamine", "Risperidone", "Lansoprazole", "Rosuvastatin", "Doxazosin", "Metoclopramide", "Topiramate", "Methotrexate", "Rabeprazole", "Budesonide", "Baclofen", "Clindamycin", "Atomoxetine", "Nortriptyline", "Zolpidem", "Olanzapine", "Hydralazine", "Cyclosporine", "Sulfamethoxazole", "Phenytoin", "Phentermine", "Levetiracetam", "Digoxin", "Perindopril", "Diltiazem", "Phenobarbital", "Lidocaine", "Pregabalin", "Terbinafine", "Memantine", "Carbamazepine", "Gabapentin", "Tolterodine", "Oxcarbazepine", "Duloxetine", "Rivastigmine", "Desvenlafaxine", "Entacapone", "Selegiline", "Galantamine", "Tacrine", "Zaleplon", "Eszopiclone", "Zopiclone", "Ramelteon", "Trazodone", "Quetiapine", "Olanzapine", "Ziprasidone", "Lurasidone", "Aripiprazole", "Paliperidone", "Asenapine", "Cariprazine", "Clozapine", "Chlorpromazine", "Haloperidol", "Fluphenazine", "Perphenazine", "Thioridazine", "Trifluoperazine", "Loxapine", "Molindone", "Pimozide", "Droperidol", "Risperidone", "Olanzapine", "Ziprasidone", "Lurasidone", "Aripiprazole", "Paliperidone", "Asenapine", "Cariprazine", "Brexpiprazole", "Iloperidone", "Sertindole", "Blonanserin", "Lumateperone", "Pimavanserin", "Iloperidone", "Sertindole", "Blonanserin", "Lumateperone", "Pimavanserin", "Alprazolam", "Lorazepam", "Clonazepam", "Diazepam", "Chlordiazepoxide", "Oxazepam", "Temazepam", "Triazolam", "Midazolam", "Estazolam", "Quazepam", "Flurazepam", "Clorazepate", "Prazepam", "Halazepam", "Clobazam", "Clorazepate", "Prazepam", "Halazepam", "Clobazam", "Flunitrazepam", "Nitrazepam", "Fludiazepam", "Loprazolam", "Bromazepam", "Ketazolam", "Pinazepam", "Flutoprazepam", "Difenoxin", "Diphenoxylate", "Loperamide", "Diphenoxylate", "Loperamide", "Eluxadoline", "Codeine", "Hydrocodone", "Oxycodone", "Hydromorphone", "Oxymorphone", "Morphine", "Levorphanol", "Meperidine", "Fentanyl", "Sufentanil", "Remifentanil", "Tramadol", "Tapentadol", "Buprenorphine", "Butorphanol", "Nalbuphine", "Pentazocine", "Dextropropoxyphene", "Dextromethorphan", "Noscapine", "Cough suppressants", "Codeine", "Hydrocodone", "Oxycodone", "Hydromorphone", "Oxymorphone", "Morphine", "Levorphanol", "Meperidine", "Fentanyl", "Sufentanil", "Remifentanil", "Tramadol", "Tapentadol", "Buprenorphine", "Butorphanol", "Nalbuphine", "Pentazocine", "Dextropropoxyphene", "Dextromethorphan" ]

def GenerateMedCategories():
    for category in medicine_categories:
        MedicationCategory.objects.create(category=category)

def GenerateMedicines():
    for medicine in medicine_names:
        f = MedicationCategory.objects.all().first().id
        medication_category_ids = sample(range(f, f + len(medicine_categories)), randrange(1, len(medicine_categories) // 2))

        print(medication_category_ids)

        medication = Medication.objects.create(
            name=medicine,
            cost=randrange(20, 400),
            available=randrange(2),
        )
        
        for medication_category_id in medication_category_ids:
            medication_category = MedicationCategory.objects.get(id=medication_category_id)
            medication.category.add(medication_category)

