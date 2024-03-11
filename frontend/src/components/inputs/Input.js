import { FaRegEyeSlash, FaSearch, FaRegEye } from "react-icons/fa";
import { useState } from "react";
import { motion } from "framer-motion"

const Input = ({
  onEnter,
  onChange,
  value,
  width,
  type,  // "search", "password" or null
  placeholder,
  label,
  error = false,
  errorMsg = "",  
  onBlur = () => {},
  onFocus = () => {}
}) => {
  const [showPassword, setShowPassword] = useState(false);

  // When enter key is pressed, enter the input
  const onKeyDown = (event) => {
    if (event.key == "Enter" && onEnter)
      onEnter();
  }


  return (
    <div className={`flex flex-col ${width || "w-fit"}`}>
      {/* Label */}
      {label &&
        <label className="font-[500]">
          {label}
        </label>
      }

      {/* Input Box */}
      <div className={`flex items-center border-2 ${error ? "border-red-500" : "border-dark-gray"} bg-white px-3 py-3 ${type === "search" ? "rounded-2xl" : "rounded-xl"} h-min w-full space-x-5 text-dark`}>
        <input
          className="outline-none w-full h-full"
          placeholder={placeholder}
          onChange={onChange}
          value={value}
          onKeyDown={onKeyDown}
          inputMode={type === "email" ? "email" : "text"}
          type={ (type !== "email" && type) ||
            (type !== "password" && type) || (!showPassword && type) ||  "text"}
          onBlur={onBlur}
          onFocus={onFocus}
        />

        {/* Search Icon */}
        {type === "search" &&
          <motion.button
            whileHover={{ scale: 1.1 }}
            className="flex items-center text-[20px]"
            onClick={onEnter || (() => {})}
          >
            <FaSearch />
          </motion.button>
        }

        {/* Hide/show password button */}
        {type === "password" &&
          <button
            className="flex items-center text-[20px]"
            onClick={() => setShowPassword(prev => !prev)}
          >
          {showPassword ?
            <FaRegEye />
          :
            <FaRegEyeSlash />
          }
          </button>
        }
      </div>
    </div>
  )
}
export default Input