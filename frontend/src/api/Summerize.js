import { BACKEND_API_URL } from "../lib/Constants";

export default class Summerize {
    constructor(token) {
        this.token = token;
    }
    getToken() {
        return this.token;
    }
    async summerizeArticle(url) {
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
    async summerizeVideo(link) {
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