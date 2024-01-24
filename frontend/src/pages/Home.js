import toast from "react-hot-toast";

const Home = () => {
  return (
    <div className="flex flex-col items-center justify-center content-center h-full space-y-32">

      <h1 className="text-[54px] font-[600]">This is our temporary home(page) 🏠❤️</h1>

      <button
        onClick={() => toast("There is no toast emoji, so 🍞")}
        className="bg-red-600 text-white px-4 py-2 rounded-xl scale-150"
      >
        Click me for a toast!
      </button>
    </div>
  )
}
export default Home;