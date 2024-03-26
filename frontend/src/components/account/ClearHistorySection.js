import AccountSection from "./AccountSection"
import FormButton from "../auth/FormButton"
import toast from "react-hot-toast"

const ClearHistorySection = () => {
  const onClearHistory = () => {
    toast.success("Cleared history!")
  }

  return (
    <AccountSection title="Clear History">
      <div className="w-full flex flex-col items-center text-left">
        <p className="text-[2rem] text-center mb-4 rounded-xl bg-dark-light px-6 py-2 mt-5">This cannot be undone, are you sure you want to clear your history?</p>
        <FormButton
          onClick={onClearHistory}
          width="w-1/2"
          isSecondary
        >
          Clear
        </FormButton>
      </div>
    </AccountSection>
  )
}
export default ClearHistorySection