"""
MEDIEXPERT
Knowledge Base

Contains:
1. Symptoms
2. Medical conditions
3. Rule definitions
4. Educational guidance
5. Red-flag information

This is an educational rule-based knowledge base.
It is NOT intended for real medical diagnosis.
"""

# ============================================================
# SYMPTOMS
# ============================================================

SYMPTOMS = [
    "fever",
    "cough",
    "dry_cough",
    "sore_throat",
    "runny_nose",
    "sneezing",
    "itchy_eyes",
    "headache",
    "severe_headache",
    "light_sensitivity",
    "nausea",
    "vomiting",
    "diarrhea",
    "stomach_pain",
    "fatigue",
    "body_aches",
    "shortness_of_breath",
    "chest_discomfort",
    "wheezing",
    "dizziness",
    "increased_thirst",
    "frequent_urination",
    "burning_urination",
    "loss_of_appetite",
    "sinus_pressure",
    "facial_pain",
    "mucus",
    "chills",
    "rapid_heartbeat",
    "dehydration_signs",
    "cough_with_mucus",
    "persistent_cough",
    "thirst",
    "weakness",
    "blurred_vision",
    "high_blood_pressure_reading",
    "stress",
    "neck_pain",
    "abdominal_cramps",
    "food_intake_before_symptoms",
]


# ============================================================
# USER-FRIENDLY SYMPTOM LABELS
# ============================================================

SYMPTOM_LABELS = {
    "fever": "Fever",
    "cough": "Cough",
    "dry_cough": "Dry Cough",
    "sore_throat": "Sore Throat",
    "runny_nose": "Runny Nose",
    "sneezing": "Sneezing",
    "itchy_eyes": "Itchy Eyes",
    "headache": "Headache",
    "severe_headache": "Severe Headache",
    "light_sensitivity": "Light Sensitivity",
    "nausea": "Nausea",
    "vomiting": "Vomiting",
    "diarrhea": "Diarrhea",
    "stomach_pain": "Stomach Pain",
    "fatigue": "Fatigue",
    "body_aches": "Body Aches",
    "shortness_of_breath": "Shortness of Breath",
    "chest_discomfort": "Chest Discomfort",
    "wheezing": "Wheezing",
    "dizziness": "Dizziness",
    "increased_thirst": "Increased Thirst",
    "frequent_urination": "Frequent Urination",
    "burning_urination": "Burning Urination",
    "loss_of_appetite": "Loss of Appetite",
    "sinus_pressure": "Sinus Pressure",
    "facial_pain": "Facial Pain",
    "mucus": "Mucus",
    "chills": "Chills",
    "rapid_heartbeat": "Rapid Heartbeat",
    "dehydration_signs": "Signs of Dehydration",
    "cough_with_mucus": "Cough With Mucus",
    "persistent_cough": "Persistent Cough",
    "thirst": "Thirst",
    "weakness": "Weakness",
    "blurred_vision": "Blurred Vision",
    "high_blood_pressure_reading": "High Blood Pressure Reading",
    "stress": "Stress",
    "neck_pain": "Neck Pain",
    "abdominal_cramps": "Abdominal Cramps",
    "food_intake_before_symptoms": "Recent Food Intake Before Symptoms",
}


# ============================================================
# KNOWLEDGE BASE
# ============================================================
#
# Each rule contains:
#
# id          -> unique rule identifier
# condition   -> possible condition
# required    -> symptoms that strongly support the rule
# optional    -> additional supporting symptoms
# guidance    -> safe educational guidance
#
# Match score is calculated by the inference engine.
# ============================================================

