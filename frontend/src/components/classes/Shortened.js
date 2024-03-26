

/*
    Contains the shortened link with the id to the summary for a revist
    @param id: the id of the shortened link
    @param shortenedUrl: the shortened url
    @param originalUrl: the original url
    @param summaryId: the id of the summary

*/
class ShortenedLink extends Link {
    
    constructor(id, shortenedUrl, originalUrl, summaryId) {
        super(id, shortenedUrl, originalUrl);
        this.summaryId = summaryId;
    }
    getSummaryId() {
        return this.summaryId;
    }

}