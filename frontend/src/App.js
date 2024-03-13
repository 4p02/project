import { Toaster } from "react-hot-toast";
import { Routes, Route } from "react-router-dom";
import {
  Home,
  Auth,
  NotFound,
  Landing,
  GetStarted,
  History,
  StylingGuide
} from "./pages";
import Navbar from "./components/nav/Navbar.js";
import Footer from "./components/footer/Footer.js";
import GlobalContextProvider from "./components/context/GlobalContext.jsx";

function App() {
  
  return (
    <main className="w-screen h-screen bg-light text-dark dark:bg-dark dark:text-light">
      <GlobalContextProvider> 
        <Navbar />
        <Toaster />
        <Routes>
          <Route path="/" element={<Home/>} />
          <Route path="/auth" element={<Auth/>} />
          <Route path="/history" element={<History/>} />
          <Route path="/landing" element={<Landing/>} />
          <Route path="/get-started" element={<GetStarted/>} />
          <Route path="/styling-guide" element={<StylingGuide/>} />
          <Route path="/*" element={<NotFound/>} />
        </Routes>
      </GlobalContextProvider>
      <Footer />
    </main>
  );
}

export default App;
