import { BACKEND_API_URL } from "../lib/Constants";

export default class Summarize {
    constructor(token) {
        this.token = token;
    }
    getToken() {
        return this.token;
    }
<<<<<<< HEAD:frontend/src/api/Summarize.js
    async summarizeArticle(link) {
=======
    async summerizeArticle(url) {
>>>>>>> 1e8fd275ad81edcdeb302c898e5b458850f10700:frontend/src/api/Summerize.js
        const response = await fetch(`${BACKEND_API_URL}/summarize/article`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: url
            })
        });
        return await response.json()
        
    }
    async summarizeVideo(link) {
        const response = await fetch(`${BACKEND_API_URL}/summarize/video`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                url: link
            })
        });
        return response;
    }
}