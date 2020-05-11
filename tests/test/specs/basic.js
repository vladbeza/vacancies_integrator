const mainPage = require('../pages/mainPage.js')
const languages = require('../common/languages.js')
const cities = require('../common/cityNames.js')

describe('There are widgets and checkboks on main Integrator page', () => {

    it('City and Lang dropdown default value', () => {
        mainPage.open();
        expect(mainPage.cityDropdown.getValue()).to.be.equal("Any")
        expect(mainPage.languageDropdown.getValue()).to.be.equal("Any")
    });

    it('City dropdown list', () => {
        mainPage.open();
        let cityDropdownElements = $$('select#city option')
        let cityNames = []
        for (el of cityDropdownElements){
            cityNames.push(el.getText())
        }
        expect(cityNames).to.be.deep.equal(["Харьков", "Киев", "Одесса", "Львов", "Другой", "Any"])
    });

    it('Check Python Kharkov automation jobs list for DOU', () => {
        mainPage.open();
        mainPage.selectCity(cities.kharkiv);
        mainPage.selectLanguage(languages.python);
        mainPage.useDjinniCheckbox.setCheckbox(false);
        mainPage.submit_button.click();
        expect(mainPage.job_links.length > 0).to.be.true;
    })
});
