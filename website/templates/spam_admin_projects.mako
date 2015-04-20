<%inherit file="base.mako"/>
<%def name="title()">Spam Admin</%def>
<%def name="content()">


<div id="spam-admin" class="scripted">

    <nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <a class="navbar-brand" href="#">Projects <span class="badge" data-bind="text: total"></span></a>
    </div>


    <div class="collapse navbar-collapse" >
      <ul class="nav navbar-nav">
        <li ><a href="/spam_admin/comments">Comments </a></li>
        <li class="active"><a href="/spam_admin/projects">Projects <span class="sr-only">(current)</span></a></li>

      </ul>
      <form class="navbar-form navbar-right" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search Projects">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>

    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>


        <div  data-bind="foreach: {data: spamAdminProjects, as: 'project'}">
            <div class="search-result well">
                <div class=" pull-right"  role="group" aria-label="...">
                    <button type="button" class="btn btn-success" data-bind="click: function(data, event) { $parent.markHam(data, event) }" >Ham</button>
                    <button type="button" class="btn btn-danger" data-bind="click: function(data, event) { $parent.markSpam(data, event) }">Spam</button>
                </div>
                <h4>
                    <a data-bind="attr: { href: project.url }" >
                        <span data-bind="text: project.title"></span>
                    </a>
                </h4>
                <p>
                    <span data-bind="text: project.wiki"></span>
                </p>
                <p>
                    <strong>Author:</strong>
                    <span data-bind="text: project.creator"></span>
                    <span class="pull-right">
                        <strong>Last Edited:</strong>
                        <span data-bind="text: project.dateModified"></span>
                    </span>
                </p>
            </div>
        </div>








</%def>



<%def name="javascript_bottom()">
<script src=${"/static/public/js/spam-admin-page.js" | webpack_asset}></script>
</%def>