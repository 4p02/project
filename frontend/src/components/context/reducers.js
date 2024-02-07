export default function Reducer(state, action) {
  switch (action.type) {
    case "LOGIN":
      return {
        ...state,
        full_name: action.payload.full_name,
        email: action.payload.email,
        token: action.payload.token,
      };
    case "LOGOUT":
      return {
        ...state,
        full_name: null,
        email: null,
        token: null,
      };
    case "SET_USER":
      return {
        ...state,
        full_name: action.payload.full_name,
        email: action.payload.email,
        token: action.payload.token,
      };
  }
}