import React, { createContext, useReducer, useEffect } from "react";
import Reducer from "./reducers";
import User from "../../api/User";


export const GlobalContext = createContext({});

/*
    * GlobalContextProvider is a wrapper component that provides the state and dispatch
    * to all the components that are wrapped inside it. thus passing values such as token, fullName, email to all the components because we need them
    * Reducer allows the changes to the state to be made in a single place
*/
export default function GlobalContextProvider({ children }) {
  const [state, dispatch] = useReducer(Reducer, {
    user: null,
  });

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token && !state.user) {
        // check if token is valid (maybe in the constructor)
        const userObj = new User(token); 
        dispatch({
          type: "SET_USER",
          payload: {
            user: userObj,
          },
        })
    }
    // else do nothing because if it not there then user is not logged in and everything is null
  }, []);

  return (
    <GlobalContext.Provider value={{ state, dispatch }}>
      {children}
    </GlobalContext.Provider>
  );
}