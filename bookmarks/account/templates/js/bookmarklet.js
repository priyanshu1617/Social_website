(function(){
  var siteUrl = 'http://127.0.0.1:8000/';
  if (window.myBookmarklet !== undefined) {
    window.myBookmarklet();
  } else {
    document.body.appendChild(document.createElement('script')).src = siteUrl + 'static/js/bookmarklet.js?r=' + Math.floor(Math.random()*9999999999999999);
  }
})();
