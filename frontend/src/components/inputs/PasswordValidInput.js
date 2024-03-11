
import { useState } from "react";
import Input from "./Input.js";

export function PasswordInput({value, setValue}) {
    const [error, setError] = useState("");
    const onSetPassword = (event) => {
        setValue(event.target.value);
    }
    const onBlur = () => {
        // 8 to 16 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character
        var regularExpression = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$/;
        if (!regularExpression.test(value)) {
            setError("Invalid password");
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