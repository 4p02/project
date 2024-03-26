import { useState } from "react";
import Input from "./Input.js";

export default function PasswordInput({value, setGlobalError, setValue, label, placeholder}) {
    const [error, setError] = useState("");
    const onSetPassword = (event) => {
        setValue(event.target.value);
    }

    const onBlur = () => {
        // 8 to 16 characters which contain at least one lowercase letter, one uppercase letter, one numeric digit, and one special character
        var regularExpression = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,16}$/;
        if (!regularExpression.test(value)) {
            setError("Invalid password");
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
          onChange={onSetPassword}
          value={value}
          width="w-full"
          type="password"
          placeholder={placeholder || "Enter your password"}
          label={label || "Password"}
          errorMsg="Invalid password"
          error={error !== ""}
          onBlur={onBlur}
          onFocus={onFocus}
      />
    )
}