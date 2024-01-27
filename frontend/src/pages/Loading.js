
import Lottie from "lottie-react";

export default function LoadingScreen() {
    return (
        <div className="justify-center items-center bg-white ">
            <Lottie height={300} width={300} loop={true}  animationData={require("../assets/animation/cat.json")} />
        </div>
        
    )
}