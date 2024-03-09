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
    const isLoggedIn = context.user?.checkValidToken() || false;

    if (isLoggedIn) navigate("/");
    if (state?.isSignIn) setLoginPageOrRegister(false);
  }, [])

  return (
    <div className="page !pt-0">
      <h1 className="title text-center">
        {loginPageOrRegister ?
          "Log Into Your Account"
        :
          "Create an Account"
        }
      </h1>
      
      <div className="w-full sm:w-11/12 md:w-3/4 lg:w-3/5">
        {loginPageOrRegister ?
          <LoginView viewToggle={toggleView} />
        :
          <RegisterView viewToggle={toggleView} />
        }
      </div>
    </div>
  )
}
export default Auth;