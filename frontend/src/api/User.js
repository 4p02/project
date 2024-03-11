import { POSTGREST_API_URL, BACKEND_API_URL } from '../lib/Constants.js';
import { PostgrestClient} from "@supabase/postgrest-js";

export default class User {
    email;
    fullName;
    postgrestClient;
    constructor(token) {
        this.token = token;
        const checkIfTokenIsValid = (token) => {
            if (token === null) {
                return false;
            }
            // maybe add a route to the backend
            return true;
        }

        this.postgrestClient = new PostgrestClient(POSTGREST_API_URL, checkIfTokenIsValid(token) ? 
        {headers: {
            Authorization: `Bearer ${token}`
        }, schema: "public"} : {schema: "public"});
    }
    getEmail() {
        return this.email;
    }
    getFullName() {
        return this.fullName;
    }
    getToken() {
        return this.token;
    }

    getPostGrestClient() {
        return this.postgrestClient;
    }

    /*
        Get more links from the user
        @param {int} limit - the number of links to get default 10
        @param {int} offset - the number of links to skip
        @return {Array} - an array of links
    */
    getLinks(limit, offset) {
        return this.postgrestClient.from('links').select().range(offset, limit).then(response => {
            return response.body;
        }).catch(error => {
            console.log(error);
            return "error";
        });
    }

    
    
    
    
    deleteAccount() {

    }
}