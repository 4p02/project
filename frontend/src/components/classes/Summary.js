class Summarize extends Link {
    
    constructor(id, shortenedUrl, originalUrl, summary) {
        super(id, shortenedUrl, originalUrl);
        this.summary = summary;
    }
    getSummary() {
        return this.summary;
    }
}