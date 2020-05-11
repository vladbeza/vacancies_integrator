const mainPage = require('../pages/mainPage.js')
const dbClient = require('../utils/dbConnector.js')

describe('Different job types with different options', () => {

    beforeEach(() => {
        browser.call(() => {
            return dbClient.list_cities()
            })
    });

    it('Empty jobs list', () => {
        mainPage.open();
        expect(mainPage.job_links.length === 0).to.be.true;
    });

})