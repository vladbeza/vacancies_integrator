const mainPage = require('../pages/mainPage.js')

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
});
