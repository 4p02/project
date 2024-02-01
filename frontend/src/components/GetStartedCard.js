import { motion } from "framer-motion";

const GetStartedCard = ({ title, desc, onClick }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      onClick={onClick}
      className="text-left flex flex-col panel m-3 w-[400px] p-5 h-[250px]"
    >
      <h3 className="title !text-[28px]">{title}</h3>
      {desc.split("\\n").map( (text, i) => 
        <p key={i} className="subtitle !text-[20px]">{text}</p>
      )}
    </motion.button>
  )
}
export default GetStartedCard