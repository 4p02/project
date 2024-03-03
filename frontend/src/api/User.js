import { BACKEND_API_URL } from '../lib/Constants.js';

export default class User {
    // maybe store links
    email;
    fullName;
    links;
    constructor(token) {
        this.token = token;
        this.links = [];
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
    getLinks() {
        return this.links;
    }

    getEmail() {
        // use the token to get the email
    }

    checkValidToken() {

    }
    
    /* 
        fetch data on behalf of the user (token required)
        @param {string} directory - the directory to send the query to (first / is already included) (e.g. /users)
        @return {Promise} - the response from the postgrest api
    */
    
    async formatAuthenticatedPostgrestQuery(directory) {

        if (this.token === null) {
            throw new Error("Token is null");
        }
        const response = await fetch(`${BACKEND_API_URL}/${directory}`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${this.token}`
            },
        });
        return response;
    }

    /*
        fetch data on behalf of the anonymous user (no token required)
        @param {string} directory - the directory to send the query to (first / is already included) (e.g. /users)
        @return {Promise} - the response from the postgrest api
    */
    async formatNonAuthenticatedPostgrestQuery(directory) {
        const response = await fetch(`${BACKEND_API_URL}/${directory}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },

        });
        return response;
    }
}