import FormButton from "./FormButton";
import GoogleIcon from "../../assets/googleIcon.svg";

const GoogleButton = ({ onClick, text }) => {
  return (
    <FormButton
      onClick={onClick}
      width="w-full"
      isSecondary
      extraClassName="flex items-center justify-center"
    >
      <img src={GoogleIcon} className="mr-4" /> {text}
    </FormButton>
  )
}
export default GoogleButton