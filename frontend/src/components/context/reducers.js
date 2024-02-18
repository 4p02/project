export default function Reducer(state, action) {
  switch (action.type) {
    case "SET_USER": {
      return {
        ...state,
        user: action.payload.user,
      };
    } 
  }
}