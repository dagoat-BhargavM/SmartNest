"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Label } from "@/components/ui/label";
import { ArrowLeft, ArrowRight, Loader2 } from "lucide-react";
import GaugeChart from "react-gauge-chart";

type QuestionOption = {
  value: string;
  label: string;
};

type Question = {
  id: string;
  question: string;
  type: "number" | "radio" | "checkbox-group";
  options?: QuestionOption[];
};

// 1. Define your question list
const questions: Question[] = [
  // Numeric questions
  { id: "age", question: "What is your age?", type: "number" },
  { id: "familyDependents", question: "How many family members or dependents rely on you financially?", type: "number" },
  { id: "monthlyIncome", question: "What is your average monthly income?", type: "number" },
  { id: "monthlyExpenses", question: "What are your average monthly expenses?", type: "number" },
  { id: "savings", question: "How much do you have in savings and emergency funds?", type: "number" },
  { id: "debt", question: "How much debt do you currently have?", type: "number" },

  // Risk Tolerance (radio)
  {
    id: "riskQ1",
    question: "When the stock market declines significantly, what would you most likely do?",
    type: "radio",
    options: [
      { value: "1", label: "A) Sell all investments to avoid further loss" },
      { value: "2", label: "B) Sell some investments and hold others" },
      { value: "3", label: "C) Do nothing and wait for the market to recover" },
      { value: "4", label: "D) Invest more to take advantage of low prices" },
    ],
  },
  {
    id: "riskQ2",
    question: "How do you feel about investing in assets that have high short-term volatility but potential for high long-term returns?",
    type: "radio",
    options: [
      { value: "1", label: "A) Extremely uncomfortable" },
      { value: "2", label: "B) Slightly uncomfortable" },
      { value: "3", label: "C) Neutral" },
      { value: "4", label: "D) Very comfortable" },
    ],
  },
  {
    id: "riskQ3",
    question: "What is your primary financial goal? (Risk Tolerance)",
    type: "radio",
    options: [
      { value: "1", label: "A) Preserve wealth with minimal risk" },
      { value: "2", label: "B) Moderate growth with controlled risk" },
      { value: "3", label: "C) High growth, accepting moderate risk" },
      { value: "4", label: "D) Maximizing returns, accepting high risk" },
    ],
  },
  {
    id: "riskQ4",
    question: "What is the time frame for your investments?",
    type: "radio",
    options: [
      { value: "1", label: "A) Less than 1 year" },
      { value: "2", label: "B) 1–3 years" },
      { value: "3", label: "C) 3–7 years" },
      { value: "4", label: "D) More than 7 years" },
    ],
  },
  {
    id: "riskQ5",
    question: "If you had to choose between two investments, which would you prefer?",
    type: "radio",
    options: [
      { value: "1", label: "A) Guaranteed return of 5%" },
      { value: "2", label: "B) 50% chance of a 10% return and 50% chance of no return" },
      { value: "3", label: "C) 25% chance of a 20% return and 75% chance of a 5% return" },
      { value: "4", label: "D) 10% chance of a 50% return and 90% chance of no return" },
    ],
  },
  {
    id: "riskQ6",
    question: "How much of your monthly savings would you feel comfortable investing in equities?",
    type: "radio",
    options: [
      { value: "1", label: "A) Less than 10%" },
      { value: "2", label: "B) 10–25%" },
      { value: "3", label: "C) 25–50%" },
      { value: "4", label: "D) More than 50%" },
    ],
  },
  {
    id: "riskQ7",
    question: "How stable is your current financial situation?",
    type: "radio",
    options: [
      { value: "1", label: "A) Very unstable; cannot afford any losses" },
      { value: "2", label: "B) Somewhat unstable; small losses are manageable" },
      { value: "3", label: "C) Stable; can handle moderate losses" },
      { value: "4", label: "D) Very stable; can handle significant losses" },
    ],
  },
  {
    id: "riskQ8",
    question: "How diversified are your current investments?",
    type: "radio",
    options: [
      { value: "1", label: "A) Fully in fixed deposits and gold" },
      { value: "2", label: "B) Mostly in low-risk instruments with minor equity exposure" },
      { value: "3", label: "C) Balanced between low-risk and high-risk instruments" },
      { value: "4", label: "D) Heavy equity exposure with limited fixed income" },
    ],
  },

  // Categorical Data (radio)
  {
    id: "maritalStatus",
    question: "What is your marital status?",
    type: "radio",
    options: [
      { value: "Single", label: "Single" },
      { value: "Married", label: "Married" },
      { value: "Divorced", label: "Divorced" },
    ],
  },
  {
    id: "education",
    question: "What is your highest educational level?",
    type: "radio",
    options: [
      { value: "High School", label: "High School" },
      { value: "Undergraduate", label: "Undergraduate" },
      { value: "Postgraduate", label: "Postgraduate" },
      { value: "Doctorate", label: "Doctorate" },
    ],
  },
  {
    id: "employmentStatus",
    question: "What is your employment status?",
    type: "radio",
    options: [
      { value: "Regular Salary", label: "Regular Salary" },
      { value: "Unemployed", label: "Unemployed" },
      { value: "Varying Salary", label: "Varying Salary" },
    ],
  },
  {
    id: "investmentHorizon",
    question: "What is your investment horizon?",
    type: "radio",
    options: [
      { value: "Short", label: "Short (Less than 1 year)" },
      { value: "Medium", label: "Medium (1–3 years)" },
      { value: "Long", label: "Long (More than 3 years)" },
    ],
  },
  {
    id: "primaryFinancialGoal",
    question: "What is your primary financial goal?",
    type: "radio",
    options: [
      { value: "Capital Growth/Expansion", label: "Capital Growth/Expansion" },
      { value: "Wealth Preservation", label: "Wealth Preservation" },
    ],
  },

  // Multi-Choice (checkbox group)
  {
    id: "existingInvestments",
    question: "Do you have any existing investments? (Select all that apply)",
    type: "checkbox-group",
    options: [
      { value: "equities", label: "Equities" },
      { value: "fixedDeposits", label: "Fixed Deposits" },
      { value: "gold", label: "Gold" },
      { value: "mutualFunds", label: "Mutual Funds" },
      { value: "realEstate", label: "Real Estate" },
    ],
  },
  {
    id: "insurances",
    question: "Do you have any insurance? (Select all that apply)",
    type: "checkbox-group",
    options: [
      { value: "healthInsurance", label: "Health Insurance" },
      { value: "criticalIllnessInsurance", label: "Critical Illness Insurance" },
      { value: "personalAccidentInsurance", label: "Personal Accident Insurance" },
      { value: "termLifeInsurance", label: "Term Life Insurance" },
    ],
  },
];

