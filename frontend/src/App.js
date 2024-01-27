import { Toaster } from "react-hot-toast";
import { Routes, Route } from "react-router-dom";
import {
  Home,
  Login,
  Summary,
  NotFound
} from "./pages";
import Navbar from "./components/nav/Navbar.js";
import Footer from "./components/footer/Footer.js";

function App() {
  return (
    <main className="w-screen h-screen text-fg">
      <Navbar />
      <Toaster />
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/login" element={<Login/>} />
        <Route path="/summary" element={<Summary/>} />
        <Route path="/*" element={<NotFound/>} />
      </Routes>
      <Footer />
    </main>
  );
}

export default App;