KNOWLEDGE_BASE = [

    # --------------------------------------------------------
    # COMMON COLD
    # --------------------------------------------------------

    {
        "id": "R001",
        "condition": "Common Cold",
        "required": [
            "runny_nose",
            "sore_throat",
            "cough"
        ],
        "optional": [
            "sneezing",
            "fatigue",
            "headache"
        ],
        "guidance": "Rest, maintain hydration, and monitor how symptoms develop. Consider professional advice if symptoms are severe or persistent."
    },

    {
        "id": "R002",
        "condition": "Common Cold",
        "required": [
            "runny_nose",
            "sneezing",
            "sore_throat"
        ],
        "optional": [
            "cough",
            "fatigue"
        ],
        "guidance": "Rest and maintain adequate fluid intake. Seek medical advice if symptoms become unusually severe."
    },


    # --------------------------------------------------------
    # INFLUENZA
    # --------------------------------------------------------

    {
        "id": "R003",
        "condition": "Influenza",
        "required": [
            "fever",
            "cough",
            "body_aches",
            "fatigue"
        ],
        "optional": [
            "chills",
            "headache",
            "sore_throat"
        ],
        "guidance": "Rest and maintain adequate hydration. Influenza-like symptoms can become serious, especially when breathing problems develop."
    },

    {
        "id": "R004",
        "condition": "Influenza",
        "required": [
            "fever",
            "body_aches",
            "chills"
        ],
        "optional": [
            "cough",
            "fatigue",
            "headache"
        ],
        "guidance": "Rest, hydrate, and monitor symptoms. Professional medical evaluation may be appropriate if symptoms are severe."
    },


    # --------------------------------------------------------
    # MIGRAINE
    # --------------------------------------------------------

    {
        "id": "R005",
        "condition": "Migraine",
        "required": [
            "severe_headache",
            "nausea",
            "light_sensitivity"
        ],
        "optional": [
            "dizziness",
            "neck_pain"
        ],
        "guidance": "Resting in a quiet environment and maintaining hydration may be helpful. Severe or unusual headaches should be professionally evaluated."
    },

    {
        "id": "R006",
        "condition": "Migraine",
        "required": [
            "severe_headache",
            "light_sensitivity"
        ],
        "optional": [
            "nausea",
            "dizziness"
        ],
        "guidance": "Reduce exposure to bright light and rest. Seek professional assessment for a new, sudden, or unusually severe headache."
    },


    # --------------------------------------------------------
    # FOOD POISONING
    # --------------------------------------------------------

    {
        "id": "R007",
        "condition": "Food Poisoning",
        "required": [
            "vomiting",
            "diarrhea",
            "stomach_pain"
        ],
        "optional": [
            "fever",
            "abdominal_cramps",
            "food_intake_before_symptoms"
        ],
        "guidance": "Maintain hydration and monitor for dehydration. Seek professional medical care if symptoms are severe or persistent."
    },

    {
        "id": "R008",
        "condition": "Food Poisoning",
        "required": [
            "diarrhea",
            "abdominal_cramps",
            "food_intake_before_symptoms"
        ],
        "optional": [
            "vomiting",
            "nausea",
            "fever"
        ],
        "guidance": "Maintain fluid intake and monitor symptoms. Professional care may be necessary when dehydration or severe symptoms occur."
    },


    # --------------------------------------------------------
    # GASTROENTERITIS
    # --------------------------------------------------------

    {
        "id": "R009",
        "condition": "Gastroenteritis",
        "required": [
            "diarrhea",
            "vomiting",
            "stomach_pain"
        ],
        "optional": [
            "nausea",
            "fever",
            "weakness"
        ],
        "guidance": "Focus on adequate hydration and rest. Seek medical care if symptoms are severe, prolonged, or accompanied by significant dehydration."
    },

    {
        "id": "R010",
        "condition": "Gastroenteritis",
        "required": [
            "diarrhea",
            "stomach_pain",
            "nausea"
        ],
        "optional": [
            "vomiting",
            "fever",
            "weakness"
        ],
        "guidance": "Maintain hydration and monitor symptoms. Medical evaluation is recommended when symptoms become severe."
    },


    # --------------------------------------------------------
    # ALLERGY
    # --------------------------------------------------------

    {
        "id": "R011",
        "condition": "Allergy",
        "required": [
            "sneezing",
            "runny_nose",
            "itchy_eyes"
        ],
        "optional": [
            "cough",
            "sinus_pressure"
        ],
        "guidance": "Avoid known triggers when possible and monitor symptoms. Seek professional care if breathing difficulties occur."
    },

    {
        "id": "R012",
        "condition": "Allergy",
        "required": [
            "sneezing",
            "itchy_eyes"
        ],
        "optional": [
            "runny_nose",
            "sinus_pressure"
        ],
        "guidance": "Reducing exposure to known triggers may help. Seek professional evaluation for significant or persistent symptoms."
    },


    # --------------------------------------------------------
    # ASTHMA
    # --------------------------------------------------------

    {
        "id": "R013",
        "condition": "Asthma Pattern",
        "required": [
            "wheezing",
            "shortness_of_breath"
        ],
        "optional": [
            "cough",
            "chest_discomfort"
        ],
        "guidance": "Breathing difficulty should be taken seriously. Follow an existing clinician-provided asthma plan if applicable and seek professional assessment."
    },

    {
        "id": "R014",
        "condition": "Asthma Pattern",
        "required": [
            "wheezing",
            "cough",
            "chest_discomfort"
        ],
        "optional": [
            "shortness_of_breath"
        ],
        "guidance": "Breathing symptoms should be professionally evaluated, particularly when they are new or worsening."
    },


    # --------------------------------------------------------
    # DEHYDRATION
    # --------------------------------------------------------

    {
        "id": "R015",
        "condition": "Dehydration Pattern",
        "required": [
            "dizziness",
            "dehydration_signs",
            "weakness"
        ],
        "optional": [
            "vomiting",
            "diarrhea",
            "thirst"
        ],
        "guidance": "Adequate fluid intake is important. Severe dehydration signs require prompt professional medical attention."
    },

    {
        "id": "R016",
        "condition": "Dehydration Pattern",
        "required": [
            "thirst",
            "dizziness"
        ],
        "optional": [
            "weakness",
            "dehydration_signs"
        ],
        "guidance": "Maintain appropriate fluid intake and monitor symptoms. Seek medical attention if dehydration becomes severe."
    },


    # --------------------------------------------------------
    # COVID-LIKE RESPIRATORY INFECTION
    # --------------------------------------------------------

    {
        "id": "R017",
        "condition": "COVID-like Respiratory Infection Pattern",
        "required": [
            "fever",
            "cough",
            "fatigue"
        ],
        "optional": [
            "sore_throat",
            "body_aches",
            "shortness_of_breath"
        ],
        "guidance": "Respiratory infections can have overlapping symptoms. Consider appropriate testing and professional medical guidance."
    },

    {
        "id": "R018",
        "condition": "COVID-like Respiratory Infection Pattern",
        "required": [
            "cough",
            "fatigue",
            "sore_throat"
        ],
        "optional": [
            "fever",
            "body_aches"
        ],
        "guidance": "Monitor respiratory symptoms and consider professional evaluation or appropriate testing."
    },


    # --------------------------------------------------------
    # BRONCHITIS
    # --------------------------------------------------------

    {
        "id": "R019",
        "condition": "Bronchitis Pattern",
        "required": [
            "persistent_cough",
            "cough_with_mucus"
        ],
        "optional": [
            "chest_discomfort",
            "fatigue",
            "fever"
        ],
        "guidance": "Persistent cough should be monitored. Professional assessment is appropriate when symptoms are prolonged or breathing becomes difficult."
    },

    {
        "id": "R020",
        "condition": "Bronchitis Pattern",
        "required": [
            "cough",
            "cough_with_mucus",
            "chest_discomfort"
        ],
        "optional": [
            "fatigue",
            "fever"
        ],
        "guidance": "Monitor respiratory symptoms and seek professional advice if cough persists or breathing difficulty develops."
    },


    # --------------------------------------------------------
    # SINUSITIS
    # --------------------------------------------------------

    {
        "id": "R021",
        "condition": "Sinusitis Pattern",
        "required": [
            "sinus_pressure",
            "facial_pain",
            "mucus"
        ],
        "optional": [
            "headache",
            "runny_nose",
            "fever"
        ],
        "guidance": "Persistent sinus symptoms may require professional evaluation, especially when facial pain or fever is significant."
    },

    {
        "id": "R022",
        "condition": "Sinusitis Pattern",
        "required": [
            "sinus_pressure",
            "headache",
            "runny_nose"
        ],
        "optional": [
            "facial_pain",
            "mucus"
        ],
        "guidance": "Monitor symptoms and seek professional assessment if symptoms persist or become severe."
    },


    # --------------------------------------------------------
    # PNEUMONIA PATTERN
    # --------------------------------------------------------

    {
        "id": "R023",
        "condition": "Pneumonia Pattern",
        "required": [
            "fever",
            "cough",
            "shortness_of_breath"
        ],
        "optional": [
            "chest_discomfort",
            "fatigue",
            "body_aches"
        ],
        "guidance": "This symptom combination can require medical assessment. Seek professional care, particularly when breathing difficulty is present."
    },

    {
        "id": "R024",
        "condition": "Pneumonia Pattern",
        "required": [
            "fever",
            "cough_with_mucus",
            "chest_discomfort"
        ],
        "optional": [
            "shortness_of_breath",
            "fatigue"
        ],
        "guidance": "Respiratory symptoms with fever and chest discomfort warrant professional medical assessment."
    },


    # --------------------------------------------------------
    # URINARY TRACT INFECTION
    # --------------------------------------------------------

    {
        "id": "R025",
        "condition": "Urinary Tract Infection Pattern",
        "required": [
            "burning_urination",
            "frequent_urination"
        ],
        "optional": [
            "fever",
            "stomach_pain",
            "weakness"
        ],
        "guidance": "Urinary symptoms should be evaluated by a healthcare professional, particularly when fever or worsening symptoms occur."
    },

    {
        "id": "R026",
        "condition": "Urinary Tract Infection Pattern",
        "required": [
            "burning_urination",
            "frequent_urination",
            "stomach_pain"
        ],
        "optional": [
            "fever"
        ],
        "guidance": "Professional evaluation is recommended for persistent urinary symptoms."
    },


    # --------------------------------------------------------
    # DIABETES WARNING PATTERN
    # --------------------------------------------------------

    {
        "id": "R027",
        "condition": "Diabetes Warning Pattern",
        "required": [
            "increased_thirst",
            "frequent_urination",
            "weakness"
        ],
        "optional": [
            "blurred_vision",
            "fatigue"
        ],
        "guidance": "This combination can occur with several conditions, including blood-glucose problems. Professional evaluation and appropriate testing are recommended."
    },

    {
        "id": "R028",
        "condition": "Diabetes Warning Pattern",
        "required": [
            "increased_thirst",
            "frequent_urination",
            "blurred_vision"
        ],
        "optional": [
            "fatigue",
            "weakness"
        ],
        "guidance": "These symptoms warrant professional medical evaluation and appropriate blood-glucose testing."
    },


    # --------------------------------------------------------
    # HYPERTENSION WARNING PATTERN
    # --------------------------------------------------------

    {
        "id": "R029",
        "condition": "Hypertension Warning Pattern",
        "required": [
            "high_blood_pressure_reading"
        ],
        "optional": [
            "headache",
            "dizziness",
            "blurred_vision"
        ],
        "guidance": "A high blood-pressure reading should be discussed with a healthcare professional. Extremely high readings with concerning symptoms require urgent care."
    },

    {
        "id": "R030",
        "condition": "Hypertension Warning Pattern",
        "required": [
            "high_blood_pressure_reading",
            "headache"
        ],
        "optional": [
            "dizziness",
            "blurred_vision"
        ],
        "guidance": "Blood pressure should be measured correctly and discussed with a qualified healthcare professional."
    },


    # --------------------------------------------------------
    # GENERAL RESPIRATORY PATTERN
    # --------------------------------------------------------

    {
        "id": "R031",
        "condition": "Respiratory Infection Pattern",
        "required": [
            "cough",
            "sore_throat"
        ],
        "optional": [
            "fever",
            "runny_nose",
            "fatigue"
        ],
        "guidance": "Respiratory symptoms can have multiple causes. Monitor symptoms and seek professional advice if they persist or worsen."
    },

    # --------------------------------------------------------
    # GENERAL VIRAL PATTERN
    # --------------------------------------------------------

    {
        "id": "R032",
        "condition": "Viral Illness Pattern",
        "required": [
            "fever",
            "fatigue",
            "body_aches"
        ],
        "optional": [
            "headache",
            "cough",
            "sore_throat"
        ],
        "guidance": "These symptoms can occur with many viral illnesses. Rest and hydration may be helpful while monitoring the course of symptoms."
    },

    # --------------------------------------------------------
    # HEADACHE PATTERN
    # --------------------------------------------------------

    {
        "id": "R033",
        "condition": "Tension Headache Pattern",
        "required": [
            "headache",
            "neck_pain",
            "stress"
        ],
        "optional": [
            "fatigue"
        ],
        "guidance": "Stress-related headaches have many possible causes. Rest and appropriate professional assessment may be useful if headaches persist."
    },

    # --------------------------------------------------------
    # GASTROINTESTINAL PATTERN
    # --------------------------------------------------------

    {
        "id": "R034",
        "condition": "Gastrointestinal Distress Pattern",
        "required": [
            "stomach_pain",
            "nausea"
        ],
        "optional": [
            "vomiting",
            "diarrhea",
            "loss_of_appetite"
        ],
        "guidance": "Gastrointestinal symptoms can have many causes. Maintain appropriate hydration and seek professional advice if symptoms are severe or persistent."
    },

    # --------------------------------------------------------
    # FATIGUE / WEAKNESS PATTERN
    # --------------------------------------------------------

    {
        "id": "R035",
        "condition": "Fatigue / Weakness Pattern",
        "required": [
            "fatigue",
            "weakness"
        ],
        "optional": [
            "dizziness",
            "loss_of_appetite"
        ],
        "guidance": "Fatigue and weakness are nonspecific symptoms with many possible causes. Persistent symptoms should be evaluated professionally."
    },

    # --------------------------------------------------------
    # ADDITIONAL RULES
    # --------------------------------------------------------

    {
        "id": "R036",
        "condition": "Respiratory Allergy Pattern",
        "required": [
            "sneezing",
            "runny_nose",
            "cough"
        ],
        "optional": [
            "itchy_eyes",
            "sinus_pressure"
        ],
        "guidance": "Allergic respiratory symptoms can overlap with infections. Avoid known triggers and consider professional advice when symptoms persist."
    },

    {
        "id": "R037",
        "condition": "Flu-like Illness Pattern",
        "required": [
            "fever",
            "headache",
            "body_aches"
        ],
        "optional": [
            "fatigue",
            "chills",
            "cough"
        ],
        "guidance": "This is a general educational pattern and does not identify a specific infection. Monitor symptoms and seek professional advice when appropriate."
    },

    {
        "id": "R038",
        "condition": "Respiratory Irritation Pattern",
        "required": [
            "dry_cough",
            "sore_throat"
        ],
        "optional": [
            "cough",
            "chest_discomfort"
        ],
        "guidance": "Respiratory irritation has multiple possible causes. Persistent or worsening symptoms should be assessed professionally."
    },

    {
        "id": "R039",
        "condition": "Dehydration Risk Pattern",
        "required": [
            "vomiting",
            "diarrhea",
            "dizziness"
        ],
        "optional": [
            "weakness",
            "dehydration_signs"
        ],
        "guidance": "Vomiting and diarrhea can cause significant fluid loss. Monitor for dehydration and seek professional care if severe."
    },

    {
        "id": "R040",
        "condition": "Metabolic Warning Pattern",
        "required": [
            "increased_thirst",
            "frequent_urination"
        ],
        "optional": [
            "weakness",
            "blurred_vision",
            "fatigue"
        ],
        "guidance": "Persistent thirst and frequent urination can have multiple causes and warrant professional assessment."
    },

]


