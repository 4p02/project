import Input from "../Input.js"
import { useEffect, useState, useContext } from "react"
import { useNavigate } from "react-router-dom";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";
import { LoginUser } from "../../api/Auth.js";
import { GlobalContext } from "../context/GlobalContext.jsx";

const LoginView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const userContext = useContext(GlobalContext);
  useEffect(() => {
    // check if token exists here so we can avoid this view
    const userObj = userContext.user;

  }, [])
  const onLogInClick = () => {
    const response = LoginUser(email, password)
    // handle response
  }

  const onGoogleLogin = () => {
    window.location.href = `${BACKEND_API_URL}/auth/google`;
  }

  const onGuestClick = () => {
    navigate("/")
  }

  return (
    <div className="panel flex flex-col items-center px-12 w-full *:mb-4 py-6">
      <Input
        onChange={(event) => setEmail(event.target.value)}
        value={email}
        width="w-full"
        placeholder="Enter your email..."
        label="Email"
      />
      
      <Input
        onChange={(event) => setPassword(event.target.value)}
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