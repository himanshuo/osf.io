<%inherit file="base.mako"/>
<%def name="title()">Spam Admin</%def>
<%def name="content()">


<div id="himanshu">
    <nav class="navbar navbar-default">
  <div class="container-fluid">
    <!-- Brand and toggle get grouped for better mobile display -->
    <div class="navbar-header">
      <a class="navbar-brand" href="#">Comments <span class="badge">${num_possible_spam_comments}</span></a>
    </div>

    <!-- Collect the nav links, forms, and other content for toggling -->
    <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">
      <ul class="nav navbar-nav">
        <li class="active"><a href="/spam_admin/comments">Comments <span class="sr-only">(current)</span></a></li>
        <li ><a href="/spam_admin/projects">Projects</a></li>

      </ul>
      <form class="navbar-form navbar-right" role="search">
        <div class="form-group">
          <input type="text" class="form-control" placeholder="Search Comments">
        </div>
        <button type="submit" class="btn btn-default">Submit</button>
      </form>

    </div><!-- /.navbar-collapse -->
  </div><!-- /.container-fluid -->
</nav>

   <div  data-bind="foreach: {data: spamAdminComments, as: 'comment'}">
        <div class="search-result well">

            <div class=" pull-right"  role="group" aria-label="...">
              <button type="button" class="btn btn-success">Ham</button>
              <button type="button" class="btn btn-danger">Spam</button>

            </div>
            <h4><a data-bind="attr: { href: comment.project_url }" ><span data-bind="text: comment.project"></span></a></h4>


        <p><span data-bind="text: comment.content"></span></p>
            <p>
                <strong>Author:</strong> <span data-bind="text: comment.author"></span>
                <span class="pull-right"><strong>Last Edited:</strong>   <span data-bind="text: comment.dateModified"></span> </span></p>
        </div>

   </div>





</%def>



<%def name="javascript_bottom()">
<script src=${"/static/public/js/spam-admin-page.js" | webpack_asset}></script>
</%def>