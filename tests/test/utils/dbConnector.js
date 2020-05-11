const pg = require('pg');

class DBConnector {

    constructor(){
        this.client = new pg.Client({
            host: 'localhost',
            port: 5433,
            user: 'integrator_test',
            password: 'Qaz123wsx',
            database: 'integrator_test_db'
          })
     }
    
    clear_jobs(){
        return this.make_request("DELETE * FROM jobs;");
    }

    list_cities(){
        return this.make_request("SELECT * FROM cities;");
    }

    add_job(title, salary, dou_id, djinni_id,
            details_link, description, company,
            created=nil, active=true,
            remove=false, is_automation=true){
        return this.make_request(`INSERT INTO jobs
             (title, dou_id, description, details_link,
              company, salary, active, remote, created,
             djinni_id, is_automation) 
             VALUES ();`)

    }

    make_request(requestString){
        this.client.connect()
        return this.client
            .query(requestString)
            .then((res) => console.log(res))
            .catch((error) => console.log(error))
            .then(() => this.client.end())
    }
}

const connector = new DBConnector()
connector.list_cities()
    

module.exports = new DBConnector();