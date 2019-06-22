function selectAll() {
        var items = document.getElementsByName('skills_list');
        for (var i = 0; i < items.length; i++) {
            if (items[i].type == 'checkbox')
                items[i].checked = true;
     }
};


function showJobs(jobsListId) {
    var jobsDivs = document.getElementsByClassName("jobs-list-inside");
    Array.from(jobsDivs).forEach((jobDiv) => {
        jobDiv.style.display = "none";
    });

    var jobToShow = document.getElementById(jobsListId);
    jobToShow.style.display = "block";
}


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