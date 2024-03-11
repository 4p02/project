import { useNavigate } from "react-router-dom";
import { useEffect, useState, useContext, useRef } from "react";
import Input from "../inputs/Input.js";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";
import { GlobalContext } from "../context/GlobalContext.jsx";
import { BACKEND_API_URL } from "../../lib/Constants.js";
import { RegisterUser } from "../../api/Auth.js";
import { EmailInput } from "../inputs/EmailInput.js";
import { PasswordInput } from "../inputs/PasswordValidInput.js";
import { ConfirmPasswordInput } from "../inputs/ConfirmPasswordInput.js";

const RegisterView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isPasswordGood, setIsPasswordGood] = useState(false);
  const [error, setError] = useState(false);
  
  useEffect(() => {
    // check if token exists here so we can avoid this view
  }, [])
  const onRegisterClick = () => {
    const response = RegisterUser(email, password, `${name} ${surname}`)
    // handle response
  }

  const onGoogleRegisterClick = () => {
    window.location.href = `${BACKEND_API_URL}/auth/google`;
  }

  const onGuestClick = () => {
    navigate("/")
  }
  const onSetName = (event) => {
    setName(event.target.value);
  }
  const onSetSurname = (event) => {
    setSurname(event.target.value);
  }
 
  return (
    <div className="panel phablet-max:bg-white flex flex-col items-center px-12 w-full *:mb-4 py-6">
      <div className="form-ui-group">
        <Input
          onChange={onSetName}
          value={name}
          width="form-ui-group-element-width"
          placeholder="John"
          label="Name"
        />
        <Input
          onChange={onSetSurname}
          value={surname}
          width="form-ui-group-element-width"
          placeholder="Doe"
          label="Surname"
        />
      </div>
      <EmailInput 
        value={email}
        setValue={setEmail}
      />
      <PasswordInput
        value={password}
        setValue={setPassword}
      /> 
      <ConfirmPasswordInput
        value={confirmPassword}
        setValue={setConfirmPassword}
        password={password}
      />

      {/* Buttons */}
      <FormButton
        onClick={onRegisterClick}
        width="w-full"
        disabled={error}
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