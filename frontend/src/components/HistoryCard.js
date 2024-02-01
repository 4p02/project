const HistoryCard = ({ title, desc, image, date }) => {
  const dateFormatOptions = { year: 'numeric', month: 'short', day: 'numeric' }
  
  return (
    <div className="flex flex-col items-center h-[412px] w-[326px] m-1">
      <img className="flex justify-center items-center bg-[#191919] rounded-t-xl text-white w-full h-2/5" alt="image" src={image} />
      <div className="h-3/5 w-full p-5">
        <h6 className="title text-[20px]">{title}</h6>
        <p className="text-[18px] text-gray-500">{desc}</p>
      </div>
      <p className="text-left w-full px-5 text-[18px] text-gray-500">{date.toLocaleDateString("en-us", dateFormatOptions)}</p>
    </div>
  )
}
export default HistoryCard