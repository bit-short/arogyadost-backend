// Action Details Data
export const actionDetails: Record<string, {
  icon: string;
  title: string;
  color: string;
  overview: string;
  benefits: string[];
  howItHelps: string;
  nextSteps: string[];
  isTodo?: boolean;
  todoItems?: { label: string; checked: boolean; link?: string }[];
  personalizedSummary?: {
    improving: { label: string; detail: string }[];
    declining: { label: string; detail: string }[];
  };
  hasReport?: boolean;
}> = {
  cardiologist: {
    icon: "Stethoscope",
    title: "Cardiologist Visit",
    color: "bg-red-500",
    overview: "Based on your health data, a visit to a cardiologist is recommended to evaluate your cardiovascular health and address any potential concerns.",
    benefits: [
      "Comprehensive heart health evaluation",
      "Early detection of cardiovascular issues",
      "Personalized treatment and prevention plan",
      "Peace of mind about your heart health",
    ],
    howItHelps: "A cardiologist can perform detailed assessments including ECG, stress tests, and echocardiograms to get a complete picture of your heart health. Early intervention is key to preventing serious cardiovascular events.",
    nextSteps: [],
    isTodo: true,
    todoItems: [
      { label: "Find a cardiologist in your network", checked: false, link: "/find-cardiologist" },
      { label: "Schedule an appointment", checked: false },
      { label: "Gather recent health records and test results", checked: false },
      { label: "Prepare list of symptoms and questions", checked: false },
      { label: "Note family history of heart disease", checked: false },
      { label: "List current medications and supplements", checked: false },
    ],
    personalizedSummary: {
      improving: [
        { label: "Resting Heart Rate", detail: "Down 5 bpm over last month" },
        { label: "Daily Steps", detail: "Averaging 6,200 steps (up from 4,800)" },
      ],
      declining: [
        { label: "Blood Pressure", detail: "Elevated readings (138/88 avg)" },
        { label: "Heart Rate Variability", detail: "Below optimal range for your age" },
        { label: "Cholesterol (estimated)", detail: "LDL trending higher based on lifestyle factors" },
      ],
    },
    hasReport: true,
  },
  wearable: {
    icon: "Watch",
    title: "Connect a Wearable",
    color: "bg-blue-500",
    overview: "Wearable devices like smartwatches and fitness trackers can continuously monitor your health metrics, providing valuable insights that periodic checkups might miss.",
    benefits: [
      "Continuous heart rate monitoring detects irregularities early",
      "Sleep tracking helps identify patterns affecting your rest quality",
      "Step counting and activity tracking motivates daily movement",
      "Stress and HRV data reveals how your body responds to daily challenges",
    ],
    howItHelps: "By connecting a wearable, your health score becomes more accurate and personalized. Instead of relying on occasional measurements, we can track trends over time and alert you to changes that matter. Many health issues show early warning signs in sleep patterns or heart rate variability before symptoms appear.",
    nextSteps: [
      "Go to Settings → Data Sources",
      "Select your wearable device brand",
      "Follow the pairing instructions",
      "Allow data sync permissions",
    ],
  },
  "lipid-panel": {
    icon: "FlaskConical",
    title: "Lipid Panel Test",
    color: "bg-orange-500",
    overview: "A lipid panel measures cholesterol and triglyceride levels in your blood, providing crucial information about your cardiovascular health risk.",
    benefits: [
      "Identifies high LDL (bad) cholesterol before it causes problems",
      "Tracks HDL (good) cholesterol that protects your heart",
      "Measures triglycerides linked to heart disease risk",
      "Helps determine if lifestyle changes or medications are needed",
    ],
    howItHelps: "Based on your current health profile, a lipid panel would give us a clearer picture of your heart health. Your moderate cholesterol indicator suggests this test could reveal important information. Early detection of lipid imbalances allows for dietary adjustments and lifestyle changes that can prevent serious cardiovascular issues.",
    nextSteps: [],
    isTodo: true,
    todoItems: [
      { label: "Find a lab or hospital near you", checked: false, link: "/find-lab/lipid-panel" },
      { label: "Schedule your appointment", checked: false },
      { label: "Fast for 9-12 hours before the test", checked: false },
      { label: "Complete the blood draw", checked: false },
      { label: "Upload results to your health profile", checked: false },
    ],
  },
  activity: {
    icon: "Activity",
    title: "Increase Daily Steps",
    color: "bg-green-500",
    overview: "Regular walking is one of the most effective and accessible ways to improve cardiovascular health, maintain healthy weight, and boost mental wellbeing.",
    benefits: [
      "Reduces risk of heart disease by up to 35%",
      "Improves mood and reduces anxiety and depression",
      "Helps maintain healthy blood pressure levels",
      "Strengthens bones and muscles without high impact",
    ],
    howItHelps: "Your current activity levels suggest room for improvement. Research shows that increasing daily steps to 8,000 can significantly reduce mortality risk. Even small increases—like 2,000 extra steps—provide measurable health benefits. Walking after meals also helps regulate blood sugar levels.",
    nextSteps: [
      "Start with a 10-minute walk after each meal",
      "Use stairs instead of elevators when possible",
      "Set hourly reminders to stand and move",
      "Track progress with your phone or wearable",
    ],
  },
  "vitamin-d": {
    icon: "Pill",
    title: "Vitamin D Test",
    color: "bg-yellow-500",
    overview: "Vitamin D is essential for skin health, immune function, and bone strength. Many people are deficient without knowing it, especially those with limited sun exposure.",
    benefits: [
      "Supports skin cell growth and repair",
      "Reduces inflammation that worsens skin conditions",
      "Strengthens immune system function",
      "Helps calcium absorption for bone health",
    ],
    howItHelps: "Low vitamin D levels are associated with slower skin healing and increased inflammation. Given your skin health goals, knowing your vitamin D status could reveal if supplementation might help. Many people see improvements in skin conditions after correcting deficiency.",
    nextSteps: [],
    isTodo: true,
    todoItems: [
      { label: "Find a lab or hospital near you", checked: false, link: "/find-lab/vitamin-d" },
      { label: "Schedule your appointment", checked: false },
      { label: "Complete the 25-hydroxyvitamin D blood test", checked: false },
      { label: "Upload results to track over time", checked: false },
      { label: "Discuss supplementation with your doctor if low", checked: false },
    ],
  },
};