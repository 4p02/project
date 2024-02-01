import LandingImage from "../assets/LandingImage.svg";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion"

const Landing = () => {
  const navigate = useNavigate();
  const onGetStarted = () => {
    navigate("/get-started")
  }

  return (
    <div className="flex h-screen w-screen">
      {/* First Half */}
      <div className="flex flex-col justify-center items-center h-full w-1/2 m-0 bg-[#191919] px-32">

        {/* Content Group */}
        <div className="flex flex-col">
          <h1 className="title !text-white">Welcome to Simplify</h1>
          <label className="subtitle mb-16">Summarize and shorten any URL with ease</label>
        
          <motion.button whileHover={{ opacity: 0.8 }} className="btn w-80 !text-black !bg-white" onClick={onGetStarted}>
            Get Started
          </motion.button>
        </div>
      </div>

      {/* Second Half */}
      <div className="flex justify-center items-center w-1/2 bg-white">
        <img
          alt="Vectors"
          src={LandingImage}
        />
      </div>
    </div>
  )
}
export default Landing;