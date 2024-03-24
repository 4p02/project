import toast from "react-hot-toast";
import Input from "../components/inputs/Input.js";
import { useState, useContext } from "react";
import { FaCopy } from "react-icons/fa";
import { motion } from "framer-motion"
import FormButton from "../components/auth/FormButton.js";
import { GlobalContext } from "../components/context/GlobalContext.jsx";
import Summarize from "../api/Summarize.js";

const Home = () => {
  const [inputURLValue, setInputURLValue] = useState("");
  const [url, setURL] = useState("");
  const [summary, setSummary] = useState("");
  const userContext = useContext(GlobalContext);

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
  
    const summaryObj = new Summarize(userContext && userContext.user && userContext.user.token ? userContext.user.token : null);
    // check if link is yt video or not 
    const youtubeRegex = /^(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
    if (youtubeRegex.test(inputURLValue)) {
      const responseJSON = await summaryObj.summerizeVideo(inputURLValue);
      console.debug(responseJSON);
      if (responseJSON === null || responseJSON === undefined || responseJSON.shortLink === null || responseJSON.summary === null) {
        toast.error("Error #1");
        return;
      }
      setURL(responseJSON.shortLink);
      setSummary(responseJSON.summary); 
      
    } else {
      const responseJSON = await summaryObj.summerizeArticle(inputURLValue);
      console.log(responseJSON);
      if (responseJSON === null || responseJSON === undefined || responseJSON.shortLink === null || responseJSON.summary === null) {
        toast.error("Error #1");
        return;
      }
      setURL(responseJSON.shortLink);
      setSummary(responseJSON.summary);
      
    }

  }

  return (
    <div className="page items-start h-fit px-6 lg:p-20 lg:space-x-16 lg:flex-row">
      {/* Left section */}
      <div className="h-min min-h-[calc(100vh-8rem)] flex flex-col w-full lg:w-1/2">
        <h1 className="title lg-max:text-center">Shorten Your Link</h1>
        <p className="subtitle text-[1.25rem] mb-5 lg-max:text-center">Enter the URL you want to summarize and shorten below. Summarily will generate a short link and a concise summary for you.</p>
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
        <div className="panel justify-between py-3 h-16 px-4 flex items-center dark:bg-light">
          {url ?
            <p className="text-[16px] text-dark">{url}</p>
          :
            <p className="text-[16px] text-dark-gray">Shortened link will appear here!</p>
          }
          
          <motion.button whileHover={{ scale: 1.2 }} className="text-[24px] dark:text-dark" onClick={onLinkCopy}>
            <FaCopy />
          </motion.button>
        </div>
      </div>
      
      {/* Right section */}
      <div className="h-[calc(100vh-8rem)] flex flex-col w-full lg:w-1/2">
        <h1 className="title lg-max:text-center lg-max:mt-6">Summary</h1>
        <div className="panel h-full w-full overflow-y-hidden relative">
          <div className="panel overflow-y-auto overflow-x-hidden h-full p-4 dark:bg-light dark:text-dark">
            {summary ?
              <p className="text-[16px]">{summary}</p>
            :
              <p className="text-[16px] text-dark-gray">Summary will appear here!</p>
            }

            <motion.button whileHover={{ scale: 1.2 }} className="text-[24px] absolute top-2 right-2" onClick={onSummaryCopy}>
              <FaCopy />
            </motion.button>
          </div>
        </div>
      </div>
    </div>
  )
}
export default Home;