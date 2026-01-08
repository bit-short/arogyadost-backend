"""
Compute derived health data for OCR users.
Generates conditions, supplements, goals, computed biomarkers, and biological age.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from app.database import SessionLocal
from app.models.db_models import User, Biomarker, MedicalHistory, Goal


class HealthDataComputer:
    """Compute derived health data from biomarkers."""
    
    def __init__(self):
        self.db = SessionLocal()
    
    def compute_all_for_user(self, user_id: str) -> Dict[str, Any]:
        """Run all computations for a user."""
        results = {
            'user_id': user_id,
            'computed_biomarkers': self.compute_biomarkers(user_id),
            'conditions': self.detect_conditions(user_id),
            'supplements': self.recommend_supplements(user_id),
            'goals': self.generate_goals(user_id),
            'biological_age': self.compute_biological_age(user_id)
        }
        return results
    
    def compute_biomarkers(self, user_id: str) -> List[Dict]:
        """Compute derived biomarkers (ratios, eGFR, etc.)."""
        biomarkers = {b.name: b.value for b in self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()}
        user = self.db.query(User).filter(User.id == user_id).first()
        computed = []
        
        # HDL/LDL Ratio
        if 'hdl' in biomarkers and 'ldl' in biomarkers and biomarkers['ldl'] > 0:
            ratio = round(biomarkers['hdl'] / biomarkers['ldl'], 2)
            computed.append({
                'name': 'hdl_ldl_ratio',
                'value': ratio,
                'unit': 'ratio',
                'normal_range': '>0.4',
                'status': 'normal' if ratio > 0.4 else 'low'
            })
        
        # Trig/HDL Ratio
        if 'triglycerides' in biomarkers and 'hdl' in biomarkers and biomarkers['hdl'] > 0:
            ratio = round(biomarkers['triglycerides'] / biomarkers['hdl'], 2)
            computed.append({
                'name': 'trig_hdl_ratio',
                'value': ratio,
                'unit': 'ratio',
                'normal_range': '<3.0',
                'status': 'normal' if ratio < 3.0 else 'high'
            })
        
        # eGFR (CKD-EPI formula simplified)
        if 'creatinine' in biomarkers and user:
            cr = biomarkers['creatinine']
            age = user.age or 30
            is_female = user.gender == 'F'
            
            # Simplified CKD-EPI
            if is_female:
                egfr = 144 * (cr / 0.7) ** (-0.329 if cr <= 0.7 else -1.209) * (0.993 ** age)
            else:
                egfr = 141 * (cr / 0.9) ** (-0.411 if cr <= 0.9 else -1.209) * (0.993 ** age)
            
            computed.append({
                'name': 'egfr',
                'value': round(egfr, 1),
                'unit': 'mL/min/1.73m²',
                'normal_range': '>90',
                'status': 'normal' if egfr >= 90 else 'low' if egfr >= 60 else 'critical'
            })
        
        # Average Blood Glucose from HbA1c
        if 'hba1c' in biomarkers:
            abg = round(28.7 * biomarkers['hba1c'] - 46.7, 1)
            computed.append({
                'name': 'average_blood_glucose',
                'value': abg,
                'unit': 'mg/dL',
                'normal_range': '70-140',
                'status': 'normal' if 70 <= abg <= 140 else 'high' if abg > 140 else 'low'
            })
        
        # Save computed biomarkers to DB
        for cb in computed:
            existing = self.db.query(Biomarker).filter(
                Biomarker.user_id == user_id,
                Biomarker.name == cb['name']
            ).first()
            
            if existing:
                existing.value = cb['value']
                existing.status = cb['status']
            else:
                self.db.add(Biomarker(
                    user_id=user_id,
                    name=cb['name'],
                    value=cb['value'],
                    unit=cb['unit'],
                    normal_range=cb['normal_range'],
                    status=cb['status'],
                    category='computed'
                ))
        
        self.db.commit()
        return computed
    
    def detect_conditions(self, user_id: str) -> List[Dict]:
        """Detect health conditions from abnormal biomarkers."""
        biomarkers = self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()
        conditions = []
        
        for b in biomarkers:
            condition = None
            
            if b.name == 'vitamin_d' and b.status == 'low':
                condition = {'name': 'Vitamin D Deficiency', 'severity': 'moderate' if b.value < 20 else 'mild'}
            elif b.name == 'vitamin_b12' and b.status == 'low':
                condition = {'name': 'Vitamin B12 Deficiency', 'severity': 'mild'}
            elif b.name == 'hdl' and b.status == 'low':
                condition = {'name': 'Low HDL Cholesterol', 'severity': 'mild'}
            elif b.name == 'triglycerides' and b.status == 'high':
                condition = {'name': 'Hypertriglyceridemia', 'severity': 'moderate' if b.value > 200 else 'mild'}
            elif b.name == 'ldl' and b.status == 'high':
                condition = {'name': 'Elevated LDL Cholesterol', 'severity': 'mild'}
            elif b.name == 'hba1c' and b.value >= 5.7:
                condition = {'name': 'Prediabetes' if b.value < 6.5 else 'Diabetes', 'severity': 'moderate'}
            elif b.name == 'tsh' and (b.value < 0.4 or b.value > 4.5):
                condition = {'name': 'Thyroid Dysfunction', 'severity': 'mild'}
            
            if condition and condition['name'] not in [c['name'] for c in conditions]:
                condition['diagnosed_date'] = datetime.now().isoformat()
                conditions.append(condition)
        
        # Save to DB
        for cond in conditions:
            existing = self.db.query(MedicalHistory).filter(
                MedicalHistory.user_id == user_id,
                MedicalHistory.type == 'condition',
                MedicalHistory.name == cond['name']
            ).first()
            
            if not existing:
                self.db.add(MedicalHistory(
                    user_id=user_id,
                    type='condition',
                    name=cond['name'],
                    details={'severity': cond['severity'], 'auto_detected': True}
                ))
        
        self.db.commit()
        return conditions
    
    def recommend_supplements(self, user_id: str) -> List[Dict]:
        """Recommend supplements based on conditions."""
        conditions = self.db.query(MedicalHistory).filter(
            MedicalHistory.user_id == user_id,
            MedicalHistory.type == 'condition'
        ).all()
        
        supplements = []
        condition_names = [c.name for c in conditions]
        
        if 'Vitamin D Deficiency' in condition_names:
            supplements.append({
                'name': 'Vitamin D3',
                'dosage': '2000-4000 IU',
                'frequency': 'daily',
                'purpose': 'Correct vitamin D deficiency'
            })
        
        if 'Vitamin B12 Deficiency' in condition_names:
            supplements.append({
                'name': 'Vitamin B12',
                'dosage': '1000 mcg',
                'frequency': 'daily',
                'purpose': 'Correct B12 deficiency'
            })
        
        if 'Hypertriglyceridemia' in condition_names or 'Low HDL Cholesterol' in condition_names:
            supplements.append({
                'name': 'Omega-3 Fish Oil',
                'dosage': '1000-2000 mg',
                'frequency': 'daily',
                'purpose': 'Improve lipid profile'
            })
        
        if 'Elevated LDL Cholesterol' in condition_names:
            supplements.append({
                'name': 'Plant Sterols',
                'dosage': '2g',
                'frequency': 'daily',
                'purpose': 'Lower LDL cholesterol'
            })
        
        # Save to DB
        for supp in supplements:
            existing = self.db.query(MedicalHistory).filter(
                MedicalHistory.user_id == user_id,
                MedicalHistory.type == 'supplement',
                MedicalHistory.name == supp['name']
            ).first()
            
            if not existing:
                self.db.add(MedicalHistory(
                    user_id=user_id,
                    type='supplement',
                    name=supp['name'],
                    details=supp,
                    start_date=datetime.now()
                ))
        
        self.db.commit()
        return supplements
    
    def generate_goals(self, user_id: str) -> List[Dict]:
        """Generate health goals based on conditions."""
        conditions = self.db.query(MedicalHistory).filter(
            MedicalHistory.user_id == user_id,
            MedicalHistory.type == 'condition'
        ).all()
        
        biomarkers = {b.name: b for b in self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()}
        goals = []
        
        if 'Vitamin D Deficiency' in [c.name for c in conditions]:
            vit_d = biomarkers.get('vitamin_d')
            goals.append({
                'type': 'vitamin_optimization',
                'target': f'Increase Vitamin D from {vit_d.value if vit_d else "low"} to >30 ng/mL',
                'timeframe_months': 3
            })
        
        if 'Hypertriglyceridemia' in [c.name for c in conditions]:
            trig = biomarkers.get('triglycerides')
            goals.append({
                'type': 'lipid_management',
                'target': f'Reduce triglycerides from {trig.value if trig else "high"} to <150 mg/dL',
                'timeframe_months': 6
            })
        
        if 'Low HDL Cholesterol' in [c.name for c in conditions]:
            hdl = biomarkers.get('hdl')
            goals.append({
                'type': 'cardiovascular_health',
                'target': f'Increase HDL from {hdl.value if hdl else "low"} to >40 mg/dL',
                'timeframe_months': 6
            })
        
        # Save to DB
        for i, goal in enumerate(goals):
            goal_id = f"{user_id}_auto_goal_{i+1}"
            existing = self.db.query(Goal).filter(Goal.id == goal_id).first()
            
            if not existing:
                self.db.add(Goal(
                    id=goal_id,
                    user_id=user_id,
                    type=goal['type'],
                    target=goal['target'],
                    status='active',
                    start_date=datetime.now()
                ))
        
        self.db.commit()
        return goals
    
    def compute_biological_age(self, user_id: str) -> float:
        """Compute biological age from all biomarkers."""
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            return 0
        
        biomarkers = {b.name: b for b in self.db.query(Biomarker).filter(Biomarker.user_id == user_id).all()}
        age = user.age or 30
        adjustment = 0
        
        # Metabolic factors
        hba1c = biomarkers.get('hba1c')
        if hba1c:
            if hba1c.value > 6.5: adjustment += 5
            elif hba1c.value > 5.7: adjustment += 2
            elif hba1c.value < 5.0: adjustment -= 1
        
        # Cardiovascular factors
        hdl = biomarkers.get('hdl')
        if hdl:
            if hdl.value < 40: adjustment += 3
            elif hdl.value > 60: adjustment -= 2
        
        trig = biomarkers.get('triglycerides')
        if trig:
            if trig.value > 200: adjustment += 3
            elif trig.value > 150: adjustment += 1
            elif trig.value < 100: adjustment -= 1
        
        ldl = biomarkers.get('ldl')
        if ldl:
            if ldl.value > 160: adjustment += 2
            elif ldl.value > 130: adjustment += 1
            elif ldl.value < 100: adjustment -= 1
        
        # Vitamin factors
        vit_d = biomarkers.get('vitamin_d')
        if vit_d:
            if vit_d.value < 20: adjustment += 2
            elif vit_d.value < 30: adjustment += 1
            elif vit_d.value > 50: adjustment -= 1
        
        vit_b12 = biomarkers.get('vitamin_b12')
        if vit_b12:
            if vit_b12.value < 200: adjustment += 1
        
        # Kidney function
        egfr = biomarkers.get('egfr')
        if egfr:
            if egfr.value < 60: adjustment += 3
            elif egfr.value < 90: adjustment += 1
        
        bio_age = round(age + adjustment, 1)
        
        # Update user's biological age in DB
        user.biological_age = bio_age
        self.db.commit()
        
        return bio_age
    
    def close(self):
        self.db.close()


def run_pipeline_for_all_ocr_users():
    """Run computation pipeline for all OCR users."""
    computer = HealthDataComputer()
    
    users = computer.db.query(User).filter(User.data_source == 'ocr_extracted').all()
    results = []
    
    for user in users:
        print(f"🔄 Processing {user.id}...")
        result = computer.compute_all_for_user(user.id)
        results.append(result)
        print(f"   ✅ Computed: {len(result['computed_biomarkers'])} biomarkers, {len(result['conditions'])} conditions, {len(result['supplements'])} supplements, {len(result['goals'])} goals")
        print(f"   🧬 Biological Age: {result['biological_age']}")
    
    computer.close()
    return results


if __name__ == "__main__":
    print("🚀 Running Health Data Computation Pipeline")
    print("=" * 50)
    run_pipeline_for_all_ocr_users()
    print("\n✅ Pipeline complete!")
