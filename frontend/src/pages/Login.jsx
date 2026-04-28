function Login() {
  return (
    <div className="flex items-center justify-center min-h-[80vh]">

      <div className="bg-white p-8 rounded-2xl shadow-md w-full max-w-md">

        {/* Title */}
        <h2 className="text-2xl font-bold text-center text-gray-800">
          Admin Login
        </h2>

        <p className="text-gray-500 text-center mt-2">
          Access your dashboard securely
        </p>

        {/* Form */}
        <form className="mt-6 space-y-4">

          {/* Email */}
          <div>
            <label className="text-sm text-gray-600">Email</label>
            <input
              type="email"
              placeholder="Enter your email"
              className="w-full mt-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Password */}
          <div>
            <label className="text-sm text-gray-600">Password</label>
            <input
              type="password"
              placeholder="Enter your password"
              className="w-full mt-1 px-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>

          {/* Button */}
          <button className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition">
            Login
          </button>

        </form>
      </div>

    </div>
  );
}

export default Login;