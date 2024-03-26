import { BiSolidDownArrow, BiSolidRightArrow  } from "react-icons/bi";
import { useState } from "react";

const AccountSection = ({ title, children }) => {
  const [collapsed, setCollapse] = useState(true);
  const toggleCollapse = () => setCollapse(prev => !prev);

  return (
    <div className="border-t-2 border-col border-dark p-2 flex flex-col justify-center items-start text-center w-full h-fit">
      <div className="flex justify-between items-center w-full cursor-pointer" onClick={toggleCollapse}>
        <p className="subtitle text-dark">{title}</p>
        <div className="ml-1.5">
          {collapsed ?
            <BiSolidRightArrow />
          :
            <BiSolidDownArrow />
          }
        </div>
      </div>
      {!collapsed && children}
    </div>
  )
}
export default AccountSection;