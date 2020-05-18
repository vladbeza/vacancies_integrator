const pg = require('pg');

const dbParameters = {
    host: 'localhost',
    port: 5433,
    user: 'integrator_test',
    password: 'Qaz123wsx',
    database: 'integrator_test_db'
  }


class DBConnector {
    
    async clear_jobs(){
        await this.make_request("DELETE FROM locations;");
        await this.make_request("DELETE FROM programm_langs_in_job;");
        await this.make_request("DELETE FROM jobs;");
    }

    async make_request(requestString){
        const client = new pg.Client(dbParameters)
        await client.connect()
        try{
            const res = await client.query(requestString)
            return res
        }
        catch (error){
            console.log("Couldn't make request.")
            console.log(error)
        }
        finally{
            await client.end()
        }
    }
}

module.exports = new DBConnector();