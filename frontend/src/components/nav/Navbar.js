// import toast from "react-hot-toast";
import { TiThMenuOutline, TiHome } from "react-icons/ti";
import { IoClose, IoArrowBack } from "react-icons/io5";
import { IoIosSunny, IoIosMoon } from "react-icons/io";
import { BsPersonCircle } from "react-icons/bs";
import { useNavigate, useLocation } from "react-router-dom";
import logo from "../../assets/templogo.png"
import { useContext, useEffect, useState } from "react";
import { GlobalContext } from "../context/GlobalContext";
import { AnimatePresence, motion } from "framer-motion";
import toast from "react-hot-toast";

const Navbar = () => {
  const [showMenu, setShowMenu] = useState(false);
  const [darkMode, setDarkMode] = useState(false)

  const navigate = useNavigate();
  const context = useContext(GlobalContext)
  const { pathname } = useLocation();

  // Button functions
  const onMenuClick = () => setShowMenu(prev => !prev);
  const onAccountClick = () => {context.token ? navigate("/") : navigate("/auth")};
  const onHistoryClick = () => pathname !== "/history" && navigate("/history");
  const onHomeClick = () => pathname !== "/" && navigate("/");
  const onBackClick = () => navigate(-1);
  const onThemeToggle = () => setDarkMode(prev => !prev)
  const onLogOut = () => toast.success("Logged out!");

  // Automatically close menu when route is changed for quality of life
  useEffect(() => {
    setShowMenu(false);
  }, [pathname])

  // Also used to indicate when a user has already visited before
  const landingRoutes = ["/landing", "/get-started", "/auth"];

  useEffect(() => {
    // Indicate user has already visited once before if they are on the landing pages
    if (landingRoutes.findIndex(route => route === pathname) !== -1)
      localStorage.setItem("FIRST_VISIT", "true");
    
    // If the user hasn't visited once before, redirect to landing page
    if (!localStorage.getItem("FIRST_VISIT"))
      navigate("/landing");
  }, []);

  return (landingRoutes.findIndex(route => route === pathname) === -1 &&
    <div className="fixed z-50 bg-white flex justify-between items-center w-screen h-16 border-2 border-b-divider pr-2">
      {/* Logo Group */}
      <div className="flex h-full w-fit items-center justify-between cursor-pointer" onClick={onHomeClick}>
        <img className="h-full mr-2 border-2 border-black" src={logo} alt="Logo" />
        <p className="font-[600] text-[24px] mr-2">Simplify</p>
      </div>

      {/* Icon button menu */}
      <div className="flex h-full items-center px-2 justify-between py-0 w-fit space-x-4">
        
        {/* Back button */}
        <motion.button whileHover={{ scale: 1.1 }} className="phablet-max:hidden w-fit h-fit" onClick={onBackClick}>
          <IoArrowBack className="icon-size" />
        </motion.button>

        {/* Theme toggle button */}
        <motion.button whileHover={{ scale: 1.1 }} className="phablet-max:hidden w-fit h-fit" onClick={onThemeToggle}>
          {darkMode ?
            <IoIosSunny className="icon-size" />
            :
            <IoIosMoon className="icon-size" />
          }
        </motion.button>

        {/* Home button */}
        <motion.button whileHover={{ scale: 1.1 }} className="icon-size" onClick={onHomeClick}>
          <TiHome className="icon-size" />
        </motion.button>

        {/* Account button */}
        <motion.button whileHover={{ scale: 1.1 }} className="phablet-max:hidden w-fit h-fit" onClick={onAccountClick}>
          <BsPersonCircle className="icon-size" />
        </motion.button>

        {/* Menu toggle button */}
        <motion.button whileHover={{ scale: 1.1 }} className="w-fit h-fit flex justify-center" onClick={onMenuClick}>
          {showMenu ?
            <IoClose className="icon-size" />
            :
            <TiThMenuOutline className="icon-size" />
          }
        </motion.button>
      </div>
      
      {/* Vertical nav menu */}
      <AnimatePresence>
        {showMenu && 
          <motion.div
            exit={{ x: "100%" }}
            animate={{ x: 5}}
            initial={{ x: "100%" }}
            transition={{ ease: "linear", duration: 0.05 }}
            className="absolute w-screen sm:w-56 px-2 h-screen right-0 top-full text-center space-y-3 flex flex-col bg-white border-2 border-divider py-6"
          >
            {/* History button */}
            <button className="nav-text-btn" onClick={onHistoryClick} >
              History
            </button>

            {/* Account button */}
            <button className="nav-text-btn" onClick={onAccountClick} >
              {context.token ? "Account" : "Sign In/Up"}
            </button>

            {/* Theme toggle button */}
            <button className="nav-text-btn" onClick={onThemeToggle} >
              {darkMode ? "Light Mode" : "Dark Mode"}
            </button>

            {/* Log out button */}
            {context.token &&
              <button className="nav-text-btn" onClick={onLogOut} >
                Log Out
              </button>
            }
          </motion.div>
        }
      </AnimatePresence>
    </div>
  )
}
export default Navbar;