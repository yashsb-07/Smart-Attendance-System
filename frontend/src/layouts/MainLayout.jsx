import Navbar from "../components/Navbar";

function MainLayout({ children }) {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      
      {/* Navbar */}
      <Navbar />

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-6">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-white border-t mt-10">
        <div className="max-w-7xl mx-auto px-4 py-4 text-center text-gray-500 text-sm">
          © 2026 SmartAttend. All rights reserved.
        </div>
      </footer>

    </div>
  );
}

export default MainLayout;