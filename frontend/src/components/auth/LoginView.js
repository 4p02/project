import Input from "../Input.js"
import { useState } from "react"
import { useNavigate } from "react-router-dom";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";

const LoginView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onLogInClick = () => {

  }

  const onGoogleLogin = () => {

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