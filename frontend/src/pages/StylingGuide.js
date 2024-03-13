import { FaCopy } from "react-icons/fa"
import { motion } from "framer-motion"
import FormButton from "../components/auth/FormButton"

const StylingGuide = () => {
  
  const PaletteColor = ({ color, hasBorder }) => 
    <motion.div
      whileHover={{ scale: 1.1 }}
      className={`icon-size rounded-lg ${color} ${hasBorder ? "border-col border-2" : ""}`}
    >
    </motion.div>

  return (
    <div className="page">
      <h1 className="title">This is a title</h1>
      <p className="subtitle">This is a subtitle</p>
      <div className="flex w-2/3 space-x-2 justify-center my-4">
        <FormButton
          extraClassName="px-8"
          width="w-1/3"
        >
          Primary button
        </FormButton>
        <FormButton
          width="w-1/3"
          extraClassName="px-8"
          isSecondary
        >
          Secondary button
        </FormButton>
      </div>

      <h1 className="title">Palette</h1>
      <div className="flex space-x-2 rounded-lg justify-center w-fit p-2 ">
        <PaletteColor color="bg-dark-complement"/>
        <PaletteColor color="bg-dark-light"/>
        <PaletteColor color="bg-dark" hasBorder />
        <PaletteColor color="bg-light" hasBorder />
        <PaletteColor color="bg-dark-gray"/>
        <PaletteColor color="bg-light-gray"/>
        <PaletteColor color="bg-red-600"/>
      </div>

      <div className="panel justify-between w-1/2 my-4 py-3 h-16 px-4 flex items-center dark:bg-light">
        <p className="text-[16px] text-dark-gray">Shortened link will appear here!</p>
        
        <motion.button whileHover={{ scale: 1.2 }} className="text-[24px] dark:text-dark">
          <FaCopy />
        </motion.button>
      </div>
      <div className="panel my-4 h-[calc(100vh-8rem)] w-1/2 overflow-y-hidden relative">
        <div className="panel overflow-y-auto overflow-x-hidden h-full p-4 dark:bg-light dark:text-dark">
          <p className="text-[16px] text-dark-gray">Summary will appear here!</p>

          <motion.button whileHover={{ scale: 1.2 }} className="text-[24px] absolute top-2 right-2">
            <FaCopy />
          </motion.button>
        </div>
      </div>
    </div>
  )
}

export default StylingGuide