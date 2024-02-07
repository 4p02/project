import toast from "react-hot-toast";
import Input from "../components/Input.js";
import { useState } from "react";
import { FaCopy } from "react-icons/fa";
import { motion } from "framer-motion"
import FormButton from "../components/auth/FormButton.js";

const Home = () => {
  const [inputURLValue, setInputURLValue] = useState("");
  const [url, setURL] = useState("");
  const [summary, setSummary] = useState("");

  const onLinkCopy = () => {
    if (!url.trim()) { toast.error("There's nothing to copy!"); return; }
    navigator.clipboard.writeText(url);
    toast("Copied link to clipboard!", { icon: "📋" });
  }

  const onSummaryCopy = () => {
    if (!summary.trim()) { toast.error("There's nothing to copy!"); return; }
    navigator.clipboard.writeText(summary);
    toast("Copied summary to clipboard!", { icon: "📋" });
  }
  
  const onSummarizeClick = async () => {
    // Invalid URL entered, indicate so and return
    if (!inputURLValue.trim()) {
      toast.error("Enter something!");
      return;
    }

    // Send POST request to backend here
    setURL("This is a temp URL!");
    setSummary("This is a temp summary, lorem ipsum or whatever and what not and blah blah blah")
  }

  return (
    <div className="page items-start h-fit px-6 lg:p-20 lg:space-x-16 lg:flex-row ">
      {/* Left section */}
      <div className="h-full flex flex-col w-full lg:w-1/2">
        <h1 className="title lg-max:text-center">Simplify Your Links</h1>
        <p className="subtitle text-[1.25rem] mb-5 lg-max:text-center">Enter the URL you want to summarize and shorten below. Simplify will generate a short link and a concise summary for you.</p>
        <Input
          onEnter={onSummarizeClick}
          onChange={(event) => setInputURLValue(event.target.value)}
          value={inputURLValue}
          width="w-full"
          type="search"
          placeholder="Enter a URL..."
        />
        <FormButton
          onClick={onSummarizeClick}
          extraClassName="mt-6 mb-3"
        >
          Submit
        </FormButton>

        <h1 className="title mt-auto lg-max:text-center lg-max:mt-6">Short Link</h1>
        <div className="mb-auto panel justify-between py-3 h-16 px-4 flex items-center">
          {url ?
            <p className="text-[16px]">{url}</p>
          :
            <p className="text-[16px] text-gray-400">Shortened link will appear here!</p>
          }
          
          <motion.button whileHover={{ scale: 1.2 }} className="text-[24px]" onClick={onLinkCopy}>
            <FaCopy />
          </motion.button>
        </div>
      </div>
      
      {/* Right section */}
      <div className="h-full flex flex-col w-full lg:w-1/2">
        <h1 className="title lg-max:text-center lg-max:mt-6">Summary</h1>
        <div className="panel h-full relative py-6 px-6">
          {summary ?
            <p className="text-[16px]">{summary}</p>
          :
            <p className="text-[16px] text-gray-400">Summary will appear here!</p>
          }
          <motion.button whileHover={{ scale: 1.2 }} className="text-[24px] absolute top-2 right-2" onClick={onSummaryCopy}>
            <FaCopy />
          </motion.button>
        </div>
      </div>
    </div>
  )
}
export default Home;