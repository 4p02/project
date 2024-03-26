
import { useEffect, useContext, useState } from "react";
import { GlobalContext } from "../components/context/GlobalContext";
import HistoryCard from "../components/HistoryCard";
import { PAGE_SIZE } from "../lib/Constants.js";

const History = () => {
  const { state } = useContext(GlobalContext);
  const [history, setHistory] = useState([]);
  const [page, setPage] = useState(0);

  useEffect(() => {
    // userContext.user 
    if (!state.user) {
      console.error("User not logged in! (something went wrong with context)")
    } else {
      state.user.getLinks(PAGE_SIZE, page * PAGE_SIZE).then(response => {
        console.log(response);
      }).catch(error => {
        console.error(error);}
      )
    }
  }, [page, state]);

  const loadMore = () => {
    setPage(page + 1);
    if (!state.user) {
      console.error("load more: User not logged in! (something went wrong with context)")
      return;
    }
    setHistory(state.user.getLinks(PAGE_SIZE, page * PAGE_SIZE).then(response => {
      console.debug(response);
      return response;
    }).catch(error => {
      console.error(error);
      return []
    }))

  }


  return (
    <div className="page lg-max:p-8 lg:p-20 xl:p-28">
      <div className="flex flex-col w-full">
        <h1 className="title lg-max:text-center">Recently Searched Links</h1>
        <p className="subtitle mb-12 lg-max:text-[1.25rem] lg-max:text-center">Discover the shortened versions of recently searched links for easy sharing and reference.</p>
        <div className="flex justify-center w-full h-fit flex-wrap xl:flex-nowrap phablet-max:space-y-10">
          {history.map((historyItem, index) => 
            <HistoryCard key={index} title={historyItem.title} desc={historyItem.desc} image={"????"} date={historyItem.date}  />
          )}
        </div>
      </div>
    </div>
  )
}
export default History;