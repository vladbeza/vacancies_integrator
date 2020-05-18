const cityNames  = require('./cityNames');
const languages = require('./languages');


const jobDou = {
    title: "TestDouTitle",
    salary: "$5000",
    dou_id: "555",
    details_link: "http://custom.link",
    description: "It is Test job for DOU",
    company: "MyCompany",
    active: true,
    remote: true,
    is_automation: true,
    cities: [cityNames.kharkiv, cityNames.kiev],
    languages: [languages.python, languages.js]
}

module.exports = jobDou;