import User from "../api/User";

export const POSTGREST_API_URL = "http://localhost:5000";
export const BACKEND_API_URL = "http://localhost:8080";

export const PAGE_SIZE = 10;

/*
Check for valid token or state
*/
export const CheckTokenAndState = (token, state, dispatch) => {
    console.debug("CheckTokenAndState", token, state);
    if (state && state.user) {
        return true;
    } else if (token) {
        const user = new User(token);
        dispatch({type: "SET_USER", payload: user});
        return true;
    }
    return false;
}