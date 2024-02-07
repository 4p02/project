import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Input from "../Input.js";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";

const RegisterView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const onRegisterClick = () => {

  }

  const onGoogleRegisterClick = () => {

  }

  const onGuestClick = () => {
    navigate("/")
  }

  return (
    <div className="panel phablet-max:bg-white flex flex-col items-center px-12 w-full *:mb-4 py-6">
      <div className="form-ui-group">
        <Input
          onChange={(event) => setName(event.target.value)}
          value={name}
          width="form-ui-group-element-width"
          placeholder="John"
          label="Name"
        />
        <Input
          onChange={(event) => setSurname(event.target.value)}
          value={surname}
          width="form-ui-group-element-width"
          placeholder="Doe"
          label="Surname"
        />
      </div>
      <Input
        onChange={(event) => setEmail(event.target.value)}
        value={email}
        width="w-full"
        placeholder="john-doe@gmail.com"
        label="Email"
      />
      <Input
        onChange={(event) => setPassword(event.target.value)}
        value={password}
        width="w-full"
        placeholder="Enter a password..."
        type="password"
        label="Password"
      />
      <Input
        onChange={(event) => setConfirmPassword(event.target.value)}
        value={confirmPassword}
        width="w-full"
        placeholder="Re-enter your password..."
        type="password"
        label="Confirm Password"
      />

      {/* Buttons */}
      <FormButton
        onClick={onRegisterClick}
        width="w-full"
      >
        Register
      </FormButton>

      <GoogleButton
        onClick={onGoogleRegisterClick}
        text={"Google Sign In"}
      />

      <div className="form-ui-group">
        <FormButton
          onClick={onGuestClick}
          isSecondary
          width="w-full phablet:w-1/2"
        >
          Continue as Guest
        </FormButton>
        <FormButton
          onClick={viewToggle}
          isSecondary
          width="w-full phablet:w-1/2"
        >
          Log in Instead
        </FormButton>
      </div>
    </div>
  )
}
export default RegisterView