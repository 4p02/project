import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Input from "../Input.js";
import FormButton from "./FormButton.js";

const RegisterView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  const onRegisterClick = () => {

  }

  const onGuestClick = () => {
    navigate("/")
  }

  return (
    <div className="panel flex flex-col items-center my-auto px-12 w-1/2 *:mb-4 py-6">
      <div className="w-full flex justify-between space-x-5">
        <Input
          onChange={(event) => setName(event.target.value)}
          value={name}
          width="w-1/2"
          placeholder="John"
          label="Name"
        />
        <Input
          onChange={(event) => setSurname(event.target.value)}
          value={surname}
          width="w-1/2"
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
        text="Register"
        onClick={onRegisterClick}
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
          text="Log in Instead"
          onClick={viewToggle}
          isSecondary
          width="w-1/2"
        />
      </div>
    </div>
  )
}
export default RegisterView