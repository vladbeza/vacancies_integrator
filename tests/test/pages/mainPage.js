const BasePage = require("./basePage");

class MainPage extends BasePage{

    constructor() {
        super()
    }

    open() {
        super.open("")
    }

    get cityDropdown() {
        return $('select#city')
    }

    get languageDropdown() {
        return $('select#language')
    }

    get automationCheckbox() {
        return $('input#automation_only')
    }

    get automationCheckbox() {
        return $('input#automation_only')
    }

    get remoteCheckbox() {
        return $('input#remote_only')
    }

    get knownSalaryCheckbox() {
        return $('input#known_salary')
    }

    get useDouCheckbox() {
        return $('input#use_dou_stats')
    }

    get useDjinniCheckbox() {
        return $('input#use_djinni')
    }

    get salary_input(){
        return $('#salary_more')
    }

    get submit_button(){
        return $('input#submit')
    }

    get job_links(){
        return $$('a#job-link')
    }

    selectCity(cityName) {
        allure.addStep(`Select city ${cityName}`)
        this.cityDropdown.selectByVisibleText(cityName)
    }

    selectLanguage(lang) {
        allure.addStep(`Select language ${lang}`)
        this.languageDropdown.selectByVisibleText(lang)
    }

    define_salary(salary) {
        allure.addStep(`Set salary ${salary}`)
        this.salary_input.setValue(salary)
    }

}

module.exports = new MainPage();