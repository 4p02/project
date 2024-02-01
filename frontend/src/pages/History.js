import HistoryCard from "../components/HistoryCard";
import mockHistory from "../mockHistory.js";

const History = () => {

  return (
    <div className="page min-h-screen !h-fit p-28">
      <div className="flex flex-col w-full">
        <h1 className="title">Recently Searched Links</h1>
        <p className="subtitle mb-12">Discover the shortened versions of recently searched links for easy sharing and reference.</p>
        <div className="flex justify-center w-full flex-wrap">
          {mockHistory.map((historyItem, index) => 
            <HistoryCard key={index} {...historyItem} />
          )}
        </div>
      </div>
    </div>
  )
}
export default History;