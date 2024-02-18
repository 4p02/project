


/* 
    abstract class for link (shortened link and summerize)
    @param id: the id of the object
    @param shortenedUrl: the shortened url
    @param originalUrl: the original url

*/
class Link {
        
    constructor(id, shortenedUrl, originalUrl) {
        this.id = id;
        this.originalUrl = originalUrl;
        this.shortenedUrl = shortenedUrl;
    }

    getId() {
        return this.id;
    }

    getOriginalUrl() {
        return this.originalUrl;
    }

    getShortenedUrl() {
        return this.shortenedUrl;
    }
    
}