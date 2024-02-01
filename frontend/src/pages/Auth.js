import { useEffect, useState, useContext } from "react";
import { useLocation } from "react-router-dom";
import RegisterView from "../components/auth/RegisterView.js";
import LoginView from "../components/auth/LoginView.js";
import { useNavigate } from 'react-router-dom';
import { GlobalContext } from "../components/context/GlobalContext.jsx";

const Auth = () => {
  const [loginPageOrRegister, setLoginPageOrRegister] = useState(true);
  const { state } = useLocation();
  const context = useContext(GlobalContext);
  const navigate = useNavigate();

  const toggleView = () => setLoginPageOrRegister(prev => !prev)

  useEffect(() => {
    if (context.token) navigate("/");
    if (state?.isSignIn) setLoginPageOrRegister(false);
  }, [])

  return (
    <div className="page !pt-2 justify-center">
      <h1 className="title !text-[64px]">
        {loginPageOrRegister ?
          "Log into Your Account"
        :
          "Create an Account"
        }
      </h1>
      
      {loginPageOrRegister ?
        <LoginView viewToggle={toggleView} />
      :
        <RegisterView viewToggle={toggleView} />
      }
    </div>
  )
}
export default Auth;