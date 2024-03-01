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
        @param {string} query - the query to be sent to the postgrest api
        @param {string} directory - the directory to send the query to (first / is already included)
        @return {Promise} - the response from the postgrest api
    */
    
    async formatAuthenticatedPostgrestQuery(query, directory) {
        if (this.token === null) {
            throw new Error("Token is null");
        }
        const response = await fetch(`${BACKEND_API_URL}/${directory}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.token}`
            },
            body: JSON.stringify(query)
        });
        return response;
    }

    /*
        fetch data on behalf of the anonymous user (no token required)
        @param {string} query - the query to be sent to the postgrest api
        @param {string} directory - the directory to send the query to (first / is already included)
        @return {Promise} - the response from the postgrest api
    */
    async formatNonAuthenticatedPostgrestQuery(query, directory) {
        const response = await fetch(`${BACKEND_API_URL}/${directory}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(query)
        });
        return response;
    }
}