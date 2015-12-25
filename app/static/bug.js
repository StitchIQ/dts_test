$(function() {
    $("#buglist").dataTable({
        "processing": true,
        ajax: "myjson2",
        columns: [
        {
            data: "posts.author"
        },
        {
            data: "posts.bug_level"
        },
        {
            data: "posts.bug_owner",
        },
        {
            data: "posts.bug_show_times",
        },
        {
            data: "posts.bug_status",
        },
        {
            data: "posts.bug_title",
        },
        {
            data: "posts.id",
        },
        {
            data: "posts.product_name",
        },
        {
            data: "posts.product_version",
        },
        {
            data: "posts.software_version",
        },
        {
            data: "posts.system_view",
        },
        {
            data: "posts.timestamp",
        },
        {
            data: "posts.url",
        }
        ]

    });
});