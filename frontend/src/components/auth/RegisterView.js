import { useNavigate } from "react-router-dom";
import { useState, useContext } from "react";
import Input from "../inputs/Input.js";
import FormButton from "./FormButton.js";
import GoogleButton from "./GoogleButton.js";
import { GlobalContext } from "../context/GlobalContext.jsx";
import { BACKEND_API_URL } from "../../lib/Constants.js";
import { RegisterUser } from "../../api/Auth.js";
import EmailInput from "../inputs/EmailInput.js";
import PasswordInput from "../inputs/PasswordValidInput.js";
import ConfirmPasswordInput from "../inputs/ConfirmPasswordInput.js";
import toast from "react-hot-toast";
import User from "../../api/User.js";

const RegisterView = ({ viewToggle }) => {
  const navigate = useNavigate();
  const {state, dispatch} = useContext(GlobalContext);
  const [name, setName] = useState("");
  const [surname, setSurname] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState(false);
  
  const onRegisterClick = async () => {
    const response = await RegisterUser(email, password, `${name} ${surname}`);
    if (response == "error") {
      toast.error("Email is already in use");
      return;
    }

    toast.success("Account created successfully!");
    const token = response.token;
    localStorage.setItem("token", token);
    toast.success("Registered successfully!");
    const user = new User(token);
    dispatch({type: "SET_USER", payload: { user } });
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
        setGlobalError={setError}
      />
      <PasswordInput
        value={password}
        setGlobalError={setError}
        setValue={setPassword}
      /> 
      <ConfirmPasswordInput
        value={confirmPassword}
        setValue={setConfirmPassword}
        setGlobalError={setError}
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