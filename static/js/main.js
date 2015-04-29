Date.prototype.addHours = function (h) {
    this.setHours(this.getHours() + h);
    return this;
};

var ANON = true;
var weekdays = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

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
        sha: cf.data.dimension(function (commit) {
            return commit.id;
        }),
        username: cf.data.dimension(function (commit) {
            return getContribRepr(commit.contributor);
        }),
        projectNumber: cf.data.dimension(function (commit) {
            return commit.project.projectNumber;
        }),
        day: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            d = d.addHours(7);
            d.setHours(0, 0, 0, 0);
            return d;
        }),
        dayOfWeek: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            return d.addHours(7).getDay();
        })
    };

    // groups based upon dimensions
    cf.groups = {
        sha: cf.dimensions.sha.group(),
        username: cf.dimensions.username.group(),
        projectNumber: cf.dimensions.projectNumber.group(),
        day: cf.dimensions.day.group(),
        dayOfWeek: cf.dimensions.dayOfWeek.group()
    };

    cf.charts = {
        dayOfWeek: function (id) {
            var self = dc.rowChart(id);
            self.width($(id).parent().width())
                .height(225)
                .margins({top: 10, left: 10, right: 10, bottom: 20})
                .group(cf.groups.dayOfWeek)
                .dimension(cf.dimensions.dayOfWeek)
                .colors(d3.scale.category10())
                .label(function (d) {
                    return weekdays[d.key];
                })
                .elasticX(true);
            return self;
        },
        contributor: function (id) {
            var self = dc.rowChart(id);
            self.width($(id).parent().width())
                .height(225)
                .margins({top: 10, left: 10, right: 10, bottom: 20})
                .group(cf.groups.username)
                .dimension(cf.dimensions.username)
                .colors(d3.scale.category20())
                .elasticX(true);
            return self;
        },
        project: function (id) {
            var self = dc.rowChart(id);
            self.width($(id).parent().width())
                .height(225)
                .margins({top: 10, left: 10, right: 10, bottom: 20})
                .group(cf.groups.projectNumber)
                .dimension(cf.dimensions.projectNumber)
                .colors(d3.scale.category20())
                .elasticX(true);
            return self;
        },
        overTime: function (id) {
            var self = dc.lineChart(id);
            self.width($(id).parent().width())
                .height(225)
                .renderArea(true)
                .margins({top: 10, right: 10, bottom: 30, left: 30})
                .dimension(cf.dimensions.day)
                .group(cf.groups.day)
                .elasticY(true)
                .x(d3.time.scale().domain(d3.extent(cf.groups.day.top(Infinity), function (d) {
                    return d.key;
                })))
                .renderHorizontalGridLines(true);
            return self;
        },
        table: function (id, dim) {
            var self = dc.dataTable(id);
            self.dimension(dim)
                .width($(id).parent().width())
                .group(function () {
                    return '';
                })
                .columns([
                    function (d) {
                        return "<a href='/contributors/"
                            + d.contributor.id
                            + "'>"
                            + getContribRepr(d.contributor)
                            + "</a>";
                    },
                    function (d) {
                        return "<a href='/projects/"
                            + d.project.id
                            + "'>"
                            + d.project.owner + "/" + d.project.name
                            + "</a>";
                    },
                    function (d) {
                        var parts = d.date.split(' ')[0].split('-');
                        return parts[1] + '/' + parts[2];
                    },
                    function (d) {
                        return d.changes;
                    },
                    function (d) {
                        return d.additions;
                    },
                    function (d) {
                        return d.deletions;
                    },
                    function (d) {
                        return d.message;
                    }])
                .sortBy(function (d) {
                    return d.date;
                })
                .order(d3.descending);

            return self;
        }
    };

}());

function hideLoadingSpinner() {
    $(".loading").fadeOut("fast");
}
function showLoadingSpinner() {
    $(".loading").fadeIn("fast");
}