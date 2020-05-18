const fetch = require("node-fetch");

class APIWrapper{

    constructor(baseUrl){
        this.baseUrl = baseUrl
    }

    async addJob(data){
        const url = `${this.baseUrl}/api/v1.0/create`
        console.log(`Fetch ${url}`)
        const response = await fetch(url, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json'
            }
            });
            const result = await response.json();
            console.log('Result:', JSON.stringify(result));
    }
}

module.exports = APIWrapper;