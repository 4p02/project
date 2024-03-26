import { useState } from "react"
import FormButton from "../auth/FormButton"
import PasswordInput from "../inputs/PasswordValidInput"
import AccountSection from "./AccountSection"

const DeleteAccountSection = () => {
  const [password, setPassword] = useState("");
  const [error, setError] = useState(false);

  const onDeleteAccount = () => {
    
  }

  return (
    <AccountSection title="Delete Account">
      <div className="w-full flex flex-col items-center text-left">
        <div className="w-2/3 space-x-4 flex mb-2">
          <PasswordInput
            value={password}
            setGlobalError={setError}
            setValue={setPassword}
          />

        </div>
        <FormButton
          onClick={onDeleteAccount}
          width="w-1/2"
          disabled={error}
        >
          Delete
        </FormButton>
      </div>
    </AccountSection>
  )
}
export default DeleteAccountSection