import LandingImage from "../assets/LandingImage.svg";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion"

const Landing = () => {
  const navigate = useNavigate();
  const onGetStarted = () => {
    navigate("/get-started")
  }

  return (
    <div className="flex h-screen w-screen phablet-max:flex-col">
      {/* First Half */}
      <div className="flex flex-col justify-center items-center h-full xl:w-1/2 w-full m-0 bg-[#191919] px-32">
        {/* Content Group */}
        <div className="flex flex-col items-center xl:items-start">
          <h1 className="title !text-white text-center xl:text-left">Welcome to Simplify</h1>
          <label className="subtitle mb-16 text-center xl:text-left">Summarize and shorten any URL with ease</label>
        
          <motion.button whileHover={{ opacity: 0.8 }} className="btn w-80 !text-black !bg-white" onClick={onGetStarted}>
            Get Started
          </motion.button>
        </div>
      </div>

      {/* Second Half */}
      <div className="justify-center items-center hidden xl:flex sm:w-1/2 bg-white">
        <img
          alt="Vectors"
          src={LandingImage}
        />
      </div>
    </div>
  )
}
export default Landing;