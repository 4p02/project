import { useNavigate } from "react-router-dom"
import GetStartedCard from "../components/GetStartedCard"

const GetStarted = () => {
  const navigate = useNavigate();

  const goToSignIn = () => navigate("/auth", { state: { isSignIn: true } })
  const goToLogIn = () => navigate("/auth");
  const continueAsGuest = () => navigate("/");

  return (
    <div className="flex flex-col items-center min-h-screen px-4 md:px-8 lg:px-16 xl:px-20">
      {/* Header Group */}
      <div className="flex flex-col w-full text-center mt-8 mb-12 md:mb-16">
        <h1 className="text-3xl md:text-4xl lg:text-5xl font-bold">Create an Account or Log In</h1>
        <label className="mt-2 text-base md:text-lg">Access additional features and save your shortened links and summaries.</label>
      </div>

      {/* Cards Group */}
      <div className="flex flex-col md:flex-row justify-center w-full md:space-x-8">
        <GetStartedCard
          title="Create an Account"
          desc="Sign up for an account to unlock all the features of Shortify.\nSave your shortened links and summaries for easy access."
          onClick={goToSignIn}
          extraClasses="md:w-1/3"
        />
        <GetStartedCard
          title="Log In"
          desc="Already have an account?\nLog in to access your saved shortened links and summaries."
          onClick={goToLogIn}
          extraClasses="md:w-1/3"
        />
        <GetStartedCard
          title="Continue as Guest"
          desc="Want to be anonynymous? Continue with our guest mode.\nNote: Links & summaries won't be saved!"
          onClick={continueAsGuest}
          extraClasses="md:w-1/3"
        />
      </div>
    </div>
  )
}
export default GetStarted
