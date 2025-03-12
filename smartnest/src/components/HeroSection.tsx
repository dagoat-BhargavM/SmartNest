import Image from "next/image";

const HeroSection: React.FC = () => {
  return (
    <div className="relative w-full h-[500px] bg-gray-900 text-white flex flex-col items-center justify-center text-center">
      {/* Background Grid */}
      <div className="absolute inset-0 grid grid-cols-3 md:grid-cols-5 gap-1 opacity-40">
        <Image src="/images/1.jpg" alt="Elderly couple" width={400} height={300} className="w-full h-full object-cover" />
        <Image src="/images/2.jpg" alt="Woman working" width={400} height={300} className="w-full h-full object-cover" />
        <Image src="/images/3.jpg" alt="Couple using phone" width={400} height={300} className="w-full h-full object-cover hidden md:block" />
        <Image src="/images/4.jpg" alt="Happy girl" width={400} height={300} className="w-full h-full object-cover hidden md:block" />
        <Image src="/images/5.jpg" alt="Excited man" width={400} height={300} className="w-full h-full object-cover" />
      </div>

      {/* Overlay Text */}
      <div className="relative z-10 px-6">
        <h1 className="text-4xl md:text-5xl font-bold">Get a Free Financial Plan</h1>
        <p className="mt-4 text-lg">Fast, free, unbiased financial education. 25,000+ 5-star reviews.</p>
        <button className="mt-6 bg-teal-500 hover:bg-teal-600 text-white font-semibold py-3 px-6 rounded-lg">
          Get Started
        </button>
      </div>
    </div>
  );
};

export default HeroSection;