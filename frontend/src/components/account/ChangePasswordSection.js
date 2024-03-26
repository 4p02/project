import PasswordInput from "../inputs/PasswordValidInput.js";
import AccountSection from "./AccountSection"
import { useState } from "react";
import { ChangePassword } from "../../api/Auth.js";
import toast from "react-hot-toast"
import FormButton from "../auth/FormButton.js";

const ChangePasswordSection = () => {
  const [error, setError] = useState(false);
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const onChangePasswordClick = async () => {
    const response = await ChangePassword(oldPassword, newPassword);
    if (response == "error") {
      toast.error("New password is invalid");
      return;
    }

    toast.success("Password successfully changed!");
  }

  return (
    <AccountSection title="Change Password">
      <div className="w-full flex flex-col items-center">
        <div className="w-full space-x-4 flex my-2 text-left">
          <PasswordInput
            placeholder={"Enter current password..."}
            value={oldPassword}
            setGlobalError={setError}
            setValue={setOldPassword}
          />
          <PasswordInput
            label={"New Password"}
            placeholder={"Enter new password..."}
            value={newPassword}
            setGlobalError={setError}
            setValue={setNewPassword}
          /> 
        </div>
        <FormButton
          onClick={onChangePasswordClick}
          width="w-1/2"
          disabled={error}
          isSecondary
        >
          Change Password
        </FormButton>
      </div>
    </AccountSection>
  )
}
export default ChangePasswordSection