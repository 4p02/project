import { motion } from "framer-motion"

const FormButton = ({ children, onClick, isSecondary, width, extraClassName, disabled }) => {
  return (
    <motion.button
      whileHover={{ scale: 1.01 }}
      onClick={onClick}
      disabled={disabled}
      className={`${isSecondary ? "btn-secondary" : "btn"} ${width} ${extraClassName}`}
    >
      {children}
    </motion.button>
  )
}
export default FormButton