// Health Biomarkers Data
export const healthCategories = [
  {
    id: "skin",
    label: "Skin",
    score: 51,
    markers: [
      { name: "Acne", level: "Moderate", value: 55, color: "orange" },
      { name: "Scarring", level: "Moderately Severe", value: 70, color: "red" },
      { name: "Pigmentation", level: "Mild", value: 35, color: "yellow" },
    ],
  },
  {
    id: "heart",
    label: "Heart",
    score: 78,
    markers: [
      { name: "Blood Pressure", level: "Normal", value: 30, color: "green" },
      { name: "Heart Rate", level: "Good", value: 25, color: "green" },
      { name: "Cholesterol", level: "Moderate", value: 50, color: "orange" },
    ],
  },
  {
    id: "sleep",
    label: "Sleep",
    score: 65,
    markers: [
      { name: "Duration", level: "Good", value: 40, color: "green" },
      { name: "Deep Sleep", level: "Low", value: 60, color: "orange" },
      { name: "Consistency", level: "Moderate", value: 50, color: "yellow" },
    ],
  },
];

// Health Recommendations Data
export const recommendedActions = [
  {
    id: "cardiologist",
    icon: "Stethoscope",
    title: "Cardiologist Visit Recommended",
    description: "Schedule a heart health checkup",
    priority: "urgent" as const,
    color: "bg-red-500",
  },
  {
    id: "wearable",
    icon: "Watch",
    title: "Connect a Wearable",
    description: "Track sleep and heart rate automatically",
    priority: "soon" as const,
    color: "bg-blue-500",
  },
  {
    id: "lipid-panel",
    icon: "FlaskConical",
    title: "Lipid Panel Test",
    description: "Recommended based on cholesterol levels",
    priority: "soon" as const,
    color: "bg-orange-500",
  },
  {
    id: "activity",
    icon: "Activity",
    title: "Increase Daily Steps",
    description: "Aim for 8,000 steps to improve heart health",
    priority: "flexible" as const,
    color: "bg-green-500",
  },
  {
    id: "vitamin-d",
    icon: "Pill",
    title: "Vitamin D Test",
    description: "Check levels for skin and immune health",
    priority: "flexible" as const,
    color: "bg-yellow-500",
  },
];

// Health Status Metrics
export const healthMetrics = [
  {
    id: "cholesterol",
    name: "Cholesterol (Total)",
    value: "205",
    unit: "mg/dL",
    status: "attention",
    normalRange: "< 200",
    trend: "down",
  },
  {
    id: "blood-glucose",
    name: "Blood Glucose",
    value: "100",
    unit: "mg/dL",
    status: "warning",
    normalRange: "70-100",
  },
  {
    id: "blood-pressure",
    name: "Blood Pressure",
    value: "132/71",
    unit: "mmHg",
    status: "attention",
    normalRange: "< 120/80",
  },
  {
    id: "vitamin-d",
    name: "Vitamin D",
    value: "31",
    unit: "ng/mL",
    status: "good",
    normalRange: "30-100",
    trend: "up",
  },
  {
    id: "heart-rate",
    name: "Resting Heart Rate",
    value: "72",
    unit: "bpm",
    status: "good",
    normalRange: "60-100",
  },
  {
    id: "hdl",
    name: "HDL Cholesterol",
    value: "67",
    unit: "mg/dL",
    status: "attention",
    normalRange: "> 40",
  },
  {
    id: "ldl",
    name: "LDL Cholesterol",
    value: "107",
    unit: "mg/dL",
    status: "attention",
    normalRange: "< 100",
  },
  {
    id: "triglycerides",
    name: "Triglycerides",
    value: "121",
    unit: "mg/dL",
    status: "good",
    normalRange: "< 150",
  },
];

// Health Report Metrics
export const healthReportMetrics = [
  {
    id: "1",
    label: "Resting Heart Rate",
    value: "72 bpm",
    trend: "down",
    trendLabel: "Down 5 bpm"
  },
  {
    id: "2",
    label: "Blood Pressure",
    value: "138/88 mmHg",
    trend: "up",
    trendLabel: "Elevated"
  },
  {
    id: "3",
    label: "HRV",
    value: "32 ms",
    trend: "down",
    trendLabel: "Below optimal"
  },
  {
    id: "4",
    label: "Daily Steps (avg)",
    value: "6,200",
    trend: "up",
    trendLabel: "Up 29%"
  },
  {
    id: "5",
    label: "Sleep Score",
    value: "72/100",
    trend: "stable",
    trendLabel: "Stable"
  },
  {
    id: "6",
    label: "Weight",
    value: "165 lbs",
    trend: "stable",
    trendLabel: "Stable"
  }
];