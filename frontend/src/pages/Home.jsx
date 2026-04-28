function Home() {
  return (
    <div>

        {/* HERO SECTION */}
        <section className="text-center py-16">
            <h1 className="text-4xl font-bold text-gray-800">
            Smart Attendance System
            </h1>
            <p className="text-gray-600 mt-4 max-w-xl mx-auto">
            AI-powered face recognition attendance system designed for modern colleges.
            </p>

            <div className="mt-6 flex justify-center gap-4">
            <button className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition">
                Get Started
            </button>
            <button className="border px-6 py-2 rounded-lg hover:bg-gray-100 transition">
                Learn More
            </button>
            </div>
        </section>

        {/* FEATURES */}
        <section className="py-10">
            <h2 className="text-2xl font-semibold text-center mb-8">
                Features
            </h2>

            <div className="grid md:grid-cols-3 gap-6">
                
                <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
                <h3 className="font-semibold text-lg">Face Recognition</h3>
                <p className="text-gray-600 mt-2">
                    Automatically detect and mark attendance using AI.
                </p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
                <h3 className="font-semibold text-lg">Real-Time Tracking</h3>
                <p className="text-gray-600 mt-2">
                    Monitor attendance instantly from dashboard.
                </p>
                </div>

                <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
                <h3 className="font-semibold text-lg">Reports & Analytics</h3>
                <p className="text-gray-600 mt-2">
                    Export attendance data with insights.
                </p>
                </div>

            </div>
        </section>

    </div>
  );
}

export default Home;