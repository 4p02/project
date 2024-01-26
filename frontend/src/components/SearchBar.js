import { FaSearch } from "react-icons/fa";

const SearchBar = ({ onEnter, onChange, value, width }) => {

  // When enter key is pressed, enter the input
  const onKeyDown = (event) => {
    if (event.key == "Enter")
      onEnter();
  }

  return (
    <div className={`flex items-center border-2 border-divider bg-white px-4 py-4 rounded-xl h-min ${width || "w-fit"} space-x-5`}>
      <input
        className="outline-none w-full h-full"
        placeholder="Paste URL to summarize..."
        onChange={onChange}
        value={value}
        onKeyDown={onKeyDown}
      />
      <button
        className="flex items-center scale-150 text-accent"
        onClick={onEnter}
      >
        <FaSearch />
      </button>
    </div>
  )
}
export default SearchBar