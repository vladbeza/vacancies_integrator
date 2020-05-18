const mainPage = require('../pages/mainPage.js')
const APIWrapper = require('../utils/apiRequests.js')
const db = require('../utils/dbConnector.js')
const jobDou = require('../common/jobsData.js')
const cities = require('../common/cityNames.js')
const languages = require('../common/languages.js')

describe('Different job types with different options', () => {

    beforeEach(function() {
        return browser.call(async function() {
            return await db.clear_jobs();
            })
      });

    it('Job appears in list', () => {
        browser.call(async function() {
            const wrapper = new APIWrapper(browser.options.baseUrl)
            return await wrapper.addJob(jobDou);
            })
        mainPage.open();
        const jobs = mainPage.job_links;
        let titles = [];
        for (job of jobs){
            titles.push(job.getText());
        }
        expect(titles.includes(`${jobDou.title} ${jobDou.salary}`)).to.be.true;
    });

    it('Check Python Kharkov automation jobs list for DOU', () => {
        browser.call(async function() {
            const wrapper = new APIWrapper(browser.options.baseUrl)
            return await wrapper.addJob(jobDou);
            })
        mainPage.open();
        mainPage.selectCity(cities.kharkiv);
        mainPage.selectLanguage(languages.python);
        mainPage.useDjinniCheckbox.setCheckbox(false);
        mainPage.submit_button.click();
        expect(mainPage.job_links.length > 0).to.be.true;
    })

})