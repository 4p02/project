const HistoryCard = ({ title, desc, image, date }) => {
  const dateFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' }
  
  return (
    <div className="flex flex-col items-center w-screen h-[412px] phablet:w-[326px] m-1">
      <img className="flex justify-center items-center bg-dark text-light dark:bg-light dark:text-dark rounded-t-xl w-full h-2/5" alt="image" src={image} />
      <div className="h-3/5 w-full p-5 my-2">
        <h6 className="title text-[20px]">{title}</h6>
        <p className="text-[18px] text-dark-gray">{desc.length > 100 ? desc.substring(0, 100) + "..." : desc}</p>
      </div>
      <p className="text-left w-full px-5 text-[18px] text-dark-gray">{date.toLocaleDateString("en-us", dateFormatOptions)}</p>
    </div>
  )
}
export default HistoryCard