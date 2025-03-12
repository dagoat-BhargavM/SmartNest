const StepsSection: React.FC = () => {
    return (
      <section className="py-16 text-center bg-gray-100">
        <h2 className="text-3xl font-bold text-gray-900">Three Steps to AI Financial Planning</h2>
        <div className="flex flex-col md:flex-row gap-8 justify-center mt-8">
          <div className="bg-white p-6 shadow-lg rounded-lg">
            <h3 className="text-xl font-semibold">Step 1: Answer Questions</h3>
            <p className="mt-2 text-gray-600">Provide details about your financial goals.</p>
          </div>
          <div className="bg-white p-6 shadow-lg rounded-lg">
            <h3 className="text-xl font-semibold">Step 2: AI Analysis</h3>
            <p className="mt-2 text-gray-600">Our AI analyzes your data to create a tailored plan.</p>
          </div>
          <div className="bg-white p-6 shadow-lg rounded-lg">
            <h3 className="text-xl font-semibold">Step 3: Implement Plan</h3>
            <p className="mt-2 text-gray-600">Follow the plan to achieve financial success.</p>
          </div>
        </div>
      </section>
    );
  };
  
  export default StepsSection;
  