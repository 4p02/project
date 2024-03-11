


import { useState } from "react";
import Input from "./Input.js";

export function ConfirmPasswordInput({value, setValue, password}) {
    const [error, setError] = useState("");
    const onSetPassword = (event) => {
        setValue(event.target.value);
    }
    const onBlur = () => {
        if (value !== password) {
            setError("Passwords do not match");
        } else {
            setError("");
        }
    }
    const onFocus = () => {
        setError("");
    }
    return (
        <>
            <Input 
                onChange={onSetPassword}
                value={value}
                width="w-full"
                type={"email"}
                placeholder="Enter your email..."
                label="Email"
                errorMsg="Invalid email address"
                error={error !== ""}
                onBlur={onBlur}
                onFocus={onFocus}
            />
        </>
    )
}