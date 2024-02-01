import { motion } from "framer-motion"

const FormButton = ({ text, onClick, isSecondary, width, extraClassName }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.02 }}
      onClick={onClick}
      className={`${isSecondary ? "btn-secondary" : "btn"} ${width} ${extraClassName}`}
    >
      {text}
    </motion.button>
  )
}
export default FormButton