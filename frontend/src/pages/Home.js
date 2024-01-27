import toast from "react-hot-toast";
import SearchBar from "../components/SearchBar.js";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import LoadingScreen from "./Loading.js";
import {LinearGradient} from 'react-text-gradients';

const Home = () => {
  const [inputURLValue, setInputURLValue] = useState("");
  const navigate = useNavigate();

  const onSummarizeClick = () => {
    // Invalid URL entered, indicate so and return
    if (!inputURLValue.trim()) {
      toast.error("Enter a valid link!");
      return;
    }

    // Send POST request to backend here
    // When response recieved, redirect to summarize page
      // Include data recieved back in query when redirecting

    navigate("/summary", {
      state: {
        url: "/login",
        summary: "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Eleifend quam adipiscing vitae proin sagittis nisl rhoncus. Sed libero enim sed faucibus turpis in. Rhoncus mattis rhoncus urna neque viverra justo nec ultrices. Diam donec adipiscing tristique risus nec feugiat in. Ultrices mi tempus imperdiet nulla malesuada pellentesque elit eget gravida. Id volutpat lacus laoreet non curabitur gravida arcu ac. Tellus cras adipiscing enim eu turpis. Risus quis varius quam quisque id. Platea dictumst quisque sagittis purus sit amet volutpat consequat mauris. Libero id faucibus nisl tincidunt eget nullam non. In dictum non consectetur a erat. Fringilla est ullamcorper eget nulla facilisi etiam dignissim diam quis. Lectus urna duis convallis convallis tellus id. Sed turpis tincidunt id aliquet risus feugiat in. Ac turpis egestas sed tempus. Felis bibendum ut tristique et egestas quis. In hac habitasse platea dictumst quisque sagittis purus."
      }
    });

    // Temp for now
    toast(inputURLValue);
  }

  return (
    <div className="page">
      <h1>
          <LinearGradient style={{fontSize: 30}} gradient={['to right', '#FF9124, #CCA1CF']}>
            Temporary
          </LinearGradient>
    </h1>
      <label className="text-[36px] font-[600] mb-20">Search something up!</label>
      
      <SearchBar
        onChange={(e) => setInputURLValue(e.target.value)} value={inputURLValue}
        onEnter={onSummarizeClick}
        width="w-1/2"
      />
      <button
        onClick={onSummarizeClick}
        className="bg-accent text-white mb-auto text-[32px] mt-8 px-8 py-2 rounded-xl"
      >
        Summarize!
      </button>
    </div>
  )
}
export default Home;