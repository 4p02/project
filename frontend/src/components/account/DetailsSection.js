import AccountSection from "./AccountSection"
import FormButton from "../auth/FormButton"
import toast from "react-hot-toast"

const DetailsSection = () => {

  const onGoPro = () => {
    toast("Redirect here or something?")
  }

  return (
    <AccountSection title="Account Details">
      <div className="w-full flex items-center text-left px-12">
        <div className="w-full flex flex-col mb-2">
          <p className="text-[1.25rem]"><b>Name:</b> John Doe</p>
          <p className="text-[1.25rem]"><b>Date joined:</b> March 2nd, 2023</p>
          <p className="text-[1.25rem]"><b>Links:</b> 23</p>
          <p className="text-[1.25rem]"><b>Status:</b> Basic/Pro</p>
        </div>
        <FormButton
          onClick={onGoPro}
          width="w-1/2"
          extraClassName="!bg-[#FFD250] !text-dark"
          isSecondary
        >
          Go Pro
        </FormButton>
      </div>
    </AccountSection>
  )
}
export default DetailsSection