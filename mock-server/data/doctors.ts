// Cardiologists Data
export const partneredDoctors = [
  {
    id: "dr-1",
    name: "Dr. Sarah Chen",
    specialty: "Interventional Cardiology",
    rating: 4.9,
    reviews: 234,
    distance: "0.8 mi",
    nextAvailable: "Tomorrow, 10:00 AM",
    image: "https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=200&h=200&fit=crop&crop=face",
    isPartner: true,
  },
  {
    id: "dr-2",
    name: "Dr. Michael Roberts",
    specialty: "Electrophysiology",
    rating: 4.8,
    reviews: 189,
    distance: "1.2 mi",
    nextAvailable: "Wed, 2:30 PM",
    image: "https://images.unsplash.com/photo-1612349317150-e413f6a5b16d?w=200&h=200&fit=crop&crop=face",
    isSponsored: true,
  },
];

export const otherDoctors = [
  {
    id: "dr-3",
    name: "Dr. Emily Watson",
    specialty: "General Cardiology",
    rating: 4.7,
    reviews: 156,
    distance: "2.1 mi",
    nextAvailable: "Thu, 9:00 AM",
    image: "https://images.unsplash.com/photo-1594824476967-48c8b964273f?w=200&h=200&fit=crop&crop=face",
  },
  {
    id: "dr-4",
    name: "Dr. James Liu",
    specialty: "Preventive Cardiology",
    rating: 4.6,
    reviews: 98,
    distance: "3.4 mi",
    nextAvailable: "Fri, 11:00 AM",
    image: "https://images.unsplash.com/photo-1537368910025-700350fe46c7?w=200&h=200&fit=crop&crop=face",
  },
  {
    id: "dr-5",
    name: "Dr. Amanda Foster",
    specialty: "Heart Failure Specialist",
    rating: 4.5,
    reviews: 87,
    distance: "4.2 mi",
    nextAvailable: "Next Mon, 3:00 PM",
    image: "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=200&h=200&fit=crop&crop=face",
  },
];

export const allCardiologists = [...partneredDoctors, ...otherDoctors];