import HistoryCard from "../components/HistoryCard";
import mockHistory from "../mockHistory.js";

const History = () => {

  return (
    <div className="page lg-max:p-8 lg:p-20 xl:p-28">
      <div className="flex flex-col w-full">
        <h1 className="title lg-max:text-center">Recently Searched Links</h1>
        <p className="subtitle mb-12 lg-max:text-[1.25rem] lg-max:text-center">Discover the shortened versions of recently searched links for easy sharing and reference.</p>
        <div className="flex justify-center w-full h-fit flex-wrap xl:flex-nowrap phablet-max:space-y-10">
          {mockHistory.map((historyItem, index) => 
            <HistoryCard key={index} {...historyItem} />
          )}
        </div>
      </div>
    </div>
  )
}
export default History;