export default function RiskScoreForm() {
  const [currentStep, setCurrentStep] = useState(0);
  const totalSteps = questions.length;

  const [loading, setLoading] = useState(false);
  const [riskScore, setRiskScore] = useState<number | null>(null);

  // If true, we show the gauge and hide the form
  const [showGauge, setShowGauge] = useState(false);

  // 2. Initialize form data
  const [formData, setFormData] = useState<Record<string, any>>({
    age: "",
    familyDependents: "",
    monthlyIncome: "",
    monthlyExpenses: "",
    savings: "",
    debt: "",
    riskQ1: "",
    riskQ2: "",
    riskQ3: "",
    riskQ4: "",
    riskQ5: "",
    riskQ6: "",
    riskQ7: "",
    riskQ8: "",
    maritalStatus: "",
    education: "",
    employmentStatus: "",
    investmentHorizon: "",
    primaryFinancialGoal: "",
    existingInvestments: [],
    insurances: [],
  });

  // 3. Handlers for different question types
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleRadioChange = (value: string, name: string) => {
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleCheckboxChange = (e: React.ChangeEvent<HTMLInputElement>, questionId: string) => {
    const { value, checked } = e.target;
    setFormData((prev) => {
      const currentArray = prev[questionId] || [];
      if (checked) {
        return { ...prev, [questionId]: [...currentArray, value] };
      } else {
        return { ...prev, [questionId]: currentArray.filter((item: string) => item !== value) };
      }
    });
  };

  // 4. Navigation
  const handleNext = () => {
    if (currentStep < totalSteps - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // On the last question, calculate the score and show the gauge
      setLoading(true);
      const score = calculateRiskScore();
      setRiskScore(score);
      setShowGauge(true);
      setLoading(false);
    }
  };

  const handlePrevious = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  // 5. Calculate the risk score
  const calculateRiskScore = () => {
    // Parse numeric fields
    const age = parseFloat(formData.age);
    const familyDependents = parseFloat(formData.familyDependents);
    const monthlyIncome = parseFloat(formData.monthlyIncome);
    const monthlyExpenses = parseFloat(formData.monthlyExpenses);
    const savings = parseFloat(formData.savings);
    const debt = parseFloat(formData.debt);

    // Sum up risk tolerance answers (1–4 each)
    const riskQs = ["riskQ1", "riskQ2", "riskQ3", "riskQ4", "riskQ5", "riskQ6", "riskQ7", "riskQ8"];
    let riskToleranceScore = 0;
    riskQs.forEach((q) => {
      riskToleranceScore += parseFloat(formData[q] || "0");
    });

    // ---- Normalization using your means/std devs ----
    const normAge = (age - 43.9194) / 15.1376;
    const normFamily = (familyDependents - 4.9846) / 3.1596;
    const normIncome = (monthlyIncome - 104169.3067) / 54837.2557;
    const normExpenses = (monthlyExpenses - 88526.0486) / 52379.8243;
    const normSavings = (savings - 2517030.0) / 1474535.9964;
    const normDebt = (debt - 1004400.0) / 604631.4563;
    const normRiskTolerance = (riskToleranceScore - 20.0841) / 7.2042;

    // ---- Multiply by weights ----
    const weightedAge = normAge * (-0.0102);
    const weightedFamily = normFamily * (-0.0306);
    const weightedIncome = normIncome * 0.1224;
    const weightedExpenses = normExpenses * (-0.1020);
    const weightedSavings = normSavings * 0.1531;
    const weightedDebt = normDebt * (-0.2040);
    const weightedRiskTolerance = normRiskTolerance * 0.0612;

    // ---- Categorical data weights ----
    let maritalWeight = 0;
    if (formData.maritalStatus === "Single") maritalWeight = 0.0306;
    else if (formData.maritalStatus === "Married") maritalWeight = -0.0204;
    else if (formData.maritalStatus === "Divorced") maritalWeight = -0.0306;

    let educationWeight = 0;
    if (formData.education === "High School") educationWeight = 0.0204;
    else if (formData.education === "Undergraduate") educationWeight = 0.0510;
    else if (formData.education === "Postgraduate") educationWeight = 0.0714;
    else if (formData.education === "Doctorate") educationWeight = 0.1020;

    let employmentWeight = 0;
    if (formData.employmentStatus === "Regular Salary") employmentWeight = 0.0612;
    else if (formData.employmentStatus === "Unemployed") employmentWeight = -0.0510;
    else if (formData.employmentStatus === "Varying Salary") employmentWeight = 0.0306;

    let horizonWeight = 0;
    if (formData.investmentHorizon === "Short") horizonWeight = 0.0816;
    else if (formData.investmentHorizon === "Medium") horizonWeight = 0.0408;
    else if (formData.investmentHorizon === "Long") horizonWeight = 0.0204;

    let financialGoalWeight = 0;
    if (formData.primaryFinancialGoal === "Capital Growth/Expansion") financialGoalWeight = 0.1020;
    else if (formData.primaryFinancialGoal === "Wealth Preservation") financialGoalWeight = 0.0510;

    // ---- Multi-choice (checkbox) weights ----
    let investmentsWeight = 0;
    if (formData.existingInvestments.includes("equities")) investmentsWeight += 0.0816;
    if (formData.existingInvestments.includes("fixedDeposits")) investmentsWeight += 0.0408;
    if (formData.existingInvestments.includes("gold")) investmentsWeight += 0.0612;
    if (formData.existingInvestments.includes("mutualFunds")) investmentsWeight += 0.0714;
    if (formData.existingInvestments.includes("realEstate")) investmentsWeight += 0.0714;

    let insuranceWeight = 0;
    if (formData.insurances.includes("healthInsurance")) insuranceWeight += 0.0408;
    if (formData.insurances.includes("criticalIllnessInsurance")) insuranceWeight += 0.0306;
    if (formData.insurances.includes("personalAccidentInsurance")) insuranceWeight += 0.0204;
    if (formData.insurances.includes("termLifeInsurance")) insuranceWeight += 0.0306;

    // ---- Sum everything ----
    const finalRiskScore =
      weightedAge +
      weightedFamily +
      weightedIncome +
      weightedExpenses +
      weightedSavings +
      weightedDebt +
      weightedRiskTolerance +
      maritalWeight +
      educationWeight +
      employmentWeight +
      horizonWeight +
      financialGoalWeight +
      investmentsWeight +
      insuranceWeight;

    return finalRiskScore;
  };

  // 6. Show the question or the gauge
  const progress = ((currentStep + 1) / totalSteps) * 100;

  // Render a single question
  const renderQuestion = () => {
    const q = questions[currentStep];

    switch (q.type) {
      case "number":
        return (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold">{q.question}</h2>
            <input
              type="number"
              name={q.id}
              value={formData[q.id]}
              onChange={handleInputChange}
              className="mt-2 block w-full border rounded p-2"
              required
            />
          </div>
        );
      case "radio":
        return (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold">{q.question}</h2>
            <RadioGroup
              value={formData[q.id]}
              onValueChange={(value) => handleRadioChange(value, q.id)}
              className="space-y-4"
            >
              {q.options?.map((option) => (
                <div key={option.value} className="flex items-center space-x-2">
                  <RadioGroupItem value={option.value} id={`${q.id}-${option.value}`} />
                  <Label htmlFor={`${q.id}-${option.value}`}>{option.label}</Label>
                </div>
              ))}
            </RadioGroup>
          </div>
        );
      case "checkbox-group":
        return (
          <div className="space-y-4">
            <h2 className="text-2xl font-semibold">{q.question}</h2>
            {q.options?.map((option) => (
              <div key={option.value} className="flex items-center space-x-2">
                <input
                  type="checkbox"
                  value={option.value}
                  checked={formData[q.id].includes(option.value)}
                  onChange={(e) => handleCheckboxChange(e, q.id)}
                  className="h-4 w-4"
                />
                <Label>{option.label}</Label>
              </div>
            ))}
          </div>
        );
      default:
        return null;
    }
  };

  // 7. Gauge chart configuration
  const renderGauge = () => {
    if (riskScore === null) return null;

    // Suppose your risk score typically ranges from -2.0 (low) to +2.0 (high).
    // We'll convert it to [0..1] for the gauge.
    const minScore = -2;
    const maxScore = 2;
    let fraction = (riskScore - minScore) / (maxScore - minScore);
    if (fraction < 0) fraction = 0;
    if (fraction > 1) fraction = 1;

    return (
      <div className="text-center space-y-4">
        <h2 className="text-2xl font-bold">Your Risk Score: {riskScore.toFixed(2)}</h2>
        <GaugeChart
          id="risk-gauge"
          nrOfLevels={30}
          colors={["#FF5F6D", "#FFC371", "#00b300"]} // red -> yellow -> green
          percent={fraction}
          animate={true}
          animDelay={0}
          animDuration={3000}  // 3-second animation
          needleColor="#464A4F"
          needleBaseColor="#464A4F"
          textColor="#000"
          hideText={true}
        />
        <p className="max-w-md mx-auto">
          The needle indicates your relative position between low risk and high risk.
        </p>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Progress Bar */}
      <div className="fixed top-0 left-0 right-0 h-2">
        {!showGauge && <Progress value={progress} className="h-full" />}
      </div>

      <main className="flex-1 container max-w-2xl mx-auto px-4 py-16">
        {showGauge ? (
          // ---- SHOW GAUGE ----
          <AnimatePresence mode="wait">
            <motion.div
              key="gauge"
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -20 }}
              transition={{ duration: 0.3 }}
            >
              {renderGauge()}
            </motion.div>
          </AnimatePresence>
        ) : (
          // ---- SHOW QUESTIONS ----
          <>
            <AnimatePresence mode="wait">
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="space-y-8"
              >
                {renderQuestion()}
              </motion.div>
            </AnimatePresence>

            <div className="flex justify-between mt-12">
              <Button variant="outline" onClick={handlePrevious} disabled={currentStep === 0}>
                <ArrowLeft className="mr-2 h-4 w-4" /> Previous
              </Button>
              <Button onClick={handleNext} disabled={loading}>
                {loading ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" /> Processing
                  </>
                ) : (
                  <>
                    {currentStep === totalSteps - 1 ? "Complete" : (
                      <>
                        Next <ArrowRight className="ml-2 h-4 w-4" />
                      </>
                    )}
                  </>
                )}
              </Button>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
