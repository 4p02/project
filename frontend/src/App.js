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
import GlobalContextProvider from "./components/context/GlobalContext.jsx";

function App() {
  
  return (
    <main className="w-screen h-screen text-fg">
        <Toaster />
        <GlobalContextProvider>            
            <Navbar />
            <Routes>
              <Route path="/" element={<Home/>} />
              <Route path="/login" element={<Login/>} />
              <Route path="/summary" element={<Summary/>} />
              <Route path="/*" element={<NotFound/>} />
            </Routes>
            <Footer />
        </GlobalContextProvider>
    </main>
  );
}

export default App;
