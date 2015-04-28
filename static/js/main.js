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
    cf.dimensions = {
        username: cf.data.dimension(function (commit) {
            return getContribRepr(commit.contributor);
        }),
        project_number: cf.data.dimension(function (commit) {
            return commit.project.project_number;
        })
    };

    cf.groups = {
        username: cf.dimensions.username.group(function (username) {
            return username;
        }),
        project_number: cf.dimensions.project_number.group()
    };


}());

