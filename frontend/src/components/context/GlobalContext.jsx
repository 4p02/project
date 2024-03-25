import React, { createContext, useReducer } from "react";
import Reducer from "./reducers";


const DEFAULT_STATE = {
  state: null,
  dispatch: () => {}
}

export const GlobalContext = createContext(DEFAULT_STATE);

/*
  * GlobalContextProvider is a wrapper component that provides the state and dispatch
  * to all the components that are wrapped inside it. thus passing values such as token, fullName, email to all the components because we need them
  * Reducer allows the changes to the state to be made in a single place
*/
export default function GlobalContextProvider({ children }) {
  const [state, dispatch] = useReducer(Reducer, {
    user: null,
    darkMode: false
  });

  return (
    <GlobalContext.Provider value={{ state, dispatch }}>
      {children}
    </GlobalContext.Provider>
  );
}