function Register() {
  return (
    <div className="flex justify-center min-h-[80vh]">

      <div className="bg-white p-8 rounded-2xl shadow-md w-full max-w-md transition duration-300 hover:shadow-lg">

        <h2 className="text-2xl font-bold text-center text-gray-800">
          Student Registration
        </h2>

        <p className="text-gray-500 text-center mt-2">
          Register your details and capture your face
        </p>

        <form className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">

          <input className="input" placeholder="Full Name" />
          <input className="input" placeholder="Roll Number" />
          <input className="input" placeholder="Department" />
          <input className="input" placeholder="Class" />
          <input className="input" placeholder="Semester" />

          {/* Full width */}
          <div className="md:col-span-2">
            <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
              Register & Capture Face
            </button>
          </div>

        </form>

      </div>

    </div>
  );
}

export default Register;