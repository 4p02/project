import Input from "../Input.js"
import { useState } from "react"
import { useNavigate } from "react-router-dom";
import FormButton from "./FormButton.js";

const LoginView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const onLogInClick = () => {

  }

  const onGuestClick = () => {
    navigate("/")
  }

  return (
    <div className="panel flex my-auto flex-col items-center px-12 w-1/2 *:mb-4 py-6">
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
        text="Log In"
        onClick={onLogInClick}
        width="w-full"
      />

      <div className="w-full flex justify-between space-x-5">
        <FormButton
          text="Continue as Guest"
          onClick={onGuestClick}
          isSecondary
          width="w-1/2"
        />
        <FormButton
          text="Register Instead"
          onClick={viewToggle}
          isSecondary
          width="w-1/2"
        />
      </div>
    </div>
  )
}
export default LoginView