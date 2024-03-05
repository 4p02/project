import { BACKEND_API_URL } from "../lib/Constants";

export default class Summarize {
    constructor(token) {
        this.token = token;
    }
    getToken() {
        return this.token;
    }
    async summarizeArticle(link) {
        const response = await fetch(`${BACKEND_API_URL}/summarize/article`, {
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