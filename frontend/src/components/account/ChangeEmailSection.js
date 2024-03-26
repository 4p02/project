import toast from "react-hot-toast"
import FormButton from "../auth/FormButton"
import AccountSection from "./AccountSection"
import PasswordInput from "../inputs/PasswordValidInput"
import EmailInput from "../inputs/EmailInput"
import { useState } from "react"

const ChangeEmailSection = () => {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState(false)

  const onChangeEmail = () => {
    toast("What here?")
  }

  return (
    <AccountSection title="Change Email">
      <div className="w-full flex flex-col items-center text-left px-12">
        <div className="w-full flex flex-col mb-2">
          <EmailInput
            value={email}
            setGlobalError={setError}
            setValue={setEmail}
            label="New email"
            placeholder="Enter your new email..."
          />
          <PasswordInput
            value={password}
            setGlobalError={setError}
            setValue={setPassword}
          />
        </div>
        <FormButton
          onClick={onChangeEmail}
          width="w-1/2"
          isSecondary
        >
          Change Email
        </FormButton>
      </div>
    </AccountSection>
  )
}
export default ChangeEmailSection