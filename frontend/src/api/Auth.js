import { BACKEND_API_URL } from "../lib/Constants";

export async function RegisterUserGoogle() {
    // TODO theres a way to get the code from the url and send it to the backend to get the token
    window.location.href = `${BACKEND_API_URL}/auth/google`;
}

export async function RegisterUser(email, password, fullName) {
    const response = await fetch(`${BACKEND_API_URL}/auth/register`, {
        method: 'POST',
        headers: {  
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password,
            fullname: fullName
        })
    }).then(response => response.json());
    // maybe check for response.ok here
    if (response.detail) {
        return "error";
    }
    return response;
}

export async function LoginUser(email, password) {
    // check if token exists here maybe?

    const response = await fetch(`${BACKEND_API_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            email: email,
            password: password
        })
    })
    .then(response => response.json());
    // maybe check for response.ok here
    return response;
}

export async function ChangePassword(password, newPassword) {
  try {

  } catch(error) {
    return "error";
  }
}

export async function ChangeEmail(email, password) {

}

export async function DeleteAccount(password) {
  try {

  } catch(error) {
    return "error";
  }
}