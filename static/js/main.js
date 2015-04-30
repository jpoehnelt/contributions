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
    var defer = $.Deferred(),
        url = "/api/commit?",
        commits = [], promises = [];

    if (project_id) {
        url += "project_id=" + String(project_id) + "&";
    }

    if (contributor_id) {
        url += "contributor_id=" + String(contributor_id);
    }

    $.ajax({
        method: "GET",
        url: url
    }).then(function (response) {
        // calculate the rest of the pages to get
        commits = $.merge(response.objects, commits);
        console.log(response);
        if (response.num_pages === 1) {
            defer.resolve(commits);
        } else {
            // get the other pages and resolve the promise when complete
            for (var i = 2; i <= response.num_pages; i++) {
                promises[i] = $.ajax({
                    method: "GET",
                    url: url + 'page=' + String(i)
                }).then(function (reponse) {
                    commits = $.merge(response.objects, commits);
                });
            }
            //
            // resolve the promise
            $.when.apply($, promises).then(function () {
                defer.resolve(commits)
            })
        }


    });

    return defer.promise();
}

function getAllCommits() {
    var defer = $.Deferred();

    $.ajax({ method: "GET", url: "/static/all_commits.json"}).then(function (response) {
        defer.resolve(response.objects);
    });

    return defer.promise();
}

(function () {
    "use strict";
    var cf = {};
    window.cf = cf;
    cf.data = crossfilter();

    function reduceAddFile(p, v) {
        p.count += v.files_total;
        p.python.sum += v.files_python;
        p.js.sum += v.files_js;
        p.css.sum += v.files_css;
        p.html.sum += v.files_html;
        p.other.sum += v.files_other;

        return p;
    }

    function reduceRemoveFile(p, v) {
        p.count -= v.files_total;//
        p.python.sum -= v.files_python;
        p.js.sum -= v.files_js;
        p.css.sum -= v.files_css;
        p.html.sum -= v.files_html;
        p.other.sum -= v.files_other;

        return p;
    }

    function reduceInitFile() {
        return {
            count: 0,
            python: {
                sum: 0
            },
            js: {
                sum: 0
            },
            css: {
                sum: 0
            },
            html: {
                sum: 0
            },
            other: {
                sum: 0
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
            return commit.project.project_number;
        }),
        project: cf.data.dimension(function (commit) {
            return commit.project.project_number + ": " + String(commit.project.id) + ": " + commit.project.name;
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
        project: cf.dimensions.project.group(),
        day: cf.dimensions.day.group(),
        timeOfDay: cf.dimensions.timeOfDay.group(),
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
        contributor: function (id, height) {
            var self = dc.rowChart(id);
            height = height ? height : $(id).parent().width();
            self.width($(id).parent().width())
                .height(height)
                .gap(1)
                .margins({top: 10, left: 10, right: 10, bottom: 20})
                .group(cf.groups.username)
                .dimension(cf.dimensions.username)
                .colors(d3.scale.category20())
                .elasticX(true)
                .ordering(function (d) {
                    return -d.value;
                });

            return self;
        },

        project: function (id, height) {
            var self = dc.rowChart(id);
            height = height ? height : $(id).parent().width();
            self.width($(id).parent().width())
                .height(height)
                .margins({top: 10, left: 10, right: 10, bottom: 30})
                .group(cf.groups.project)
                .dimension(cf.dimensions.project)
                .colors(d3.scale.category20())
                .elasticX(true)
                .gap(1)
                .label(function (d) {
                    var pieces = d.key.split(":");
                    return pieces[pieces.length - 1];
                })
                .ordering(function (d) {
                    return d.key.split(":")[0] * 10000000 - d.value;
                });
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
            self.dimension(cf.dimensions.project)
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
                height = Math.max(Math.min($(id).parent().width(), 400), 400);
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
                height = Math.max(Math.min($(id).parent().width(), 400), 400);

            self.margins({top: 20, right: 10, left: 29, bottom: 20})
                .width($(id).parent().width())
                .height(height)
                .dimension(cf.dimensions.timeOfDay)
                .group(cf.groups.timeOfDay)
                .colors(d3.scale.category20())
                .colorAccessor(function (d) {
                    if (d.key < 8) {
                        return 11;
                    }
                    if (d.key > 18) {
                        return 18;
                    }
                    return 0;
                }).label(function (d) {
                    var xm, hour;
                    if (d.key > 12) {
                        xm = ' pm';
                    } else {
                        xm = ' am';
                    }
                    hour = d.key % 12;
                    if (hour === 0) {
                        hour = 12;
                    }
                    return String(hour) + xm;

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