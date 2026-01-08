# Dummy User Data Reference

This document contains all the dummy/test user data used in the Aarogyadost Backend API for development and testing purposes.

## 1. Hardcoded Default User

**User ID**: `hardcoded`

### Basic Profile
- **Display Name**: Default (Hardcoded)
- **Age**: 35
- **Gender**: Male
- **Location**: Mumbai, India
- **Created**: Current timestamp
- **Last Active**: Current timestamp

### Health Profile
- **Height**: 175 cm
- **Weight**: 75 kg
- **BMI**: 24.5
- **Blood Type**: O+
- **Biological Age**: 32.0

### Goals
- **Goal ID**: hardcoded_goal_1
- **Type**: fitness
- **Target**: "Improve cardiovascular health"
- **Status**: active

### Data Availability
- ✅ Biomarkers: Available (85% completeness)
- ✅ Medical History: Available
- ✅ Lifestyle: Available
- ❌ AI Interactions: Not available
- ❌ Interventions: Not available

---

## 2. Test User 1 (Complete Dataset)

**User ID**: `test_user_1_29f`

### Basic Profile
- **Display Name**: Test User 1 (29F)
- **Age**: 29
- **Gender**: Female
- **Location**: Bengaluru, India
- **Created**: 2024-07-01T00:00:00Z
- **Last Active**: 2026-01-07T22:39:58Z

### Health Profile
- **Height**: 165 cm
- **Weight**: 58 kg
- **BMI**: 21.3
- **Blood Type**: O+
- **Biological Age**: 27

### Goals
1. **Vitamin Optimization**
   - Goal ID: g1_001
   - Target: "Increase Vitamin D to >30 ng/mL"
   - Start: 2024-07-26, Target: 2024-10-26
   - Status: active

2. **Lipid Management**
   - Goal ID: g1_002
   - Target: "Reduce triglycerides to <150 mg/dL"
   - Start: 2024-07-26, Target: 2024-12-26
   - Status: active

### Preferences
- **Units**: metric
- **Notifications**: enabled
- **Data Sharing**: enabled

---

## 3. Biomarker Data (test_user_1_29f)

### Blood Chemistry
- **Glucose (Fasting)**: 92 mg/dL (Normal: 70-100)
- **HbA1c**: 5.8% (Normal: <5.7%)
- **Total Cholesterol**: 195 mg/dL (Normal: <200)
- **LDL**: 125 mg/dL (Normal: <100)
- **HDL**: 38 mg/dL (Low: Normal >40)
- **Triglycerides**: 269 mg/dL (High: Normal <150)

### Vitamins & Minerals
- **Vitamin D**: 8.25 ng/mL (Deficient: Normal >30)
- **Vitamin B12**: 180 pg/mL (Low: Normal 200-900)
- **Iron**: 65 μg/dL (Normal: 60-170)
- **Ferritin**: 25 ng/mL (Low: Normal 30-150)

### Hormones
- **TSH**: 2.8 mIU/L (Normal: 0.4-4.0)
- **Free T4**: 1.2 ng/dL (Normal: 0.8-1.8)
- **Cortisol (Morning)**: 18 μg/dL (Normal: 6-23)

### Inflammatory Markers
- **CRP**: 2.1 mg/L (Elevated: Normal <1.0)
- **ESR**: 22 mm/hr (Normal: <20)

### Complete Blood Count
- **Hemoglobin**: 11.8 g/dL (Low: Normal 12-15.5)
- **Hematocrit**: 35.2% (Low: Normal 36-46)
- **WBC**: 6800 /μL (Normal: 4500-11000)
- **Platelets**: 285000 /μL (Normal: 150000-450000)

---

## 4. Medical History (test_user_1_29f)

### Conditions
1. **Vitamin D Deficiency**
   - Diagnosed: 2024-07-26
   - Severity: moderate
   - Notes: Level at 8.25 ng/mL, supplementation started

2. **Dyslipidemia**
   - Diagnosed: 2024-07-26
   - Severity: mild
   - Notes: Elevated triglycerides (269 mg/dL), low HDL (38 mg/dL)

### Current Supplements
1. **Vitamin D3**
   - Dosage: 2000 IU daily
   - Started: 2024-07-27
   - Purpose: Correct vitamin D deficiency

2. **Vitamin B12**
   - Dosage: 1000 mcg daily
   - Started: 2024-07-27
   - Purpose: Correct B12 deficiency

3. **Omega-3 Fish Oil**
   - Dosage: 1000 mg twice daily
   - Started: 2024-07-27
   - Purpose: Improve lipid profile, reduce triglycerides

### Family History
- **Diabetes Type 2**: Father (diagnosed at age 55)
- **Hypertension**: Mother (diagnosed at age 50)
- **Heart Disease**: Paternal grandfather (diagnosed at age 65)

---

## 5. Lifestyle Data (test_user_1_29f)

### Sleep Patterns
- **Average Sleep**: 6.5 hours/night
- **Sleep Quality**: 6/10
- **Bedtime**: 11:30 PM
- **Wake Time**: 6:00 AM

