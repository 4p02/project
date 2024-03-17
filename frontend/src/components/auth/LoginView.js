import Input from "../inputs/Input.js"
import { useEffect, useState, useContext } from "react"
import { useNavigate } from "react-router-dom";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";
import { LoginUser } from "../../api/Auth.js";
import { GlobalContext } from "../context/GlobalContext.jsx";
import { BACKEND_API_URL } from "../../lib/Constants.js";
import toast from "react-hot-toast";
import User from "../../api/User.js";

const LoginView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);
  const {state, dispatch} = useContext(GlobalContext);
  useEffect(() => {
    // check if token exists here so we can avoid this view
    const token = localStorage.getItem("token");
    console.log(error);
    if (token && (!state || !state.user) ) {
        // check if token is valid (maybe in the constructor)
        const userObj = new User(token); 
        dispatch({
          type: "SET_USER",
          payload: {
            user: userObj,
          },
        })
    }
    navigate("/");
  }, [state, dispatch, navigate])
  const onLogInClick = async () => {
    const response = await LoginUser(email, password);
    console.log(response);
    if (!response.token) {
      setError(true);
      return;
    }
    localStorage.setItem("token", response.token);
    toast.success("Logged in successfully!");
    const userObj = new User(response.token);
    dispatch({type: "SET_USER", payload: userObj});
    navigate("/");
  }

  const onGoogleLogin = () => {
    window.location.href = `${BACKEND_API_URL}/auth/google`;
  }
  const onSetEmail = (event) => {
    setEmail(event.target.value);
  }
  const onSetPassword = (event) => {
    setPassword(event.target.value);
  }

  const onGuestClick = () => {
    navigate("/")
  }

  return (
    <div className="panel flex flex-col items-center px-12 w-full *:mb-4 py-6">
      <Input
        onChange={onSetEmail}
        value={email}
        width="w-full"
        placeholder="Enter your email..."
        label="Email"
      />
      
      <Input
        onChange={onSetPassword}
        value={password}
        width="w-full"
        placeholder="Enter your password..."
        type="password"
        label="Password"
      />

      <FormButton
        onClick={onLogInClick}
        width="w-full"
      >
        Log In
      </FormButton>

      <GoogleButton
        onClick={onGoogleLogin}
        text={"Google Log In"}
      />

      <div className="form-ui-group">
        <FormButton
          onClick={onGuestClick}
          isSecondary
          width="form-ui-group-element-width"
        >
          Continue as Guest
        </FormButton>
        <FormButton
          onClick={viewToggle}
          isSecondary
          width="form-ui-group-element-width"
        >
          Register Instead
        </FormButton>
      </div>
    </div>
  )
}
export default LoginView