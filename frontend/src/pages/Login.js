import { useEffect, useState, useContext } from "react";
import { GlobalContext } from "../components/context/GlobalContext.jsx";
import { useNavigate } from 'react-router-dom';
import toast from "react-hot-toast";


const Login = () => {
  const [loginPageOrRegister, setLoginPageOrRegister] = useState(true);
  const context = useContext(GlobalContext);
  const navigate = useNavigate();
  
  useEffect(() => {
    if (context.token) {
      navigate("/");
    }
  }, []);

  return (
    <div className="page">
      {loginPageOrRegister ?
        <p className="text-[54px] font-[600]">This is a 🪵 in page!</p>
      :
        <>
          <p className="text-[54px] font-[600]">This is a register page! token: {context.token} full_name: {context.full_name} email: {context.email}</p>
          <p className="text-[24px] font-[600]">Cha ching!&nbsp;
            <button className="text-[20px] underline" onClick={() => toast("Because cash registers 💸")}>Get it?</button>
          </p>
        </>
      }

      <p className="text-[20px] mt-2">
        {loginPageOrRegister ? "Don't have an account? " : "Already have an account? " }
        <button
          onClick={() => setLoginPageOrRegister(prev => !prev)}
          className="text-accent text-[20px]"
        >
          Click on me!
        </button>
      </p>

    </div>
  )
}
export default Login;