import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import RegisterView from "../components/auth/RegisterView.js";
import LoginView from "../components/auth/LoginView.js";

const Auth = () => {
  const [isLogin, setIsLogin] = useState(true);
  const { state } = useLocation();

  const toggleView = () => setIsLogin(prev => !prev)

  useEffect(() => {
    if (state?.isSignIn) setIsLogin(false);
  }, [])

  return (
    <div className="page !pt-2 justify-center">

      <h1 className="title !text-[64px]">
        {isLogin ?
          "Log into Your Account"
        :
          "Create an Account"
        }
      </h1>
      
      {isLogin ?
        <LoginView viewToggle={toggleView} />
      :
        <RegisterView viewToggle={toggleView} />
      }
    </div>
  )
}
export default Auth;