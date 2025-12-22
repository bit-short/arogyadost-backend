// Metric Detail Data
export const metricDetails: Record<string, {
  title: string;
  subtitle: string;
  status: "good" | "attention" | "warning";
  metrics: {
    name: string;
    value: string;
    normalRange: string;
    color: string;
  }[];
  chartData: {
    [key: string]: string | number;
  }[];
  chartLines: {
    key: string;
    name: string;
    color: string;
  }[];
}> = {
  cholesterol: {
    title: "Cholesterol Panel",
    subtitle: "Last 12 months trend",
    status: "attention",
    metrics: [
      { name: "Total", value: "186", normalRange: "< 200", color: "#3B82F6" },
      { name: "LDL", value: "107", normalRange: "< 100", color: "#F97316" },
      { name: "HDL", value: "67", normalRange: "> 40", color: "#22C55E" },
      { name: "Triglycerides", value: "121", normalRange: "< 150", color: "#EAB308" },
    ],
    chartData: [
      { date: "Jan 20", total: 190, ldl: 120, hdl: 55, triglycerides: 58 },
      { date: "Jul 20", total: 195, ldl: 110, hdl: 60, triglycerides: 155 },
      { date: "Jan 21", total: 200, ldl: 115, hdl: 55, triglycerides: 145 },
      { date: "Jul 21", total: 220, ldl: 118, hdl: 65, triglycerides: 160 },
      { date: "Jan 22", total: 185, ldl: 125, hdl: 58, triglycerides: 150 },
      { date: "Jul 22", total: 210, ldl: 112, hdl: 55, triglycerides: 175 },
      { date: "Jan 23", total: 205, ldl: 108, hdl: 70, triglycerides: 145 },
      { date: "Jul 23", total: 210, ldl: 105, hdl: 55, triglycerides: 140 },
      { date: "Jan 24", total: 200, ldl: 118, hdl: 60, triglycerides: 135 },
      { date: "Jul 24", total: 215, ldl: 105, hdl: 65, triglycerides: 125 },
      { date: "Jan 25", total: 220, ldl: 102, hdl: 68, triglycerides: 118 },
      { date: "Jul 25", total: 186, ldl: 107, hdl: 67, triglycerides: 121 },
    ],
    chartLines: [
      { key: "total", name: "Total", color: "#3B82F6" },
      { key: "ldl", name: "LDL", color: "#F97316" },
      { key: "hdl", name: "HDL", color: "#22C55E" },
      { key: "triglycerides", name: "Triglycerides", color: "#EAB308" },
    ],
  },
  "blood-glucose": {
    title: "Blood Glucose",
    subtitle: "Last 6 months trend",
    status: "warning",
    metrics: [
      { name: "Fasting", value: "100", normalRange: "70-100", color: "#EF4444" },
      { name: "HbA1c", value: "5.8%", normalRange: "< 5.7%", color: "#F97316" },
    ],
    chartData: [
      { date: "Jun", fasting: 92, hba1c: 5.5 },
      { date: "Jul", fasting: 95, hba1c: 5.6 },
      { date: "Aug", fasting: 98, hba1c: 5.6 },
      { date: "Sep", fasting: 97, hba1c: 5.7 },
      { date: "Oct", fasting: 99, hba1c: 5.7 },
      { date: "Nov", fasting: 100, hba1c: 5.8 },
    ],
    chartLines: [
      { key: "fasting", name: "Fasting", color: "#EF4444" },
    ],
  },
  "blood-pressure": {
    title: "Blood Pressure",
    subtitle: "Last 6 months trend",
    status: "attention",
    metrics: [
      { name: "Systolic", value: "132", normalRange: "< 120", color: "#EF4444" },
      { name: "Diastolic", value: "71", normalRange: "< 80", color: "#3B82F6" },
    ],
    chartData: [
      { date: "Jun", systolic: 128, diastolic: 78 },
      { date: "Jul", systolic: 130, diastolic: 75 },
      { date: "Aug", systolic: 125, diastolic: 72 },
      { date: "Sep", systolic: 135, diastolic: 76 },
      { date: "Oct", systolic: 130, diastolic: 74 },
      { date: "Nov", systolic: 132, diastolic: 71 },
    ],
    chartLines: [
      { key: "systolic", name: "Systolic", color: "#EF4444" },
      { key: "diastolic", name: "Diastolic", color: "#3B82F6" },
    ],
  },
  "vitamin-d": {
    title: "Vitamin D",
    subtitle: "Last 6 months trend",
    status: "good",
    metrics: [
      { name: "Level", value: "31", normalRange: "30-100", color: "#22C55E" },
    ],
    chartData: [
      { date: "Jun", level: 22 },
      { date: "Jul", level: 24 },
      { date: "Aug", level: 26 },
      { date: "Sep", level: 28 },
      { date: "Oct", level: 29 },
      { date: "Nov", level: 31 },
    ],
    chartLines: [
      { key: "level", name: "Vitamin D", color: "#22C55E" },
    ],
  },
  "heart-rate": {
    title: "Resting Heart Rate",
    subtitle: "Last 6 months trend",
    status: "good",
    metrics: [
      { name: "Average", value: "72", normalRange: "60-100", color: "#EF4444" },
    ],
    chartData: [
      { date: "Jun", average: 78 },
      { date: "Jul", average: 76 },
      { date: "Aug", average: 75 },
      { date: "Sep", average: 74 },
      { date: "Oct", average: 73 },
      { date: "Nov", average: 72 },
    ],
    chartLines: [
      { key: "average", name: "Heart Rate", color: "#EF4444" },
    ],
  },
  hdl: {
    title: "HDL Cholesterol",
    subtitle: "Last 6 months trend",
    status: "attention",
    metrics: [
      { name: "Level", value: "67", normalRange: "> 40", color: "#22C55E" },
    ],
    chartData: [
      { date: "Jun", level: 55 },
      { date: "Jul", level: 58 },
      { date: "Aug", level: 60 },
      { date: "Sep", level: 62 },
      { date: "Oct", level: 65 },
      { date: "Nov", level: 67 },
    ],
    chartLines: [
      { key: "level", name: "HDL", color: "#22C55E" },
    ],
  },
  ldl: {
    title: "LDL Cholesterol",
    subtitle: "Last 6 months trend",
    status: "attention",
    metrics: [
      { name: "Level", value: "107", normalRange: "< 100", color: "#F97316" },
    ],
    chartData: [
      { date: "Jun", level: 120 },
      { date: "Jul", level: 118 },
      { date: "Aug", level: 115 },
      { date: "Sep", level: 112 },
      { date: "Oct", level: 110 },
      { date: "Nov", level: 107 },
    ],
    chartLines: [
      { key: "level", name: "LDL", color: "#F97316" },
    ],
  },
  triglycerides: {
    title: "Triglycerides",
    subtitle: "Last 6 months trend",
    status: "good",
    metrics: [
      { name: "Level", value: "121", normalRange: "< 150", color: "#EAB308" },
    ],
    chartData: [
      { date: "Jun", level: 145 },
      { date: "Jul", level: 140 },
      { date: "Aug", level: 135 },
      { date: "Sep", level: 130 },
      { date: "Oct", level: 125 },
      { date: "Nov", level: 121 },
    ],
    chartLines: [
      { key: "level", name: "Triglycerides", color: "#EAB308" },
    ],
  },
};