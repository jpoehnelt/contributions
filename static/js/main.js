var ANON = true;

function getContribRepr(contributor) {
    if (ANON) {
        return contributor.id;
    }
    return contributor.name;
}

function getCommits(project_id, contributor_id) {
    "use strict";
    var url = "/api/commit?";

    if (project_id) {
        url += "project_id=" + String(project_id) + "&";
    }

    if (contributor_id) {
        url += "contributor_id=" + String(contributor_id);
    }

    return $.ajax({
        method: "GET",
        url: url
        });
}

(function () {
    "use strict";
    var cf = {};
    window.cf = cf;
    cf.data = crossfilter();

    // crossfilter dimensions allow indexing of these returned values for quick processing
    cf.dimensions = {
        username: cf.data.dimension(function (commit) {
            return getContribRepr(commit.contributor);
        }),
        projectNumber: cf.data.dimension(function (commit) {
            return commit.project.projectNumber;
        })
    };

    // groups based upon dimensions
    cf.groups = {
        username: cf.dimensions.username.group(function (username) {
            return username;
        }),
        projectNumber: cf.dimensions.projectNumber.group(function (projectNumber) {
            return projectNumber;
        })
    };


}());

