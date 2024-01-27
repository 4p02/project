import toast from "react-hot-toast";
import { TiThMenuOutline, TiHome } from "react-icons/ti";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../../assets/templogo.png"
import { useContext } from "react";
import { GlobalContext } from "../context/GlobalContext";

const Navbar = () => {
  const navigate = useNavigate();
  const context = useContext(GlobalContext)
  const { pathname } = useLocation();
  const onMenuClick = () => toast.error("Not a thing yet!")
  const onLogInClick = () => navigate("/login");
  const onHomeClick = () => navigate("/");

  return (
    <div className="fixed bg-white flex justify-between items-center w-screen h-16 border-2 border-b-divider z-50">
      {/* Logo Group */}
      <div className="flex h-full w-fit items-center justify-between cursor-pointer" onClick={onHomeClick}>
        <img className="h-full mr-2 outline" src={logo} alt="Logo" />
        <p className="font-[600] text-[24px] mr-2">Shortify</p>
        <TiHome className="font-[600] text-[24px]" />
      </div>

      {/* Button Group */}
      <div className="flex h-full items-center px-5 justify-between space-x-7">
        <button className={`nav-text-btn ${pathname === "/" && "text-accent"}`} onClick={onHomeClick}>
          Home
        </button>

        {/* Vertical Divider */}
        <div className="nav-text-btn-divider"></div>
        {
          context.token ? ( 
            <>
            <p>{context.full_name ? context.full_name : "unknown"}</p>
            </>
          ) : (
            <>
            <button className={`nav-text-btn ${pathname === "/login" && "text-accent"}`} onClick={onLogInClick}>
              Log In/Register
            </button>
            </>
          )
        }
        

        {/* WILL BE ADDED WITH MOBILE VIEW STAGE */}
        {/* Vertical Divider */}
        {/* <div className="nav-text-btn-divider"></div>

        <button className="w-10 h-10 flex justify-center m-2" onClick={onMenuClick}>
          <TiThMenuOutline className="w-10 h-10" />
        </button> */}
      </div>
    </div>
  )
}
export default Navbar;