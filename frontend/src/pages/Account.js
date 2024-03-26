import ChangeEmailSection from "../components/account/ChangeEmailSection"
import ChangePasswordSection from "../components/account/ChangePasswordSection"
import ClearHistorySection from "../components/account/ClearHistorySection"
import DeleteAccountSection from "../components/account/DeleteAccountSection"
import DetailsSection from "../components/account/DetailsSection"

const Account = () => {
  return (
    <div className="page">
      <h1 className="title">Account Settings</h1>
      <div className="panel w-2/3 [&>*:first-child]:border-t-0 py-2">
        <DetailsSection />
        <ChangeEmailSection />
        <ChangePasswordSection />
        <ClearHistorySection />
        <DeleteAccountSection />
      </div>
    </div>
  )
}
export default Account