### Exercise Routine
- **Frequency**: 4 days/week
- **Primary Activity**: Yoga, Walking
- **Duration**: 45 minutes average
- **Intensity**: Moderate

### Nutrition
- **Diet Type**: Vegetarian
- **Meals/Day**: 3 main + 2 snacks
- **Water Intake**: 2.5 L/day
- **Alcohol**: 1-2 drinks/week

### Stress & Mental Health
- **Stress Level**: 7/10
- **Work Hours**: 9 hours/day
- **Meditation**: 10 minutes/day
- **Social Activities**: 2-3 times/week

---

## 6. Daily Routine Stack (Hardcoded Data)

### Morning Longevity Stack
1. **Vitamin D3 + K2**
   - Dosage: 2000 IU with breakfast
   - Purpose: Bone health

2. **Omega-3 EPA/DHA**
   - Dosage: 2g daily
   - Purpose: Cardiovascular health

### Exercise & Movement
- Zone 2 cardio sessions
- Strength training routine
- Daily walks

### Evening Routine
- Magnesium supplementation
- Sleep optimization protocols

---

## 7. AI Chat Interactions (test_user_1_29f)

### Sample Recommendations Generated
1. **Vitamin D3 Supplementation**
   - Start 2000-4000 IU daily
   - Retest in 8-12 weeks
   - Sun exposure 15-20 minutes midday

2. **Omega-3 Supplementation**
   - High-quality fish oil or algae-based
   - Target EPA/DHA ratio
   - Monitor lipid improvements

3. **Lifestyle Modifications**
   - Improve sleep to 7-8 hours
   - Reduce stress through meditation
   - Increase physical activity

---

## 8. Mock Health Categories (Hardcoded)

### Available Categories
1. **Cardiovascular Health** (Score: 78/100)
2. **Metabolic Health** (Score: 72/100)
3. **Hormonal Balance** (Score: 85/100)
4. **Inflammation Markers** (Score: 65/100)
5. **Nutritional Status** (Score: 70/100)

### Recommended Actions
- Take Vitamin D3 2000 IU daily
- Increase omega-3 intake
- Practice stress management
- Improve sleep quality
- Regular exercise routine

---

## 9. Available Labs & Doctors (Mock Data)

### Labs
- **Thyrocare**: Home collection, Vitamin D3 testing
- **Apollo Diagnostics**: Premium centers, Advanced testing
- **SRL Diagnostics**: Comprehensive panels
- **Dr. Lal PathLabs**: Nationwide network

### Doctors
- **Dr. Sarah Johnson**: Preventive Medicine Specialist
- **Dr. Michael Chen**: Longevity Medicine Expert
- **Dr. Priya Sharma**: Functional Medicine Practitioner

---

## Usage Notes

- **Hardcoded user** is the fallback when no specific user is selected
- **test_user_1_29f** has complete biomarker, lifestyle, and medical history data
- **OCR users** (ocr_user_001_29f, ocr_user_003_31m, ocr_user_004_31m) have real biomarkers extracted from medical reports
- All timestamps use ISO 8601 format
- Biomarker values include normal ranges for reference
- Mock data is designed to demonstrate various health conditions and recommendations

This data is used across all API endpoints for consistent testing and development.

---

## 10. OCR-Extracted Users (Real Medical Data)

### OCR User 1 (29F) - `ocr_user_001_29f`
**Source**: Real medical report from Thyrocare (Women's Advanced Healthcare Package)
**Extracted Biomarkers**: 33 values

#### Key Findings
- **Vitamin D**: 8.25 ng/mL (Deficient - Normal >30)
- **Vitamin B12**: 150 pg/mL (Low - Normal 197-771)
- **Triglycerides**: 269 mg/dL (High - Normal <150)
- **HDL**: 38 mg/dL (Low - Normal >40)
- **LDL**: 124 mg/dL (High - Normal <100)
- **HbA1c**: 4.7% (Normal - <5.7%)
- **TSH**: 3.21 µIU/mL (Normal - 0.54-5.30)

### OCR User 2 (31M) - `ocr_user_003_31m`
**Source**: Real medical report from Thyrocare
**Extracted Biomarkers**: 30 values

#### Key Findings
- **HbA1c**: 4.9% (Normal)
- **Comprehensive metabolic panel**: Available
- **Lipid profile**: Complete
- **Thyroid function**: Normal range

### OCR User 3 (31M) - `ocr_user_004_31m`
**Source**: Real medical report from Thyrocare
**Extracted Biomarkers**: 29 values

#### Key Findings
- **Complete blood count**: Available
- **Liver function tests**: Normal
- **Kidney function**: Normal
- **Metabolic markers**: Complete panel

### OCR Data Advantages
- ✅ **Real medical values** from actual lab reports
- ✅ **Comprehensive panels** with 29-33 biomarkers each
- ✅ **Authentic ranges** and reference values
- ✅ **Clinical context** from actual patient reports
- ✅ **Diverse profiles** across age groups and genders
