class Page {

    constructor(){ }
    
    open(path) {
        allure.addStep(`Open page ${path}`)
        browser.url(`/${path}`)
    }

}

module.exports = Page;
