import { useState } from "react";
import toast from "react-hot-toast";

const Login = () => {
  const [isLogin, setIsLogin] = useState(true);

  return (
    <div className="page">
      {isLogin ?
        <p className="text-[54px] font-[600]">This is a 🪵 in page!</p>
      :
        <>
          <p className="text-[54px] font-[600]">This is a register page!</p>
          <p className="text-[24px] font-[600]">Cha ching!&nbsp;
            <button className="text-[20px] underline" onClick={() => toast("Because cash registers 💸")}>Get it?</button>
          </p>
        </>
      }

      <p className="text-[20px] mt-2">
        {isLogin ? "Don't have an account? " : "Already have an account? " }
        <button
          onClick={() => setIsLogin(prev => !prev)}
          className="text-accent text-[20px]"
        >
          Click on me!
        </button>
      </p>

    </div>
  )
}
export default Login;