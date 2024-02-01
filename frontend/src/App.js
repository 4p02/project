import { Toaster } from "react-hot-toast";
import { Routes, Route } from "react-router-dom";
import {
  Home,
  Auth,
  NotFound,
  Landing,
  GetStarted,
  History
} from "./pages";
import Navbar from "./components/nav/Navbar.js";
import Footer from "./components/footer/Footer.js";

function App() {
  return (
    <main className="w-screen h-screen text-black">
      <Navbar />
      <Toaster />
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/auth" element={<Auth/>} />
        <Route path="/history" element={<History/>} />
        <Route path="/landing" element={<Landing/>} />
        <Route path="/get-started" element={<GetStarted/>} />
        <Route path="/*" element={<NotFound/>} />
      </Routes>
      <Footer />
    </main>
  );
}

export default App;
