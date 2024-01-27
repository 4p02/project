import React, { createContext, useReducer, useEffect } from "react";
import Reducer from "./reducers";

export const GlobalContext = createContext({});

/*
    * GlobalContextProvider is a wrapper component that provides the state and dispatch
    * to all the components that are wrapped inside it. thus passing values such as token, full_name, email to all the components because we need them
    * Reducer allows the changes to the state to be made in a single place
*/
export default function GlobalContextProvider({ children }) {
  const [state, dispatch] = useReducer(Reducer, {
    token: null,
    full_name: null,
    email: null,
  });
    useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
        // check if token is valid

    }
    // else do nothing because if it not there then user is not logged in and everything is null
  }, []);
  return (
    <GlobalContext.Provider value={{ state, dispatch }}>
      {children}
    </GlobalContext.Provider>
  );
}