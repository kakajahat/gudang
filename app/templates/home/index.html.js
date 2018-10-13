{% extends "base.html" %}
{% block title %}Home{% endblock %}
{% block head %}
    <link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='js/jsgrid/jsgrid.min.css') }}" />
    <link type="text/css" rel="stylesheet" href="{{ url_for('static', filename='js/jsgrid/jsgrid-theme.min.css') }}" />
<script type="text/javascript" src="{{ url_for('static', filename='js/jsgrid/jsgrid.min.js') }}"></script>
{% endblock %}

{% block body %}
<!--
<div class="intro-header">
    <div class="container">
        <div class="row">
            <div class="col-lg-12">
                <div class="intro-message">
                    <h1>Balikpapan WareHouse</h1>
                    <h3>The best warehouse in the world!</h3>
                    <hr class="intro-divider">
                    </ul>
                </div>
            </div>
        </div>
    </div>
</div>
--><br/><br/><br/>
<div id="jsGrid"></div>
<script>
    $("#jsGrid").jsGrid({
        width: "100%",
        height: "800px",
        
        filtering: true,
        editing: true,
        sorting: true,
        paging: true,
        autoload: true,
        selecting: true,
        
        pageSize: 15,
        pageButtonCount: 5,
        
        //inserting: true,
        //editing: true,
        //sorting: false,
        //paging: false,
        //autoload: true,
        controller: {
            loadData: function() {
                var d = $.Deferred();
                $.ajax({
                    url: "/api/inventory",
                    dataType: "json",
                    //type: "GET"
                }).done(function(response) {
                    d.resolve(response);
                });
                return d.promise();
            }
        //controller: db,
        },
        fields: [
            { name: "Nama", type: "text", width: 150, validate: "required" },
            { name: "Tgl Terima", type: "date" },
            { name: "Consumable", type: "checkbox", title: "anu" },
            { name: "Type", type: "text" },
            { name: "Serial", type: "text" },
            { name: "Qty", type: "number", width: 50 },
            { name: "Kondisi", type: "checkbox", title: "anu" },
            { name: "Penempatan", type: "text" },
            { name: "Keterangan", type: "text" },
            { name: "Asal", type: "text" },
            { name: "Tujuan", type: "text" },
            { type: "control" }
        ]
    });
</script>

{% endblock %}
