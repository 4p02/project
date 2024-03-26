import { useState } from "react";
import Input from "./Input.js";

export default function EmailInput({value, setValue, setGlobalError, label, placeholder}) {
    const [error, setError] = useState("");
    const onSetEmail = (event) => {
        setValue(event.target.value);
    }
    const onBlur = () => {
        const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        if (!emailRegex.test(value)) {
            setError("Invalid email address");
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
      <Input 
          onChange={onSetEmail}
          value={value}
          width="w-full"
          type={"email"}
          placeholder={placeholder || "Enter your email..."}
          label={label || "Email"}
          errorMsg="Invalid email address"
          error={error !== ""}
          onBlur={onBlur}
          onFocus={onFocus}
      />
    )
}