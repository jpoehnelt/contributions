Date.prototype.addHours = function (h) {
    this.setHours(this.getHours() + h);
    return this;
};

var ANON = false;
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

function getAllCommits() {
    "use strict";
    return $.ajax({ method: "GET", url: "/static/all_commits.json"});
}

(function () {
    "use strict";
    var cf = {};
    window.cf = cf;
    cf.data = crossfilter();

    function reduceAddFile(p, v) {
        p.count += v.files.length;//
        for (var i = 0; i < v.files.length; i++) {
            var filenamePieces = v.files[i].filename.split('.');
            var filenameExt = filenamePieces[filenamePieces.length - 1];
            switch (filenameExt) {
                case 'py':
                    p.python.sum++;
                    break;
                case 'css':
                    p.css.sum++;
                    break;
                case 'html':
                    p.html.sum++;
                    break;
                case 'js':
                    p.js.sum++;
                    break;
                default:
                    p.other.sum++;
            }
        }
        return p;
    }

    function reduceRemoveFile(p, v) {
        p.count -= v.files.length;//
        for (var i = 0; i < v.files.length; i++) {
            var filenamePieces = v.files[i].filename.split('.');
            var filenameExt = filenamePieces[filenamePieces.length - 1];
            switch (filenameExt) {
                case 'py':
                    p.python.sum--;
                    break;
                case 'css':
                    p.css.sum--;
                    break;
                case 'html':
                    p.html.sum--;
                    break;
                case 'js':
                    p.js.sum--;
                    break;
                default:
                    p.other.sum--;
            }
        }
        return p;
    }

    function reduceInitFile() {
        return {
            count: 0,
            python: {
                sum: 0,
                avg: 0
            },
            js: {
                sum: 0,
                avg: 0
            },
            css: {
                sum: 0,
                avg: 0
            },
            html: {
                sum: 0,
                avg: 0
            },
            other: {
                sum: 0,
                avg: 0
            }
        };
    }

    // crossfilter dimensions allow indexing of these returned values for quick processing
    cf.dimensions = {
        sha: cf.data.dimension(function (commit) {
            return commit.id;
        }),
        username: cf.data.dimension(function (commit) {
            return getContribRepr(commit.contributor);
        }),
        projectNumber: cf.data.dimension(function (commit) {
            return commit.project.name;
        }),
        day: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            d = d.addHours(-7);
            d.setHours(0, 0, 0, 0);
            return d;
        }),
        timeOfDay: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            d = d.addHours(-7);
            return d.getHours();
        }),
        dayOfWeek: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            return d.addHours(-7).getDay();
        }),
        /* take the existing day function and modify it to return the difference between the commit.date and the project due date */
        priorToDueDate: cf.data.dimension(function (commit) {
            var d = new Date(commit.date);
            d = d.addHours(-7);
            /* return difference between d and dueDates[commit.project.project_number] */
            return d;
        }),
        files: cf.data.dimension(function (commit) {
            return commit.files;
        })
    };

    // groups based upon dimensions
    cf.groups = {
        sha: cf.dimensions.sha.group(),
        files: cf.dimensions.projectNumber.group().reduce(reduceAddFile, reduceRemoveFile, reduceInitFile),
        username: cf.dimensions.username.group(),
        projectNumber: cf.dimensions.projectNumber.group(),
        day: cf.dimensions.day.group(),
        timeOfDay: cf.dimensions.timeOfDay.group(),
        dayOfWeek: cf.dimensions.dayOfWeek.group(),
        priorToDueDate: cf.dimensions.priorToDueDate.group()
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
        },
        files: function (id) {
            var self = dc.barChart(id),
                height = Math.min($(id).parent().width(), 400);
            self.margins({top: 20, right: 20, left: 100, bottom: 20})
                .width($(id).parent().width())
                .height(height)
                .gap(1)
                .dimension(cf.dimensions.files)
                .group(cf.groups.files, 'Python')
                .valueAccessor(function (d) {
                    return d.value.python.sum;
                })
                .stack(cf.groups.files, 'JS', function (d) {
                    return d.value.js.sum;
                })
                .stack(cf.groups.files, 'HTML', function (d) {
                    return d.value.html.sum;
                })
                .stack(cf.groups.files, 'CSS', function (d) {
                    return d.value.css.sum;
                })
                .stack(cf.groups.files, 'Other', function (d) {
                    return d.value.other.sum;
                })
                .x(d3.scale.ordinal().domain(cf.groups.files.top(Infinity).map(function (p) {
                    return p.key;
                })))
                .xUnits(dc.units.ordinal)
                .centerBar(false)
                .elasticY(true)
                .elasticX(true)
                .brushOn(false)
                .label(function () {
                    return '';
                })
                .colors(d3.scale.category20())
                .legend(dc.legend().x(10).y(height / 5).itemHeight(13).gap(5));
            self.filter = function () {
            };
            return self;
        },
        timeOfDay: function (id) {
            var self = dc.rowChart(id),
                height = Math.min($(id).parent().width(), 400);

            self.margins({top: 20, right: 10, left: 25, bottom: 20})
                .width($(id).parent().width())
                .height(height)
                .dimension(cf.dimensions.timeOfDay)
                .group(cf.groups.timeOfDay)
                .colorAccessor(function (d) {
                    if (d.key < 8) {
                        return 1;
                    }
                    if (d.key > 18) {
                        return 2;
                    }
                    return 0;
                });

            return self;
        },
        priorToDueDate: function (id) {
            var self = dc.rowChart(id),
                height = Math.min($(id).parent().width(), 400);

            self.margins({top: 20, right: 10, left: 25, bottom: 20})
                .width($(id).parent().width())
                .height(height)
                .dimension(cf.dimensions.priorToDueDate)
                .group(cf.groups.priorToDueDate)
                .colorAccessor(function (d) {
                    if (d.key < 8) {
                        return 1;
                    }
                    if (d.key > 18) {
                        return 2;
                    }
                    return 0;
                });

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