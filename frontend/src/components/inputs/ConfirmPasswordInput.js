


import { useState } from "react";
import Input from "./Input.js";

export function ConfirmPasswordInput({value, setValue, setGlobalError, password}) {
    const [error, setError] = useState("");
    const onSetPassword = (event) => {
        setValue(event.target.value);
    }
    const onBlur = () => {
        if (value !== password) {
            setError("Passwords do not match");
            setGlobalError(true);
        } else {
            setError("");
            setGlobalError(false);
        }
    }
    const onFocus = () => {
        setError("");
        setGlobalError(false);
    }
    return (
        <>
            <Input 
                onChange={onSetPassword}
                value={value}
                width="w-full"
                type={"password"}
                placeholder="Enter your password again."
                label="Confirm Password"
                errorMsg="Passwords do not match"
                error={error !== ""}
                onBlur={onBlur}
                onFocus={onFocus}
            />
        </>
    )
}