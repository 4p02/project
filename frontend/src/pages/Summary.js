import { useLocation } from "react-router-dom";
import { FaCopy } from "react-icons/fa";
import toast from "react-hot-toast";

const Summary = () => {
  const { state } = useLocation();
  const { url, summary } = state;

  const onLinkCopy = () => {
    navigator.clipboard.writeText(url);
    toast("Copied link to clipboard!", { icon: "📋" });
  }

  const onSummaryCopy = () => {
    navigator.clipboard.writeText(summary);
    toast("Copied summary to clipboard!", { icon: "📋" });
  }

  return (
    <div className="page">
      <h1 className="text-[54px] font-[600]">This is a temporary page till the summary design is added 😊</h1>
      
      <div
        className="relative w-11/12 items-center bg-white py-2 rounded-xl border-2 border-divider h-min flex justify-center text-center cursor-pointer"
        onClick={onLinkCopy}
      >
        <p className="text-[20px] font-[600] absolute left-2">Shortened URL:</p>
        <p className="w-[70ch] text-[32px] font-[400] text-accent">
          {url.length > 70 ? `${url.substring(0, 67)}...` : url}
        </p>
        <FaCopy className="text-[24px] text-accent absolute right-2" />
      </div>
      
      <p className="text-[32px] font-[600] mt-6">Summary</p>
      <div className="relative w-11/12 min-h-fit h-full bg-white p-8 rounded-xl border-2 border-divider flex text-center">
        <p className="text-[24px] font-[400]">{summary}</p>
        <button className="text-[24px] text-accent absolute top-2 right-2" onClick={onSummaryCopy}>
          <FaCopy />
        </button>
      </div>
    </div>
  )
}
export default Summary;