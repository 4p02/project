import { motion } from "framer-motion";

const GetStartedCard = ({ title, desc, onClick }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      onClick={onClick}
      className="bg-dark-light text-left flex flex-col panel w-[90vw] m-6 phablet:m-3 phablet:w-[400px] p-5 h-[250px]"
    >
      <h3 className="title dark:text-dark text-white !text-[28px]">{title}</h3>
      {desc.split("\\n").map( (text, i) => 
        <p key={i} className="subtitle dark:text-dark-gray text-light-gray !text-[20px]">{text}</p>
      )}
    </motion.button>
  )
}
export default GetStartedCard