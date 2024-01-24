import { Toaster } from "react-hot-toast";
import { Routes, Route } from "react-router-dom";
import {
  Home,
  NotFound
} from "./pages";

function App() {
  return (
    <main className="w-screen h-screen">
      <Toaster />
      <Routes>
        <Route path="/" element={<Home/>} />
        <Route path="/*" element={<NotFound/>} />
      </Routes>
    </main>
  );
}

export default App;
