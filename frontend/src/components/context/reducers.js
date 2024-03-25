export default function Reducer(state, action) {
  switch (action.type) {
    case "SET_USER": {
      return {
        ...state,
        user: action.payload.user,
      };
    }
    case "SET_DARK_MODE": {
      localStorage.setItem("darkMode", action.payload.darkMode)
      return {
        ...state,
        darkMode: action.payload.darkMode
      }
    }
  }
}