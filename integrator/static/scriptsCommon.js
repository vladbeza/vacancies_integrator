function selectAll() {
        var items = document.getElementsByName('skills_list');
        for (var i = 0; i < items.length; i++) {
            if (items[i].type == 'checkbox')
                items[i].checked = true;
     }
};


function showJobs(skill, jobsList) {
    console.log(skill);
    console.log(jobsList);
    var jobsP = document.getElementById("jobs_skill_title");
    var jobsUl = document.getElementById("jobs-list");
    var jobsDiv = document.getElementById("jobs_for_skill");
    while(jobsUl.firstChild) jobsUl.removeChild(jobsUl.firstChild);
    jobsP.textContent = "Jobs for " + skill;
    for (var job in jobsList) {
            var li = document.createElement("li");
            var a = document.createElement("a");

            li.setAttribute("id", "job-item");
            a.setAttribute("id", "job-link");
            a.setAttribute("href", jobsList[job].details_link);
            a.textContent = jobsList[job].title;

            li.appendChild(a);
            jobsUl.appendChild(li);
        };

    jobsDiv.style.display = "block";
    jobsDiv.scrollIntoView();
};


document.addEventListener('DOMContentLoaded', function(){
    console.log("add button");
    var form_div = document.querySelector("#skills_list").closest(".form-group ");
    var button = document.createElement("button");
    button.type = "button";
    button.innerHTML = 'Select all';
    button.onclick = function() {
                selectAll();
            };
    form_div.appendChild(button);
});