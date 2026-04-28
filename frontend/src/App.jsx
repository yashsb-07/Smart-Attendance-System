import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import heroImg from './assets/hero.png'
import './App.css'

import { useEffect, useState } from "react";
import API from "./services/api";

function App() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    API.get("test/")
      .then((res) => {
        setMessage(res.data.message);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  return (
    <div className="flex items-center justify-center h-screen">
      <h1 className="text-2xl font-bold text-green-600">
        {message || "Loading..."}
      </h1>
    </div>
  );
}

export default App;
