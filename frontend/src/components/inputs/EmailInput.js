import { useState } from "react";
import Input from "./Input.js";
export function EmailInput({value, setValue}) {
    const [error, setError] = useState("");
    const onSetEmail = (event) => {
        setValue(event.target.value);
    }
    const onBlur = () => {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailRegex.test(value)) {
            setError("Invalid email address");
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
            onChange={onSetEmail}
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