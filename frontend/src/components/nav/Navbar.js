// import toast from "react-hot-toast";
import { TiThMenuOutline, TiHome } from "react-icons/ti";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../../assets/templogo.png"
import { useEffect } from "react";

const Navbar = () => {
  const navigate = useNavigate();
  const { pathname } = useLocation();
  // const onMenuClick = () => toast.error("Not a thing yet!")
  const onLogInClick = () => navigate("/auth");
  const onHistoryClick = () => navigate("/history");
  const onHomeClick = () => navigate("/");

  // Also used to indicate when a user has already visited before
  const landingRoutes = ["/landing", "/get-started", "/auth"];

  useEffect(() => {
    // Indicae user has already visited once before if they are on the landing pages
    if (landingRoutes.findIndex(route => route === pathname) !== -1)
      localStorage.setItem("FIRST_VISIT", "true");
    
    // If the user hasn't visited once before, redirect to landing page
    if (!localStorage.getItem("FIRST_VISIT"))
      navigate("/landing");
  }, []);

  return (landingRoutes.findIndex(route => route === pathname) === -1 &&
    <div className="fixed bg-white flex justify-between items-center w-screen h-16 border-2 border-b-divider z-50">
      {/* Logo Group */}
      <div className="flex h-full w-fit items-center justify-between cursor-pointer" onClick={onHomeClick}>
        <img className="h-full mr-2 outline" src={logo} alt="Logo" />
        <p className="font-[600] text-[24px] mr-2">Simplify</p>
        <TiHome className="font-[600] text-[24px]" />
      </div>

      {/* Button Group */}
      <div className="flex h-full items-center px-5 justify-between space-x-7">
        <button className={`nav-text-btn ${pathname === "/" && "underline"}`} onClick={onHomeClick}>
          Home
        </button>

        {/* Vertical Divider */}
        <div className="nav-text-btn-divider"></div>

        <button className={`nav-text-btn ${pathname === "/history" && "underline"}`} onClick={onHistoryClick}>
          History
        </button>

        {/* Vertical Divider */}
        <div className="nav-text-btn-divider"></div>

        <button className={`nav-text-btn ${pathname === "/auth" && "underline"}`} onClick={onLogInClick}>
          Log In/Register
        </button>

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