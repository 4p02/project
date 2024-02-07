import { useNavigate } from "react-router-dom"
import GetStartedCard from "../components/GetStartedCard"

const GetStarted = () => {
  const navigate = useNavigate();

  const goToSignIn = () => navigate("/auth", { state: { isSignIn: true } })
  const goToLogIn = () => navigate("/auth");
  const continueAsGuest = () => navigate("/");

  return (
    <div className="flex flex-col items-center min-h-screen h-fit w-screen p-16">
      {/* Header Group */}
      <div className="flex flex-col w-full">
        <h1 className="title phablet-max:text-center">Create an Account or Log In</h1>
        <label className="subtitle phablet-max:text-[1.25rem] phablet-max:text-center">Access additional features and save your shortened links and summaries.</label>
      </div>

      {/* Cards Group */}
      <div className="flex lg:flex-row flex-col justify-center items-center w-full  phablet-max:my-2 my-24">
        <GetStartedCard
          title="Create an Account"
          desc="Sign up for an account to unlock all the features of Shortify.\nSave your shortened links and summaries for easy access."
          onClick={goToSignIn}
        />
        <GetStartedCard
          title="Log In"
          desc="Already have an account?\nLog in to access your saved shortened links and summaries."
          onClick={goToLogIn}
        />
        <GetStartedCard
          title="Continue as Guest"
          desc="Want to be anonynymous? Continue with our guest mode.\nNote: Links & summaries won't be saved!"
          onClick={continueAsGuest}
        />
      </div>
    </div>
  )
}
export default GetStarted