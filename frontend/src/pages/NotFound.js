import { useNavigate } from "react-router-dom"
import { IoMdArrowRoundBack } from "react-icons/io";

const NotFound = () => {
  const navigate = useNavigate();

  return (
    <div className="page">
      <h1 className="text-[54px] font-[600]">This page is not a thing.</h1>

      <button
        onClick={() => navigate("/")}
        className="btn mt-6 px-4 py-2 rounded-xl scale-150 flex items-center"
      >
        <IoMdArrowRoundBack className="mr-2" /> Go Home
      </button>
    </div>
  )
}
export default NotFound