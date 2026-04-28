import { Link, useLocation } from "react-router-dom";

function Navbar() {
  const location = useLocation();

  const navLinks = [
    { name: "Home", path: "/" },
    { name: "Register", path: "/register" },
    { name: "Attendance", path: "/attendance" },
    { name: "Dashboard", path: "/dashboard" },
  ];

  return (
    <nav className="bg-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 py-3 flex justify-between items-center">
        
        {/* Logo / Brand */}
        <h1 className="text-xl font-bold text-blue-600">
          SmartAttendance
        </h1>

        {/* Navigation Links */}
        <div className="flex gap-6">
          {navLinks.map((link) => (
            <Link
              key={link.path}
              to={link.path}
              className={`font-medium ${
                location.pathname === link.path
                  ? "text-blue-600 border-b-2 border-blue-600"
                  : "text-gray-600 hover:text-blue-500"
              }`}
            >
              {link.name}
            </Link>
          ))}
        </div>

        {/* Login Button */}
        <Link
          to="/login"
          className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
        >
          Login
        </Link>
      </div>
    </nav>
  );
}

export default Navbar;