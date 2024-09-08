import React from 'react';
import { ArrowRight, CheckCircle } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";
const HomePage = () => {
  const features = [
    { title: 'Automated Grading', description: 'Save time with AI-powered grading' },
    { title: 'Test Management', description: 'Easily create and manage tests' },
    { title: 'Analytics', description: 'Gain insights into student performance' },
    { title: 'Customizable', description: 'Tailor the system to your needs' },
  ];

  const testimonials = [
    { name: 'Dr. Smith', role: 'Professor of Computer Science', quote: 'A+I has revolutionized my grading process.' },
    { name: 'Prof. Johnson', role: 'Mathematics Department Head', quote: 'The analytics provided by A+I are invaluable.' },
  ];

  const faqItems = [
    { question: 'How does A+I work?', answer: 'A+I uses advanced AI algorithms to analyze and grade student work based on customizable criteria set by professors.' },
    { question: 'Is A+I secure?', answer: 'Yes, A+I employs state-of-the-art security measures to protect all user data and student information.' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
    {/* Hero Section */}
    <section className="bg-gradient-to-r from-red-100 to-red-200 py-20">
      <div className="container mx-auto px-4">
        <h1 className="text-4xl md:text-6xl font-bold mb-4 text-gray-900">Welcome to A+I</h1>
        <p className="text-xl md:text-2xl mb-8 text-gray-700">The future of automated grading and test management</p>
        <div className="space-x-4">
          <Button variant="default" size="lg">Sign up as a professor</Button>
          <Button variant="outline" size="lg">Learn More</Button>
        </div>
      </div>
    </section>

    {/* Overview Section */}
    <section className="py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-900">How A+I Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {['Upload Tests', 'AI Grading', 'Review Results'].map((step, index) => (
            <Card key={index}>
              <CardHeader>
                <CardTitle className="text-xl font-semibold text-red-600">{`${index + 1}. ${step}`}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">
                  {index === 0 && "Easily upload your tests and grading criteria to the A+I platform."}
                  {index === 1 && "Our advanced AI algorithms grade student work quickly and accurately."}
                  {index === 2 && "Review grading results and gain insights through detailed analytics."}
                </p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>

    {/* Features Section */}
    <section className="bg-white py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-900">Key Features</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <div key={index} className="flex items-start">
              <CheckCircle className="text-red-500 mr-4 flex-shrink-0" />
              <div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>

    {/* Testimonials Section */}
    <section className="py-16 bg-gray-100">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-900">What Professors Say</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {testimonials.map((testimonial, index) => (
            <Card key={index}>
              <CardContent className="pt-6">
                <p className="text-lg mb-4 text-gray-700">"{testimonial.quote}"</p>
                <p className="font-semibold text-red-600">{testimonial.name}</p>
                <p className="text-sm text-gray-500">{testimonial.role}</p>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </section>

    {/* FAQ Section */}
    <section className="bg-white py-16">
      <div className="container mx-auto px-4">
        <h2 className="text-3xl font-bold mb-8 text-center text-gray-900">Frequently Asked Questions</h2>
        <Accordion type="single" collapsible className="w-full">
          {faqItems.map((item, index) => (
            <AccordionItem key={index} value={`item-${index}`}>
              <AccordionTrigger className="text-left text-lg font-semibold text-gray-800">{item.question}</AccordionTrigger>
              <AccordionContent className="text-gray-600">
                {item.answer}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>

    {/* CTA Section */}
    <section className="bg-red-100 py-16">
      <div className="container mx-auto px-4 text-center">
        <h2 className="text-3xl font-bold mb-4 text-gray-900">Ready to transform your grading process?</h2>
        <p className="text-xl mb-8 text-gray-700">Join A+I today and experience the future of education.</p>
        <Button variant="default" size="lg" className="bg-red-500 hover:bg-red-600">
          Get Started
          <ArrowRight className="ml-2" />
        </Button>
      </div>
    </section>
  </div>
  );
};

export default HomePage;