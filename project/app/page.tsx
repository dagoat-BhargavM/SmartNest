"use client";

import { motion } from "framer-motion";
import { useInView } from "react-intersection-observer";
import { Button } from "@/components/ui/button";
import { MonitorCheck, MessageCircle, FileCheck } from "lucide-react";
import Link from "next/link";

export default function Home() {
  const [ref, inView] = useInView({
    triggerOnce: true,
    threshold: 0.1,
  });

  return (
    <main className="min-h-screen">
      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center">
        <div className="absolute inset-0 bg-gradient-to-b from-background/80 to-background/20 z-10" />
        <div 
          className="absolute inset-0 z-0" 
          style={{
            backgroundImage: "url('https://images.unsplash.com/photo-1551434678-e076c223a692?q=80&w=2070')",
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        />
        
        <div className="relative z-20 text-center px-4 max-w-4xl mx-auto">
          <motion.h1
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-4xl md:text-6xl font-bold mb-6"
          >
            Get a Free Risk Score
          </motion.h1>
          <motion.p
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="text-xl md:text-2xl mb-8 text-muted-foreground"
          >
            Fast, free, Risk Tolerance calculator.
          </motion.p>
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.4 }}
          >
            <Link href="/onboarding">
              <Button size="lg" className="text-lg px-8 py-6">
                Get Started
              </Button>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Three Steps Section */}
      <section ref={ref} className="py-24 bg-background">
        <div className="container mx-auto px-4">
          <motion.h2
            initial={{ opacity: 0, y: 20 }}
            animate={inView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.8 }}
            className="text-3xl md:text-4xl font-bold text-center mb-16"
          >
            Three Steps to AI Financial Planning
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-12">
            {[
              {
                icon: <MonitorCheck className="w-12 h-12" />,
                title: "Build Your Free Financial Plan",
                description:
                  "No phone number. No account. Less than 5 minutes. AI removes bias from traditional planning and delivers personalized financial education based on your answers.",
              },
              {
                icon: <MessageCircle className="w-12 h-12" />,
                title: "Discuss With Our AI Financial Advisor",
                description:
                  "Refine your plan with our AI Financial Advisor, a powerful financial planning tool. Thought-provoking interactions designed to challenge and inspire you.",
              },
              {
                icon: <FileCheck className="w-12 h-12" />,
                title: "Get Expert Insights & News Data",
                description:
                  "Get expert insights and news data to help you make better financial decisions. Our AI Financial Advisor will help you stay on track and reach your goals.",
              },
            ].map((step, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={inView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.8, delay: index * 0.2 }}
                className="flex flex-col items-center text-center p-6 rounded-lg bg-card hover:shadow-lg transition-shadow"
              >
                <div className="mb-6 text-primary">{step.icon}</div>
                <h3 className="text-xl font-semibold mb-4">{step.title}</h3>
                <p className="text-muted-foreground">{step.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}