# ============================================================
# RED FLAGS
# ============================================================

RED_FLAGS = [
    {
        "title": "Severe difficulty breathing",
        "description": "Significant or rapidly worsening breathing difficulty requires urgent professional medical attention."
    },
    {
        "title": "Severe chest pain",
        "description": "Severe or unexplained chest pain should be treated as a potentially urgent symptom."
    },
    {
        "title": "Loss of consciousness",
        "description": "Fainting or loss of consciousness requires appropriate medical evaluation."
    },
    {
        "title": "Severe dehydration",
        "description": "Severe dehydration, especially with persistent vomiting or diarrhea, can require urgent care."
    },
    {
        "title": "Confusion",
        "description": "New or severe confusion can be a medical emergency."
    },
    {
        "title": "Sudden weakness",
        "description": "Sudden unexplained weakness requires prompt professional assessment."
    },
    {
        "title": "Rapidly worsening symptoms",
        "description": "Symptoms that rapidly become worse should be evaluated by a healthcare professional."
    },
]


# ============================================================
# KNOWLEDGE BASE STATISTICS
# ============================================================

KNOWLEDGE_STATS = {
    "conditions": len(set(rule["condition"] for rule in KNOWLEDGE_BASE)),
    "symptoms": len(SYMPTOMS),
    "rules": len(KNOWLEDGE_BASE),
}