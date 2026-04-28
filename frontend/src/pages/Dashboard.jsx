function Dashboard() {
  return (
    <div>

      {/* Header */}
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Dashboard Overview
      </h1>

      {/* Cards */}
      <div className="grid md:grid-cols-3 gap-6">

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-gray-500">Total Students</h3>
          <p className="text-2xl font-bold">120</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-gray-500">Present Today</h3>
          <p className="text-2xl font-bold text-green-600">98</p>
        </div>

        <div className="bg-white p-6 rounded-xl shadow hover:shadow-lg transition">
          <h3 className="text-gray-500">Absent Today</h3>
          <p className="text-2xl font-bold text-red-600">22</p>
        </div>

      </div>

    </div>
  );
}

export default Dashboard;