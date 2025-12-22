// Biomarker Detail Data
export const biomarkerData: Record<string, {
  title: string;
  score: number;
  trend: "up" | "down";
  trendValue: string;
  chartData: { date: string; value: number }[];
  details: { name: string; current: string; optimal: string }[];
  improving: { name: string; change: string; description: string }[];
  needsAttention: { name: string; issue: string; suggestion: string }[];
}> = {
  overview: {
    title: "Overall Health Score",
    score: 65,
    trend: "up",
    trendValue: "+3 from last month",
    chartData: [
      { date: "Jun", value: 58 },
      { date: "Jul", value: 60 },
      { date: "Aug", value: 61 },
      { date: "Sep", value: 62 },
      { date: "Oct", value: 63 },
      { date: "Nov", value: 65 },
    ],
    details: [
      { name: "Skin Health", current: "51/100", optimal: "70+" },
      { name: "Heart Health", current: "78/100", optimal: "80+" },
      { name: "Sleep Quality", current: "65/100", optimal: "75+" },
    ],
    improving: [
      { name: "Heart Health", change: "+8 points", description: "Consistent improvement from regular walking" },
      { name: "Blood Pressure", change: "Normalized", description: "Now within healthy range after lifestyle changes" },
      { name: "Daily Steps", change: "+2,000/day", description: "Activity levels have steadily increased" },
    ],
    needsAttention: [
      { name: "Deep Sleep", issue: "12% (below optimal)", suggestion: "Try reducing screen time 1 hour before bed" },
      { name: "Acne", issue: "Moderate severity", suggestion: "Consider dermatologist follow-up" },
      { name: "Vitamin D", issue: "Not tested recently", suggestion: "Schedule a blood test" },
    ],
  },
  skin: {
    title: "Skin Health Score",
    score: 51,
    trend: "up",
    trendValue: "+5 from last month",
    chartData: [
      { date: "Jun", value: 42 },
      { date: "Jul", value: 45 },
      { date: "Aug", value: 48 },
      { date: "Sep", value: 46 },
      { date: "Oct", value: 49 },
      { date: "Nov", value: 51 },
    ],
    details: [
      { name: "Acne", current: "Moderate", optimal: "Minimal" },
      { name: "Scarring", current: "Moderately Severe", optimal: "Mild" },
      { name: "Pigmentation", current: "Mild", optimal: "None" },
    ],
    improving: [
      { name: "Pigmentation", change: "Reduced by 20%", description: "SPF usage is showing results" },
      { name: "Hydration", change: "Improved", description: "Moisturizer routine working well" },
    ],
    needsAttention: [
      { name: "Acne", issue: "Persistent breakouts", suggestion: "Consider prescription treatment" },
      { name: "Scarring", issue: "Slow healing", suggestion: "Discuss retinoid options with dermatologist" },
    ],
  },
  heart: {
    title: "Heart Health Score",
    score: 78,
    trend: "up",
    trendValue: "+3 from last month",
    chartData: [
      { date: "Jun", value: 70 },
      { date: "Jul", value: 72 },
      { date: "Aug", value: 74 },
      { date: "Sep", value: 75 },
      { date: "Oct", value: 76 },
      { date: "Nov", value: 78 },
    ],
    details: [
      { name: "Blood Pressure", current: "120/80", optimal: "< 120/80" },
      { name: "Heart Rate", current: "72 bpm", optimal: "60-100 bpm" },
      { name: "Cholesterol", current: "195 mg/dL", optimal: "< 200 mg/dL" },
    ],
    improving: [
      { name: "Resting Heart Rate", change: "-5 bpm", description: "Cardio fitness improving" },
      { name: "Blood Pressure", change: "Stable", description: "Maintaining healthy levels" },
    ],
    needsAttention: [
      { name: "Cholesterol", issue: "Borderline high", suggestion: "Schedule lipid panel test" },
      { name: "Activity Gaps", issue: "Sedentary weekends", suggestion: "Add weekend walks" },
    ],
  },
  sleep: {
    title: "Sleep Quality Score",
    score: 65,
    trend: "up",
    trendValue: "+2 from last month",
    chartData: [
      { date: "Jun", value: 58 },
      { date: "Jul", value: 60 },
      { date: "Aug", value: 61 },
      { date: "Sep", value: 62 },
      { date: "Oct", value: 64 },
      { date: "Nov", value: 65 },
    ],
    details: [
      { name: "Duration", current: "7.2 hrs", optimal: "7-9 hrs" },
      { name: "Deep Sleep", current: "12%", optimal: "15-25%" },
      { name: "Consistency", current: "Moderate", optimal: "High" },
    ],
    improving: [
      { name: "Sleep Duration", change: "+30 min", description: "Earlier bedtime helping" },
      { name: "Consistency", change: "More regular", description: "Bedtime routine established" },
    ],
    needsAttention: [
      { name: "Deep Sleep", issue: "Below optimal range", suggestion: "Reduce caffeine after 2 PM" },
      { name: "Wake-ups", issue: "Frequent interruptions", suggestion: "Consider sleep environment improvements" },
    ],
  },
};